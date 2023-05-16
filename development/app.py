from dash import Dash, html, dcc, callback, Output, Input
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import plotly.express as px
import pandas as pd



#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]
# https://developers.google.com/identity/protocols/oauth2/scopes

# https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md
API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
CLIENT_SECRETS_FILE = "/youtube_analytics/client_secret_889124158621-s2c9bu0j2batb5nvm2mlni74efq63okq.apps.googleusercontent.com.json"

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(
        **kwargs
    ).execute()
    print(response)
    return response

today = datetime.today().strftime('%Y-%m-%d')


if __name__ == "__main__":
    # https://developers.google.com/youtube/analytics/data_model
    youtubeAnalytics = get_service()
    result = execute_api_request(
        youtubeAnalytics.reports().query,
        ids="channel==MINE",
        startDate="2022-01-01",
        endDate=today,
        metrics="views,likes,subscribersGained,estimatedMinutesWatched,averageViewDuration,shares",
        dimensions="day,creatorContentType",
        sort="day"
    )

columns = [
    result['columnHeaders'][0]['name'],
    result['columnHeaders'][1]['name'],
    result['columnHeaders'][2]['name'],
    result['columnHeaders'][3]['name'],
    result['columnHeaders'][4]['name'],
    result['columnHeaders'][5]['name'],
    result['columnHeaders'][6]['name'],
    result['columnHeaders'][7]['name']
]

df = pd.DataFrame(result["rows"])
df.columns = columns

# Filter out shorts and creatorContentTypeUnspecified
df_video_and_live = df[~df['creatorContentType'].isin(['shorts', 'creatorContentTypeUnspecified'])]
df_video_and_live['watch_hours'] = df_video_and_live['estimatedMinutesWatched'] / 60
df_video_and_live['cumulative_watch_hours'] = df_video_and_live['watch_hours'].cumsum()
df_video_and_live['partner_goal_watch_hours'] = 4000
df_video_and_live_2023 = df_video_and_live[df_video_and_live['day'] > '2023-03-01']

fig1 = px.line(df_video_and_live_2023, x='day', y='cumulative_watch_hours')
fig2 = px.line(df_video_and_live_2023, x='day', y='watch_hours', color='creatorContentType')

app = Dash(__name__)

app.layout = html.Div([
    # html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    # dcc.Dropdown(df['country'].unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2)
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = df[df['country']==value]
    return px.line(dff, x='year', y='pop')

#if __name__ == '__main__':
#    app.run_server(debug=True)
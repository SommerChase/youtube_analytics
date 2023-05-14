"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        title="Plotly Dash Flask Tutorial",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )

@app.route('/test')
def test_api_request():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  youtubeAnalytics = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)

  today = datetime.today().strftime('%Y-%m-%d')

  #report = youtube.reports().query(ids='channel==MINE', start_date='2016-05-01', end_date='2016-06-30', metrics='views').execute()
      
  #youtubeAnalytics = get_service()
  report = youtubeAnalytics.reports().query(
        ids="channel==MINE",
        startDate="2022-01-01",
        endDate=today,
        metrics="views,likes,subscribersGained,estimatedMinutesWatched,averageViewDuration,shares",
        dimensions="day,creatorContentType",
        sort="day"
    ).execute()

  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.jsonify(**report)


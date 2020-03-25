# web_radio_song_scrape

Project is a python web service app that will go out and scrape a given streaming radio's playlist
and pull the song, artist and album.  Before comminting to the database, app chackes if song, artist and album'
already exists in database. If so

Any number of streaming radio stations can be scrpaed by entering their info into the webstation table in the database.

Database engine is Postgres and SQL for tables is included in resources folder.

Chromedriver is needed for headless browser to get webpage.

App is deployed in a container and I currently have this version running in Google Cloud Platform in Cloud Run.

Using GCP job automation to call endpoint every hour, but can be executed manually.

Do not have db in container, instead currently have db run in GCP Cloud SQL.

Logging only goes to standard out and err those are automatically monitored by GCP loggging andf can easily be viewed in the console.

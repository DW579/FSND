#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# Implementation of flask_migrate
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database (Done)
# Connected to local db 'fyyur' through config.py file

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model): # Done
    __tablename__ = 'venue'

    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    past_shows_count = db.Column(db.Integer, default=0)
    upcoming_shows_count = db.Column(db.Integer, default=0)
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (Done)

class Artist(db.Model): # Done
    __tablename__ = 'artist'

    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    past_shows_count = db.Column(db.Integer, default=0)
    upcoming_shows_count = db.Column(db.Integer, default=0)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (Done)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Genres(db.Model): # Done
    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class VenueGenres(db.Model): # Done
    __tablename__ = 'venue_genres'

    venue_genre_id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, default=0)
    genre_id = db.Column(db.Integer, default=0)

class ArtistGenres(db.Model): # Done
    __tablename__ = 'artist_genres'

    artist_genre_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, default=0)
    genre_id = db.Column(db.Integer, default=0)

class PastShows(db.Model): # Done
    __tablename__ = 'past_shows'

    past_show_id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, default=0)
    artist_id = db.Column(db.Integer, default=0)
    start_time = db.Column(db.String(120))

class UpcomingShows(db.Model): # Done
    __tablename__ = 'upcoming_shows'

    upcoming_show_id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, default=0)
    artist_id = db.Column(db.Integer, default=0)
    start_time = db.Column(db.String(120))

class Shows(db.Model): # Done
    __tablename__ = 'shows'

    show_id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, default=0)
    artist_id = db.Column(db.Integer, default=0)
    start_time = db.Column(db.String(120))

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'): # Nothing to do
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/') # Nothing to do
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues') # Done
def venues():
  # TODO: replace with real venues data. (Done)
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # Query the data in the venue table
  venue_data = Venue.query.all()
  # Hash map to quickly look up where in the data array is a location
  data_map = {}
  # Array of formated venue data to be used on venues.html
  data = []

  # Loop through the objects of queried venue data
  for venue in venue_data:
    # Create a string of the location of the venue
    location = venue.city + ", " + venue.state
    # Blank object that will be appened to the data array
    venue_data = {}
    
    # If the venues location is in the data_map hash, add the venue_data to data array
    if location in data_map:
      venue_data = {
        "id": venue.venue_id,
        "name": venue.name,
        "num_upcoming_shows": venue.upcoming_shows_count
      }

      data[data_map[location]]["venues"].append(venue_data)

    # If the venues location is new, create a new location that will expand the data array length
    else:
      data_map[location] = len(data)

      venue_data = {
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.venue_id,
          "name": venue.name,
          "num_upcoming_shows": venue.upcoming_shows_count
        }]
      }

      data.append(venue_data)

  # Send the data array data to the venues.html page
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST']) # Done
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive. (Done)
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  # Grab user search term from the form POST
  search_term = request.form.get('search_term', None)
  # Query all rows in venue table
  venue_data = Venue.query.all()
  # Inilized response data for user search
  response = {
    "count": 0,
    "data": []
  }

  # Loop through all the venues in venue table
  for venue in venue_data:

    # If user search term is a substring within the venue name
    if search_term.lower() in venue.name.lower():
      # Increment by 1 the response count
      response["count"] += 1
      # Object to append to response data
      match_venue = {
        "id": venue.venue_id,
        "name": venue.name,
        "num_upcoming_shows": venue.upcoming_shows_count
      }

      response["data"].append(match_venue)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>') # Done
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  # Query for specific venue's data by ID
  venue_data = Venue.query.get(venue_id)
  # Query for all venue genres
  venue_genres = VenueGenres.query.all()
  # Query for all past shows
  past_shows = PastShows.query.all()
  # Query for all upcoming shows
  upcoming_shows = UpcomingShows.query.all()

  data = {
    "id": venue_id,
    "name": venue_data.name,
    "genres": [],
    "address": venue_data.address,
    "city": venue_data.city,
    "state": venue_data.state,
    "phone": venue_data.phone,
    "website": venue_data.website,
    "facebook_link": venue_data.facebook_link,
    "seeking_talent": venue_data.seeking_talent,
    "seeking_description": venue_data.seeking_description,
    "image_link": venue_data.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": venue_data.past_shows_count,
    "upcoming_shows_count": venue_data.upcoming_shows_count
  }

  # Add venue genres to data['genres']
  for venue_genre in venue_genres:

    if venue_genre.venue_id == venue_id:
      data['genres'].append(Genres.query.get(venue_genre.genre_id).name)

  # Add past shows to data['past_shows']
  for past_show in past_shows:

    if past_show.venue_id == venue_id:
      past_show_artist = {
        "artist_id": past_show.artist_id,
        "artist_name": Artist.query.get(past_show.artist_id).name,
        "artist_image_link": Artist.query.get(past_show.artist_id).image_link,
        "start_time": past_show.start_time
      }

      data['past_shows'].append(past_show_artist)

  # Add upcoming shows to data['upcoming_shows']
  for upcoming_show in upcoming_shows:
    
    if upcoming_show.venue_id == venue_id:
      upcoming_show_artist = {
        "artist_id": upcoming_show.artist_id,
        "artist_name": Artist.query.get(upcoming_show.artist_id).name,
        "artist_image_link": Artist.query.get(upcoming_show.artist_id).image_link,
        "start_time": upcoming_show.start_time
      }

      data['upcoming_shows'].append(upcoming_show_artist)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET']) # Nothing to do
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists') # Done
def artists():
  # TODO: replace with real data returned from querying the database

  # Query all artists in artist table in db
  all_artist_data = Artist.query.all()
  # Declare data array to hold artist data to be forwarded to pages/artists.html
  data = []

  # Loop through all artist and build objects of their data to be appened into data array
  for artist in all_artist_data:
    artist_data = {
      "id": artist.artist_id,
      "name": artist.name
    }

    data.append(artist_data)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST']) # Done
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # Grab user search term from the form POST
  search_term = request.form.get('search_term', None)
  # Query all rows in artist table
  artist_data = Artist.query.all()
  # Inilized response data for user search
  response = {
    "count": 0,
    "data": []
  }

  # Loop through all the artists in artist table
  for artist in artist_data:

    # If user search term is a substring within the artist name
    if search_term.lower() in artist.name.lower():
      # Increment by 1 the response count
      response["count"] += 1
      # Object to append to response data
      match_artist = {
        "id": artist.artist_id,
        "name": artist.name,
        "num_upcoming_shows": artist.upcoming_shows_count
      }

      response["data"].append(match_artist)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>') # Done
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  # Query for specific artist's data by ID
  artist_data = Artist.query.get(artist_id)
  # Query for all artist genres
  artist_genres = ArtistGenres.query.all()
  # Query for all past shows
  past_shows = PastShows.query.all()
  # Query for all upcoming shows
  upcoming_shows = UpcomingShows.query.all()

  data = {
    "id": artist_id,
    "name": artist_data.name,
    "genres": [],
    "city": artist_data.city,
    "state": artist_data.state,
    "phone": artist_data.phone,
    "website": artist_data.website,
    "facebook_link": artist_data.facebook_link,
    "seeking_venue": artist_data.seeking_venue,
    "seeking_description": artist_data.seeking_description,
    "image_link": artist_data.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": artist_data.past_shows_count,
    "upcoming_shows_count": artist_data.upcoming_shows_count
  }

  # Add artist genres to data['genres']
  for artist_genre in artist_genres:

    if artist_genre.artist_id == artist_id:
      data['genres'].append(Genres.query.get(artist_genre.genre_id).name)

  # Add past shows to data['past_shows']
  for past_show in past_shows:

    if past_show.artist_id == artist_id:
      past_show_venue = {
        "venue_id": past_show.venue_id,
        "venue_name": Venue.query.get(past_show.venue_id).name,
        "venue_image_link": Venue.query.get(past_show.venue_id).image_link,
        "start_time": past_show.start_time
      }

      data['past_shows'].append(past_show_venue)

  # Add upcoming shows to data['upcoming_shows']
  for upcoming_show in upcoming_shows:
    
    if upcoming_show.artist_id == artist_id:
      upcoming_show_venue = {
        "venue_id": upcoming_show.venue_id,
        "venue_name": Venue.query.get(upcoming_show.venue_id).name,
        "venue_image_link": Venue.query.get(upcoming_show.venue_id).image_link,
        "start_time": upcoming_show.start_time
      }

      data['upcoming_shows'].append(upcoming_show_venue)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET']) # Nothing to do
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows') # Done
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # Query all shows
  all_shows = Shows.query.order_by(Shows.start_time.asc())
  # Data array that will be passed to /shows.html
  data = []

  for show in all_shows:
    show_data = {
      "venue_id": show.venue_id,
      "venue_name": Venue.query.get(show.venue_id).name,
      "artist_id": show.artist_id,
      "artist_name": Artist.query.get(show.artist_id).name,
      "artist_image_link": Artist.query.get(show.artist_id).image_link,
      "start_time": show.start_time
    }

    data.append(show_data)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create') # Nothing to do
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404) # Nothing to do
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500) # Nothing to do
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

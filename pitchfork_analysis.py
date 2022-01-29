import sqlite3
import numpy as np
import pandas as pd

#%% Constants

dbpath = 'data/database.sqlite'

# %% Get reviews data from database

# Establish connection to database
conn = sqlite3.connect(dbpath)

# Show tables in database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print(cursor.fetchall())

def make_query(table_name):
    return "SELECT * FROM " + table_name

reviews = pd.read_sql_query(make_query("reviews"), conn)
artists = pd.read_sql_query(make_query("artists"), conn)
genres = pd.read_sql_query(make_query("genres"), conn)
labels = pd.read_sql_query(make_query("labels"), conn)
years = pd.read_sql_query(make_query("years"), conn)
content = pd.read_sql_query(make_query("content"), conn)

# Add album years to reviews
years_deduped = years.sort_values(by='year').drop_duplicates('reviewid').sort_index()
reviews = pd.merge(reviews, years_deduped, how='left', on='reviewid')

#%% Function to filter reviews to a given genre

def get_genre_reviews(reviews_data, genres_data, genre):
    """
    Create a copy of reviews dataset containing only albums of a given genre
    (according to the genres dataset)

    Parameters
    ----------
    reviews : dataframe
        The reviews dataset.
    genres_data : dataframe
        The genres dataset.
    genre : string
        The name of the desired genre.

    Returns
    -------
    genre_reviews : dataframe
        A copy of reviews_data filtered to albums with an entry in genres_data
        for the given genre.
    """
    genres_filtered = genres_data[genres_data.genre == genre]
    genre_reviews = reviews_data[reviews_data.reviewid.isin(genres_filtered.reviewid)]
    return genre_reviews

#%% Best albums/artists by genre

my_genre = 'rap'
genre_reviews = get_genre_reviews(reviews, genres, my_genre)

genre_reviews.head()

# Top albums in genre
n_top = 20
genre_reviews_top = genre_reviews.sort_values(by='score', ascending=False)[:n_top]

print(genre_reviews_top[['title', 'artist', 'year', 'score']])

# Artists with best average scores (with at least n albums)
n_albums = 3
n_top_artists = 10

genre_artist_counts = genre_reviews.groupby('artist').apply(len).rename('n_albums')

genre_artists = pd.merge(genre_reviews, genre_artist_counts, on='artist')
genre_artist_avg = genre_artists[genre_artists.n_albums >= n_albums].groupby('artist')[['artist', 'score']].mean().reset_index()

genre_artists_top = genre_artist_avg.sort_values(by='score', ascending=False)[:n_top_artists]

print(genre_artists_top)



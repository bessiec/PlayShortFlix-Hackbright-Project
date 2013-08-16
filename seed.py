import csv
import datetime
import models
from models import session
models.create_db()


s = models.session


def load_films(session):
    with open ('films.csv','rU') as f:
        filename_films = csv.reader(f, delimiter=',')
        for film_row in filename_films:
            new_film_row = models.Films(title=film_row[0],genre=film_row[1], url=film_row[2], 
                link_type=film_row[3], embed=film_row[4])
            session.add(new_film_row)
        session.commit()
        session.refresh(new_film_row)


def load_playlist_entries(session):
    with open ('stock_playlists.csv', 'rU') as f:
        filename_playlists = csv.reader(f, delimiter=",")
        for playlist_row in filename_playlists:
            new_playlist_row = models.Playlist_Entry( playlist_id=playlist_row[1],
                film_id=playlist_row[2], play_order=playlist_row[3])
            session.add(new_playlist_row)
        session.commit()

def load_playlists(session):
    user = 1
    playlist_titles = ["Narrative Shorts", "Something Different", "Hellbent Sports", "Documentaries"]
    for title in playlist_titles:
        playlist = models.Playlists(title=title, user_id=user)
        session.add(playlist)
    session.commit()

def main(session):
    load_films(session)
    load_playlist_entries(session)
    load_playlists(session)

if __name__ == "__main__":
    main(s)
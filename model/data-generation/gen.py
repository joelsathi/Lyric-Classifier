# import requests
# from bs4 import BeautifulSoup
import re
import pandas as pd
from auth import authenticate_genius, authenticate_spotify

# def get_lyrics(song, artist, lyricsgenius):
#     genius = lyricsgenius.Genius('')
#     song = genius.search_song(title=song, artist=artist)
#     try:
#       lyrics = song.lyrics
#       print(lyrics)
#       print('\n')
#     except AttributeError:
#       print("There are no lyrics for this song on Genius")
#       print('\n')

# def scrape_lyrics(artistname, songname):
#     artistname2 = str(artistname.replace(' ', '-')) if ' ' in artistname else str(artistname)
#     songname2 = str(songname.replace(' ', '-')) if ' ' in songname else str(songname)
#     page = requests.get('https://genius.com/' + artistname2 + '-' + songname2 + '-' + 'lyrics')
#     html = BeautifulSoup(page.text, 'html.parser')
#     lyrics1 = html.find("div", class_="lyrics")
#     lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
#     if lyrics1:
#         lyrics = lyrics1.get_text()
#     elif lyrics2:
#         lyrics = lyrics2.get_text()
#     elif lyrics1 == lyrics2 == None:
#         lyrics = None
#     return lyrics

# def lyrics_onto_frame(df1, artist_name):
#     for i, x in enumerate(df1['Track Name']):
#         test = scrape_lyrics(artist_name, x)
#         print(test)
#         df1.loc[i, 'Lyrics'] = test
#     return df1

def get_lyrics_df(sp, genius, offset=0, genre='classic'):
    artist_names = []
    track_names = []
    release_dates = []
    genres = []
    lyrics = []

    pop_tracks = sp.search(q=f'genre:{genre}', type='track', limit=50, offset=offset)

    # Iterate through the search results and collect data
    i = 1
    for track in pop_tracks['tracks']['items']:
        try:
            i += 1

            song = genius.search_song(track['name'], track['artists'][0]['name'])
            song = song.to_dict()
            l = song["lyrics"]
            l = re.sub(r'^.*?\n+', '', l, count=1)
            l = re.sub(r'\s+', ' ', l)

            lyrics.append(l)
            artist_names.append(track['artists'][0]['name'])
            track_names.append(track['name'])
            release_dates.append(track['album']['release_date'])
            genres.append(genre)

        except:
            pass

    # Create a DataFrame
    data = {
        'artist_name': artist_names,
        'track_name': track_names,
        'release_date': release_dates,
        'genre': genres,
        'lyrics': lyrics
    }

    df = pd.DataFrame(data)

    # df['release_date'] = pd.to_datetime(df['release_date'])
    # df = df.dropna(subset=['release_date'])
    # df['release_date'] = df['release_date'].dt.year.astype('int64')

    return df

sp = authenticate_spotify()
genius = authenticate_genius()

if __name__ == "__main__":

    genre = 'classic'
    
    df1 = get_lyrics_df(sp, genius)
    print(df1.head())

    df2 = get_lyrics_df(sp, genius, offset=80)
    print(df2.head())

    df3 = get_lyrics_df(sp, genius, offset=200)
    print(df3.head())

    # Concatenate the DataFrames
    df = pd.concat([df1, df2, df3], ignore_index=True)

    # Remove duplicates based on 'track_name' and 'artist_name'
    df = df.drop_duplicates(subset=['track_name', 'artist_name'], keep='first')
    # Reset the index
    df.reset_index(drop=True, inplace=True)
    # Print the DataFrame
    print(df.head())

    # Save the DataFrame to a CSV file
    df.to_csv(f'{genre}_lyrics.csv', index=False)
    print(f"DataFrame saved to '{genre}_lyrics.csv'")

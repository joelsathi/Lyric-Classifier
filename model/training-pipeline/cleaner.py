import pandas as pd

mendaly_musi = pd.read_csv('../data/tcc_ceds_music.csv')
classic_music = pd.read_csv('../data/classic_lyrics.csv')

df = mendaly_musi[["artist_name", "track_name", "release_date", "genre", "lyrics"]]

# drop the rows with null values in the release_date column
df = df.dropna(subset=['release_date'])

# Go through the classic_music df and in the release_date column, the data is in the format YYYY-MM-DD, so we need to convert it to YYYY
# and then convert it to int64

classic_music['release_date'] = pd.to_datetime(classic_music['release_date'], errors='coerce')

invalid_dates = classic_music[classic_music['release_date'].isna()]

classic_music = classic_music.dropna(subset=['release_date'])

classic_music['release_date'] = classic_music['release_date'].dt.year.astype('int64')

# convert all the genre values to country from retro
classic_music['genre'] = classic_music['genre'].replace(['retro'], 'country')

print(classic_music.head())

# Save classic_music to a csv file
classic_music.to_csv('../data/Student_dataset.csv', index=False)

print("Shape of the mendaly_musi df: ", df.shape)
print("Shape of the classic_music df: ", classic_music.shape)

print("\n"*3)

# combine the two dataframes

combined_df = pd.concat([df, classic_music], ignore_index=True)
print("Shape of the combined df: ", combined_df.shape)

for col in ["artist_name", "track_name", "lyrics"]:
    combined_df[col] = combined_df[col].str.replace('\n', ' ')
    combined_df[col] = combined_df[col].str.replace('\t', ' ')
    combined_df[col] = combined_df[col].str.replace(',', ' ')
    combined_df[col] = combined_df[col].str.replace(r'\s+', ' ', regex=True)

# Save the combined dataframe to a csv file
combined_df.to_csv('../data/Merged_dataset.csv', index=False)

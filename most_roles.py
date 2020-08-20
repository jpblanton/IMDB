import csv

import pandas as pd

###
# Need to read in basics for getting titleType of movie or TvMovie
# Need to read in principals to get actors number roles
# Can get name basics at the very end when we have the highest count by NameID
# Also want to read in title.akas.tsv to enable filtering for only english language films
# If want to get really fancy, coiuld implement chunk_filter function using dict of {column : filter}
# columns we don't need at all: ordering, job(?) (principals), types, attributes, isOrigTitle (akas)

reader = pd.read_table('title.basics.tsv', na_values=r'\N', quoting=csv.QUOTE_NONE, chunksize = 5*10e4)

dataframes = []
for chunk in reader:
    tmp = chunk[chunk['titleType'].isin({'movie', 'tvMovie'})]
    dataframes.append(tmp)

movie_df = pd.concat(dataframes)
movie_ids = set(movie_df['tconst'])

reader = pd.read_table('title.principals.tsv', na_values=r'\N', quoting=csv.QUOTE_NONE, chunksize=5*10e4)

dataframes = []
for chunk in reader:
    tmp = chunk[chunk['tconst'].isin(movie_ids)]
    tmp = tmp[tmp['category'].isin({'actor', 'actress', 'self'})]
    dataframes.append(tmp)

actor_df = pd.concat(dataframes)

reader = pd.read_table('title.akas.tsv', na_values=r'\N', quoting=csv.QUOTE_NONE, chunksize=5*10e4)

dataframes = []
for chunk in reader:
    tmp = chunk[chunk['titleId'].isin(movie_ids)]
    dataframes.append(tmp)

akas_df = pd.concat(dataframes)
main_titles = akas_df[akas_df['isOriginalTitle'] == 1]

names_df = pd.read_table('name.basics.tsv', na_values=r'\N', usecols=['nconst', 'primaryName'])
final_df = pd.merge(left=actor_df, right=names_df, left_on='nconst', right_on='nconst', how='left')
final_df = pd.merge(left=final_df, right=main_titles, left_on='tconst', right_on='titleId', how='left') 
final_df = pd.merge(left=final_df, right=movie_df, left_on='tconst', right_on='tconst', how='left')

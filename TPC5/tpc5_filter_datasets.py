# Datasets From:
# https://developer.imdb.com/non-commercial-datasets/

import pandas
from datetime import datetime
import os


def load_filter_TSVs(file_tBasics, file_tAkas, file_tPrincipals, file_nBasics):
    files_to_rm = []
    
    temp_filename = "." + str(datetime.now().timestamp()) + ".csv"
    files_to_rm.append(temp_filename) # 0movies
    movies_set_1 = set()
    for chunk in pandas.read_csv(file_tBasics, sep="\t", usecols=["tconst", "titleType", "primaryTitle", "originalTitle", "startYear", "runtimeMinutes", "genres"], dtype={"tconst": "str", "titleType": "str", "primaryTitle": "str", "originalTitle": "str", "startYear": "str", "runtimeMinutes": "str", "genres": "str"}, na_values="\\N", chunksize=100000):
        chunk_filtered = chunk[chunk["titleType"] == "movie"]
        chunk_filtered = chunk_filtered.drop_duplicates(subset=["tconst", "primaryTitle", "originalTitle"], keep="first")
        chunk_filtered = chunk_filtered.dropna()
        movies_set_1.update(chunk_filtered["tconst"])
        chunk_filtered.to_csv(temp_filename, mode='a', index=False, header=not os.path.exists(temp_filename))
    print("Movies' first filter done")
    
    temp_filename = "." + str(datetime.now().timestamp()) + ".csv"
    files_to_rm.append(temp_filename) # 0movies, 1akas
    akas_set_1 = set()
    for chunk in pandas.read_csv(file_tAkas, sep="\t", usecols=["titleId", "language", "region"], dtype={"titleId": "str", "language": "str", "region": "str"}, na_values="\\N", chunksize=100000):
        chunk_filtered = chunk[chunk["titleId"].isin(movies_set_1)]
        chunk_filtered = chunk_filtered.drop_duplicates(subset=["titleId", "language", "region"], keep="first")
        chunk_filtered = chunk_filtered.dropna()
        akas_set_1.update(chunk_filtered["titleId"])
        chunk_filtered.to_csv(temp_filename, mode='a', index=False, header=not os.path.exists(temp_filename))
    print("Akas' first filter done")
    
    temp_filename = "." + str(datetime.now().timestamp()) + ".csv"
    files_to_rm.append(temp_filename) # 0movies, 1akas, 2principals
    principals_set_1 = set()
    for chunk in pandas.read_csv(file_tPrincipals, sep="\t", usecols=["tconst", "nconst", "characters"], dtype={"tconst": "str", "nconst": "str", "characters": "str"}, na_values="\\N", chunksize=100000, low_memory=False, encoding="utf-8"):
        chunk_filtered = chunk[chunk["tconst"].isin(akas_set_1)]
        chunk_filtered = chunk_filtered.drop_duplicates(subset=["tconst", "nconst", "characters"], keep="first")
        chunk_filtered = chunk_filtered.dropna()
        principals_set_1.update(chunk_filtered["nconst"])
        chunk_filtered.to_csv(temp_filename, mode='a', index=False, header=not os.path.exists(temp_filename))
    print("Principals' first filter done")
    
    
    temp_filename = "." + str(datetime.now().timestamp()) + ".csv"
    files_to_rm.append(temp_filename) # 0movies, 1akas, 2principals, 3actors
    actors_set_1 = set()
    for chunk in pandas.read_csv(file_nBasics, sep="\t", usecols=["nconst", "primaryName"], dtype={"nconst": "str", "primaryName": "str"}, na_values="\\N", chunksize=100000):
        chunk_filtered = chunk[chunk["nconst"].isin(principals_set_1)]
        chunk_filtered = chunk_filtered.drop_duplicates(subset=["nconst", "primaryName"], keep="first")
        chunk_filtered = chunk_filtered.dropna()
        actors_set_1.update(chunk_filtered["nconst"])
        chunk_filtered.to_csv(temp_filename, mode='a', index=False, header=not os.path.exists(temp_filename))
    print("Actors' first filter done")
    print("First phase of reading and filtering is completed.")
    
    print("Starting second phase of filtering...")
    # 0movies, 1akas, 2principals, 3actors
    print("Started loading files...")
    movies = pandas.read_csv(files_to_rm[0], dtype={"tconst": "str", "titleType": "str", "primaryTitle": "str", "originalTitle": "str", "startYear": "str", "runtimeMinutes": "str", "genres": "str"})
    akas = pandas.read_csv(files_to_rm[1], dtype={"titleId": "str", "language": "str", "region": "str"})
    principals = pandas.read_csv(files_to_rm[2], dtype={"tconst": "str", "nconst": "str", "characters": "str"})
    actors = pandas.read_csv(files_to_rm[3], dtype={"nconst": "str", "primaryName": "str"})
    print("Files loaded successfully.")
    
    print("Starting second filtering...")
    
    movies = movies[movies["tconst"].isin(akas["titleId"])]
    akas = akas[akas["titleId"].isin(movies["tconst"])]
    # add akas columns to movies
    akas = akas.rename(columns={"titleId": "tconst"})
    movies = movies.merge(akas, on="tconst", how="inner")
    movies.dropna(inplace=True)
    akas = None
    
    principals = principals[principals["tconst"].isin(movies["tconst"])]
    principals = principals[principals["nconst"].isin(actors["nconst"])]
    movies = movies[movies["tconst"].isin(principals["tconst"])]
    actors = actors[actors["nconst"].isin(principals["nconst"])]
    
    print("Second filtering completed.")
    print("Saving results...")
    movies.to_csv("movies.csv", index=False)
    actors.to_csv("actors.csv", index=False)
    principals.to_csv("principals.csv", index=False)
    for f in files_to_rm:
        os.remove(f)
    print("Results saved.")
    
    
    

if __name__ == "__main__":
    load_filter_TSVs("title.basics.tsv", "title.akas.tsv", "title.principals.tsv", "name.basics.tsv")
    #filter_save_results()
    #print("Process completed.")
    
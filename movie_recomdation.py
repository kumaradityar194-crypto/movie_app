import pandas as pd
import numpy as np

movie=pd.read_csv(r"c:\Users\kumar\OneDrive\Desktop\Daatasheet\tmdb_5000_movies.csv")
print(movie.shape)

print(movie.head(10))
missing=movie.isnull().sum()
print("Missing",missing)

credit=pd.read_csv(r"c:\Users\kumar\OneDrive\Desktop\Daatasheet\tmdb_5000_credits.csv")
print("\n")
print(credit.head(10))
print(credit.shape)

movie=movie.merge(credit,on='title')
print(movie.head(10))
print(movie.shape)

print(movie.info())
movie=movie[["movie_id","title","overview","genres","keywords","cast","crew"]]
print(movie.head(10))
print(movie.shape)
missing=movie.isna().sum()
print("Missing....",missing)
movie.dropna(inplace=True)
miss=movie.isna().sum()
print("Missing....",miss)

import ast

def convert(text):
    L=[]
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L
    
movie["genres"]=movie["genres"].apply(convert)
movie["keywords"]=movie["keywords"].apply(convert)
movie["cast"]=movie["cast"].apply(convert)
movie["cast"]=movie["cast"].apply(lambda x:x[0:3])

def director(text):
    L=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            L.append(i['name'])
    return L

movie["crew"]=movie["crew"].apply(director)

print(movie.head(10))

def police(l):
    L=[]
    for i in l:
        L.append(i.replace(" ",""))
    return L

movie["genres"]=movie["genres"].apply(police)
movie["keywords"]=movie["keywords"].apply(police)
movie["cast"]=movie["cast"].apply(police)
movie["crew"]=movie["crew"].apply(police)

print(movie.head(10))

print(movie["overview"][0])
movie["overview"]=movie["overview"].apply(lambda x:x.split())
print("\n")
print(movie["overview"][0])

movie['tag']=movie["genres"]+movie["keywords"]+movie["cast"]+movie["crew"]+movie["overview"]
dataset=movie.drop(columns=["genres","keywords","cast","crew","overview"])
print("\n")
print(dataset.head(10))
print(dataset.shape)
print(movie["tag"][0])

dataset["tag"]=movie["tag"].apply(lambda x:" ".join(x))
print(dataset.head(10))

from sklearn.feature_extraction.text import CountVectorizer
ev=CountVectorizer(max_features=5000,stop_words='english')

Vector=ev.fit_transform(dataset["tag"]).toarray()
print(Vector.shape)

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(Vector)

print("Enter your movie;")
movie=input("movie:")
    
def recommend(movie):
    dataset['title_clean'] = dataset['title'].str.lower().str.replace(" ", "").str.replace("-", "")

    movie = movie.lower().replace(" ", "").replace("-", "")

    if movie not in dataset['title_clean'].values:
        print("❌ Movie not found in dataset")
        return

    index = dataset[dataset['title_clean'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    print("🎬 Recommended movies:")
    for i in distances[1:6]:
        print(dataset.iloc[i[0]].title)

        
print("here recomndede movie.......")
recommend(movie)
    
    
import pickle

pickle.dump(dataset, open("movie_dict.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))
print("Done")

import requests
import json

omdbapikey=input("Enter OMDB API key : ")

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

## Find similer movies based on movie name
def get_movies_from_tastedive(name):
    baseurl="https://tastedive.com/api/similar"
    params={'q':name,'type':'movies', 'limit':20}
    response=requests.get(baseurl,params)
    return response.json()

#### Extracts movie names from json received from testedive
def extract_movie_titles(suggestions):
    similar_movies=list()
    for i in suggestions['Similar']['Results']:
        similar_movies.append(i['Name'])
    return (similar_movies)

##### Takes movie names as list and finds similer movies and removes duplicates
def get_related_titles(movielist):
    uniquemovies=list()
    for movie in movielist:
        allmovies=(extract_movie_titles(get_movies_from_tastedive(movie)))
        for m in allmovies:
            if m not in uniquemovies:
                uniquemovies.append(m)
    return uniquemovies

#### API to connect to OMDB, needs API key
def get_movie_data(m):
    baseurl="http://www.omdbapi.com/"
    params={'apikey': omdbapikey, 't': m, 'r':'json'}
    moviedata=requests.get(baseurl,params=params)
    return moviedata.json()

####Extracts rotten Tomatoes ratings
def get_movie_rating(omdb_d):
    rating=0
    try:
        if omdb_d['Ratings'][1]["Source"] == "Rotten Tomatoes":
            rating = int(omdb_d['Ratings'][1]["Value"].strip('%'))
    except:
        rating = 0
    return rating

#####Sorts movies based on Rotten Tomatoes ratings, highest to lowest, Movie names as tie breaker
def get_sorted_recommendations(movielist):
    related=get_related_titles(movielist) 
    return sorted(related,key=lambda x:(get_movie_rating(get_movie_data(x)),x),reverse=True)

input_movies=input("Enter Your favourite movies saperated by Comma : ")
m_list=input_movies.split(',')
print("Looking for similer movies................\n\n")
recommendations=get_sorted_recommendations(m_list)
print("Movies you might Enjoy (Sorted based on Rotten Tomatoes ratings): ")
print("--------------------------------------------")
for m in recommendations:
    print(m)
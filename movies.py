import requests
import json
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_movies_from_tastedive(name):
    baseurl="https://tastedive.com/api/similar"
    params={'q':name,'type':'moives', 'limit':10}
    response=requests.get(baseurl,params)
    return response.json()

def extract_movie_titles(suggestions):
    similar_movies=list()
    for i in suggestions['Similar']['Results']:
        similar_movies.append(i['Name'])
    return (similar_movies)

extract_movie_titles(get_movies_from_tastedive("Tony Bennett"))
print(extract_movie_titles(get_movies_from_tastedive("Black Panther")))

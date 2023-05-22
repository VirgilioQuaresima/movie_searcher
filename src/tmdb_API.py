import requests
from dotenv import load_dotenv
import os


load_dotenv('.env')
API_KEY = os.environ.get('TMDB_KEY')
PREFIX_URL = 'https://api.themoviedb.org/3'


def search_movie(query: str) -> list:
    url = f"{PREFIX_URL}/search/movie?api_key={API_KEY}&query={query}&language=it-IT&region=IT"
    response = requests.get(url=url)
    response = dict(response.json())
    return response.get('results')


def search_tv(query: str) -> list:
    url = f"{PREFIX_URL}/search/tv?api_key={API_KEY}&query={query}&language=it-IT&region=IT"
    response = requests.get(url=url)
    response = dict(response.json())
    return response.get('results')


def retrive_provider(result_id: int, result_type: str):
    url = f"{PREFIX_URL}/{result_type}/{result_id}/watch/providers?api_key={API_KEY}"
    response = requests.get(url=url)
    response = dict(response.json())
    if not response['results'].get('IT'):
        return []
    flat=dict(response['results']['IT']).get('flatrate') or []
    buy=dict(response['results']['IT']).get('buy') or []
    rent=dict(response['results']['IT']).get('rent') or []
    lista_final=flat+buy+rent
    return lista_final

def transform_date(original_date: str) -> str:
    ''''''
    if not original_date:
        return None
    try:
        splitted = original_date.split('-')
        return f"{splitted[2]}/{splitted[1]}/{splitted[0]}"
    except:
        return original_date


def transform_movies_datas(movies: list) -> list:
    return [
        {
            'title': movie.get('title'),
            'id': movie.get('id'),
            'release_date': transform_date(movie.get('release_date')),
            'popularity': movie.get('popularity'),
            'type': 'movie'
        } for movie in movies
    ]


def transform_tv_series_datas(series: list) -> list:
    return [
        {
            'name': serie.get('name'),
            'id': serie.get('id'),
            'release_date': transform_date(serie.get('release_date')),
            'popularity': serie.get('popularity'),
            'type': 'tv'
        } for serie in series
    ]


def transform_providers_datas(providers: list) -> list:
    print(providers)
    with open('providers_urls.csv', 'r') as f:
        lines = f.readlines()
    d = dict()
    for line in lines:
        provider_data = line.split(',')
        d[provider_data[0]] = provider_data[1].split('\n')[0]
    providers_list = []
    for provider in providers:
        providers_list.append({'name': provider.get(
            'provider_name'), 'url': d.get(provider['provider_name'].lower())})
    return providers_list


def print_json_file(body) -> None:
    import json
    with open('results.json', 'w') as f:
        json.dump(body, f, indent=4)


def search_all(query: str) -> list:
    lists = transform_movies_datas(search_movie(
        query))+transform_tv_series_datas(search_tv(query))
    return sorted(lists, key=lambda x: x['popularity'], reverse=True)


def get_providers(id: int, type: str = 'movie'):
    return transform_providers_datas(retrive_provider(id, type))


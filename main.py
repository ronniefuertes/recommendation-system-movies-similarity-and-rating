"""API para extraer información de la base de datos de películas"""

from fastapi import FastAPI
from api.utils.helpers import count_movies_released_month
from api.utils.helpers import count_movies_released_day
from api.utils.helpers import movie_popularity
from api.utils.helpers import movie_vote
from api.utils.helpers import actor_info
from api.utils.helpers import director_info

app_description = """
        Los títulos de películas, los nombres de actores y directores deben ir separados por '-'.
        No importa si está en mayusculas o minusculas, o si la vocal posee tilde.
        """

app = FastAPI(title="Extracción de información de peliculas",description=app_description)

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    """
    Ingresa el nombre del mes para ver la cantidad de peliculas que se han estrenado historicamente.
    El nombre del mes debe de ser en español.
    No importa si está en mayusculas o minusculas, o si la vocal posee tilde.
    """
    cantidad = count_movies_released_month(mes)
    return {'mes': mes, 'cantidad': cantidad}


@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia:str):
    """
    Ingresa el nombre del día para ver la cantidad de peliculas que se han estrenado historicamente.
    El nombre de ser en español.
    No importa si está en mayusculas o minusculas, o si la vocal posee tilde.
    """
    cantidad = count_movies_released_day(dia)
    return {'dia':dia, 'cantidad': cantidad}


@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    """
    Ingresa el título de una filmación para ver el año de estreno y su calificación.
    Los espacios en el título de la película deben ser reemplazados por '-'.
    No importa si está en mayusculas o minusculas, o si la vocal posee tilde.
    """
    info = movie_popularity(titulo)
    return {'titulo':info["title"], 'anio':info["year"], 'popularidad':info["popularity"]}


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    """
    Ingresa el título de una filmación para ver la cantidad de votos y el valor promedio de las votaciones.
    Si la cantidad de votos es menor a 2000, aparece un mensaje avisando que no cumple esta condición.
    
    Los espacios en el título de la película deben ser reemplazados por '-'.
    No importa si está en mayusculas o minusculas, o si la vocal posee tilde.
    """
    info = movie_vote(titulo)
    return {'titulo':info["title"], 'anio':info["year"], 'voto_total':info["vote_total"], 
            'voto_promedio':info["vote_average"]}

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    """
    Ingresa el nombre de un actor para ver el éxito de él medido a través del retorno.
    Adicional, se muestra la cantidad de películas que en las que ha participado y el promedio de retorno.

    Los espacios en el nombre del actor deben ser reemplazados por '-'.
    No importa si está en mayusculas o minusculas, o si la vocal posee tilde.

    """
    info = actor_info(nombre_actor)
    return {'actor':info["name"], 'cantidad_filmaciones':info["movies_total"], 'retorno_total':info["return_total"], 
            'retorno_promedio':info["return_average"]}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    """
    Ingresa el nombre de un director para ver el éxito de él medido a través del retorno. 
    Adicional, se muestra el nombre de cada película que ha dirigido, su la fecha de lanzamiento, 
        el retorno de cada película, su costo y la ganancia de la misma.

    Los espacios en el nombre del actor deben ser reemplazados por '-'.
    No importa si está en mayusculas o minusculas, o si la vocal posee tilde.
    """
    info = director_info(nombre_director)
    return {'director':info["name"], 'retorno_total_director':info["return_total"], 'peliculas':info["movies_total"], 
            'anio':info["release_date"], 'retorno_pelicula':info["return_movie"], 'budget_pelicula':info["budget_movie"],
            'revenue_pelicula':info["revenue_movie"]}

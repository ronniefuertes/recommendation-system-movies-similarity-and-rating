# Movie Recommendation System

## Installation
The project can be replicated using the `requirements.txt` file.

## Overview
Create a generalized movie recommendation system for each user based on the popularity of the movie. The basic idea behind this recommender is that movies that are more popular and critically acclaimed are more likely to be liked by the average audience.

The process for creating the system involves performing data engineering (data extraction, transformation, loading, and exposing through an API) and then machine learning (EDA, training).

## Data Transformation
The files for data transformation are located in the "data" folder.
The "data_processing.ipynb" file contains a step-by-step guide for data verification and transformations, which utilizes the functions from the "validation.py" file.
The "validation.py" file contains all the functions created for performing the transformations.
The "raw" folder within this directory contains the original unprocessed data.
The following transformations were applied to the data:
- Two files, "movies_dataset.csv" and "credits.csv," were merged using the common field "id."
- Duplicate IDs were checked and removed to avoid providing erroneous information about authors and directors.
- Information from fields such as "belongs_to_collection," "genres," "production_companies," "production_countries," "spoken_languages," "cast," and "crew" was split to utilize it in the API and the recommendation system.
- Null values in the "revenue" and "budget" fields were replaced with 0.
- Null values in the "release_date" field were removed.
- The date format was verified and modified to "YYYY-mm-dd."
- The "release_year" column was created using the year from the release date.
- A new column "return" was created to calculate the return on investment by dividing the "revenue" and "budget" fields. If the data is unavailable, it is set to 0.
- Columns that won't be used such as "video," "imdb_id," "adult," "original_title," "poster_path," and "homepage" were deleted.

## API Development
The API files are located in the "api" folder.
- The "main.py" file contains the API functions.
- The "data" folder stores the document with the transformed movie information.
- The "utils" folder contains the document with the functions created for data extraction.
- The data is exposed using the FastAPI framework. The proposed API endpoints include:
  - `/cantidad_filmaciones_mes/<mes>`: Returns the count of movies released in the specified month.
  - `/cantidad_filmaciones_dia/<dia>`: Returns the count of movies released on the specified day.
  - `/score_titulo/<titulo_de_la_filmación>`: Returns the title, release year, and score for the given movie title.
  - `/votos_titulo/<titulo_de_la_filmación>`: Returns the title, number of votes, and average rating for the given movie title. The movie must have at least 2000 ratings, otherwise, a message indicating the condition is not met will be returned.
  - `/get_actor/<nombre_actor>`: Returns the success of an actor measured through the return value. Additionally, it returns the count of movies the actor has participated in and the average return. The definition excludes directors.
  - `/get_director/<nombre_director>`: Returns the success of a director measured through the return value. It also returns the title of each movie with its release date, individual return, cost, and revenue.
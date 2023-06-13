import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def movie_recommendation(title: str) -> dict:
    """Check for the movie realese and popularity."""

    info = {"movie_recommendations": []}

    movies = pd.read_csv(r"ML_model\data\overview.csv")
    # Get the number of rows in the DataFrame
    num_rows = len(movies)

    # Set the desired number of rows (half of the original)
    desired_num_rows = num_rows // 4

    # Randomly select a subset of rows
    movies = movies.sample(n=desired_num_rows, random_state=2)

    cv=CountVectorizer(max_features=5000, stop_words='english')

    vector=cv.fit_transform(movies['overview'].values.astype('U')).toarray()

    similarity=cosine_similarity(vector)

    #matching_rows = movies[movies['title'] == title]

    # if len(matching_rows) > 0:
    #     movie_index = matching_rows.index[0]
    #     # Further operations using movie_index
    # else:
    #     print("No movie found with the title 'Iron Man'")
    recomendation = []

    distance = sorted(list(enumerate(similarity[2])), reverse=True, key=lambda vector:vector[1])
    for i in distance[0:5]:
        name = movies.iloc[i[0]].title
        recomendation.append(name)
    
    info["movie_recommendations"] = recomendation

    return info


## For future improvement of the system
# def belongs_to_collection(title):
#     """Verify if the movie belongs to a movies series."""
#     title_normalized = normalize_string(title)

#     dataframe = read_movies_data(path1)
    
#     id_movie = []

#     for row in dataframe:
#         movie = row["title"]
#         movie_normalized = normalize_string(movie)

#         if movie_normalized == title_normalized:
#             idx_movie = int(row["id"])
#             id_movie.append(idx_movie)

#     return idx_movie
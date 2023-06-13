import csv
import ast
import os

path12 = "../data/api_data12.csv"
path3 = "../data/api_data3.csv"
path4 = "../data/api_data4.csv"
path5 = "../data/api_data5.csv"
path6 = "../data/api_data6.csv"

def read_movies_data(path):
    """Read and return the movies data as a dataframe."""
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Derive the path to "file.csv" based on the script directory
    csv_path = os.path.join(script_dir, path)

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        dataframe = list(reader)
        return dataframe

def normalize_string(string) -> str:
    """Normalize the text"""
    string = string.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    string = string.replace(" ", "-")
    return string


def convert_month_to_number(month: str) -> int:
    """Convert the month from text to its corresponding number representation."""
    month_dict = {
        "enero":        1,
        "febrero":      2,
        "marzo":        3,
        "abril":        4,
        "mayo":         5,
        "junio":        6,
        "julio":        7,
        "agosto":       8,
        "septiembre":   9,
        "octubre":      10,
        "noviembre":    11,
        "diciembre":    12
    }
    normalized_month = normalize_string(month)
    return month_dict.get(normalized_month)


def convert_day_to_number(day: str) -> int:
    """Convert the month from text to its corresponding number representation."""
    day_dict = {
        "lunes":        1,
        "martes":       2,
        "miercoles":    3,
        "jueves":       4,
        "viernes":      5,
        "sabado":       6,
        "domingo":      7
    }
    normalized_day = normalize_string(day)
    return day_dict.get(normalized_day)


def count_movies_released_month(month: str) -> int:
    """Count the number of movies released historically."""

    month_number = convert_month_to_number(month)

    count = 0

    dataframe = read_movies_data(path12)
    for row in dataframe:
        release_date = row["release_date"].split("-")
        movie_month = int(release_date[1])
        if movie_month == month_number and row["status"] == "Released":
            count += 1

    return count


def count_movies_released_day(day: str) -> int:
    """Count the number of movies released historically."""

    day_number = convert_day_to_number(day)

    count = 0
    dataframe = read_movies_data(path12)
    for row in dataframe:
        release_date = row["release_date"].split("-")
        movie_day = int(release_date[2])
        if movie_day == day_number and row["status"] == "Released":
            count += 1

    return count


def movie_popularity(movie: str) -> dict:
    """Check for the movie realese and popularity."""
    
    movie_name = normalize_string(movie)

    info = {"title": [], "year": [], "popularity": []}

    dataframe = read_movies_data(path3)
    for row in dataframe:
        title = row["title"]
        title_normalized = normalize_string(title)
        
        if title_normalized == movie_name:
            info["title"].append(title)
            info["year"].append(row["release_year"])
            info["popularity"].append(float(row["popularity"]))
    
    return info


def movie_vote(movie: str) -> dict:
    """Check for the vote of the movie movie."""
    
    movie_name = normalize_string(movie)

    info = {"title": [], "year": [], "vote_total": [], "vote_average": []}

    dataframe = read_movies_data(path4)
    for row in dataframe:
        title = row["title"]
        title_normalized = normalize_string(title)
        
        if title_normalized == movie_name:
            info["title"].append(title)
            info["year"].append(row["release_year"])
            info["vote_total"].append(float(row["vote_count"]))
            
            if float(row["vote_count"]) >= 2000:
                info["vote_average"].append(row["vote_average"])
            else:
                info["vote_average"].append("La filmación posee menos de 2000 valoraciones")
    
    return info


def actor_info(actor: str) -> dict:
    """Check information of the actor."""
    
    actor_name = normalize_string(actor)

    info = {"name": [], "movies_total": [], "return_total": [], "return_average": []}
    movies_acted = []
    return_total = 0

    dataframe = read_movies_data(path5)
    for row in dataframe:
        actors_list = ast.literal_eval(row["actor_name"])
        for actor_in_list in actors_list:
            actor_normalized = normalize_string(actor_in_list)
            if actor_normalized == actor_name:
                info["name"] = actor_in_list
                movies_acted.append(row["id"])
                return_total += float(row["return"])
    
    
    movie_count = len(movies_acted)
    return_average = return_total/movie_count
    
    info["movies_total"] = movie_count
    info["return_total"] = return_total
    info["return_average"] = return_average
    
    return info


def director_info(director: str) -> dict:
    """Check information of the director."""
    
    director_name = normalize_string(director)

    info = {"name": [], "return_total": [], "movies_total": [], "release_date": [],
            "return_movie": [], "budget_movie": [], "revenue_movie": []}

    return_total = 0
    movies_directed = []
    movie_date = []
    movie_return = []
    movie_budget = []
    movie_revenue = []

    dataframe = read_movies_data(path6)

    for row in dataframe:
        directors_list = ast.literal_eval(row["crew_name"])
        
        for idx_director, director_in_list in enumerate(directors_list):
            director_normalized = normalize_string(director_in_list)
            
            if director_normalized == director_name:
                departments = ast.literal_eval(row["crew_job"])
                
                if departments[idx_director] == "Director":
                    info["name"] = director_in_list
                    return_total += float(row["return"])
                    movies_directed.append(row["title"])
                    movie_date.append(row["release_date"])
                    movie_return.append(row["return"])
                    movie_budget.append(row["budget"])
                    movie_revenue.append(row["revenue"])

    info["return_total"] = return_total
    info["movies_total"] = movies_directed
    info["release_date"] = movie_date
    info["return_movie"] = movie_return
    info["budget_movie"] = movie_budget
    info["revenue_movie"] = movie_revenue
    
    return info
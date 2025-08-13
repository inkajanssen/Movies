import json


def get_movies():
    """
    Returns a list of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 
    """

    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)

    return data


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """

    with open("data.json", "w") as fileobj:
        json.dump(movies, fileobj)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """

    data = get_movies()
    new_entry = {'Title': title, 'Rating': rating, 'Year': year}
    data.append(new_entry)

    with open("data.json", "w") as fileobj:
        json.dump(data, fileobj)


def delete_movie(movie):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """

    data = get_movies()
    data.remove(movie)

    with open("data.json", "w") as fileobj:
        json.dump(data, fileobj)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """

    data = get_movies()
    for movie in data:
        if title == movie['Title']:
            movie['Rating'] = rating

    with open("data.json", "w") as fileobj:
        json.dump(data, fileobj)

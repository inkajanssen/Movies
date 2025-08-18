import random
from datetime import datetime

import matplotlib.pyplot as plt
from colorama import Fore
from fuzzywuzzy import fuzz

from storage import *
from api import *
from web import *

START_RATING = 0
END_RATING = 10.0
START_YEAR = 0
END_YEAR = datetime.now().year


def print_menu():
    """
    Prints the menu
    :return:
    """

    print(Fore.CYAN + """
    ********** My Movies Database **********
    Menu:
    0.  Exit
    1.  List movies
    2.  Add movie
    3.  Delete movie
    4.  Update movie
    5.  Stats
    6.  Random movie
    7.  Search movie
    8.  Movies sorted by rating
    9.  Movies sorted by year
    10. Filter movie
    11. Create Rating Histogram
    12. Generate Website
    
    Enter choice (0-12): 
    """)


def validate_title(movies):
    """
    Validate the input title
    :return:
    """

    while True:
        name_movie = input(Fore.GREEN + "Please enter the name of the movie to add:")

        if any(movie['Title'] == name_movie for movie in movies):
            print(
                Fore.RED + f"Movie {name_movie} is already in the list. "
                           f"Please enter another name or use update: (q to quit)")
        elif name_movie == "":
            print(Fore.RED + f"You entered an empty string. "
                             f"Please enter another name.")

        else:
            break
    return name_movie


def validate_rating():
    """
    Validate the input rating
    :return:
    """

    while True:
        new_rating = input(Fore.GREEN + "Please enter your rating:")
        try:
            new_rating = float(new_rating)
        except ValueError:
            print(Fore.RED + f"Please enter a number between"
                             f" {START_RATING} and {END_RATING}.")

        if START_RATING <= new_rating <= END_RATING:
            return new_rating

        print(Fore.RED + f"Your input {new_rating} was invalid.Please enter"
                         f"a number between {START_RATING} and {END_RATING}.")


def validate_year():
    """
    Validate the input year
    :return:
    """

    while True:
        new_year = input(Fore.GREEN + "Please enter your year:")
        try:
            new_year = int(new_year)
        except ValueError:
            print(Fore.RED + f"Please enter just a number between"
                             f" {START_YEAR} and {END_YEAR}.")

        if START_YEAR <= new_year <= END_YEAR:
            print(END_YEAR)
            return new_year

        print(Fore.RED + f"Your input {new_year} was invalid. Please enter"
                         f" a number between {START_YEAR} and {END_YEAR}.")

def fetch_movie_infos(title:str, movies:list):
    """
    Searches the movie in OMDb API, and fetches the following parameters:
    Title, Year, Rating, Poster Image URL
    Because searching with incomplete title is possible and the API gives
    back a random movie a question is added for confirmation of the user
    :return: Title, Year, Rating, Poster Image URL
    """

    movie_info = get_info_from_api(title)

    if movie_info.get("Response") == "False":
        print(Fore.RED + "Your movie could not be found. "
                         "Please try again.")
        return "retry"

    title = movie_info.get("Title")
    response = input(Fore.GREEN +
                     f"Is this ({title}) the movie you want to add?"
                                  " (y for yes, n for no)")

    if response.lower() == "y":
        year = movie_info.get("Year")
        rating = movie_info.get("imdbRating")
        poster_url = movie_info.get("Poster")
        movie_data = title, year, rating, poster_url
        return movie_data
    else:
        return "retry"


def validate_ranking():
    """
    Validate the input if it should be reverse or not
    :return:
    """

    while True:
        ranking = input(Fore.GREEN + "Do you want to see the latest movies "
                                     "first or last('f' or 'l': ").lower()

        if ranking in ('f', 'l'):
            ranking = (ranking == "f")
            break
        else:
            print(Fore.RED + "Please enter f or l: ")

    return ranking


def print_movies(movies: list):
    """
    Print the total number of movies as well as each movie in an extra line
    :param movies:
    :return:
    """

    print(Fore.BLUE + f"There are {len(movies)} movies in total")
    for movie in movies:
        print(Fore.BLUE + f"{movie['Title']} ({movie['Year']}): {movie['Rating']}")


def adds_movie(movies: list):
    """
    Add another entry to the dict
    Ask for movie name
    Fetch information from API
    :param movies:
    :return:
    """

    while True:
        name_movie = validate_title(movies)

        if name_movie == 'q':
            return None

        movie_data = fetch_movie_infos(name_movie, movies)
        if movie_data == "retry":
            continue

        title, year, rating, poster_url = movie_data
        add_movie(title, year, rating, poster_url)
        print(Fore.BLUE + f"Movie {title} successfully added!")
        return None


def deletes_movie(movies: list):
    """
    Delete an entry if it exists in movies
    Saves the changes to a file
    :param movies:
    :return:
    """

    name_movie = input(Fore.GREEN + "Please enter the movie name to delete:")
    for movie in movies:
        if name_movie == movie['Title']:
            delete_movie(movie['Title'])
            print(Fore.BLUE + f"Movie {name_movie} successfully deleted!")
            return None

    print(Fore.RED + f"Movie {name_movie} doesn't exist!")
    return None


def updates_movie(movies: list):
    """
    Update a movies ranking if it exists
    Saves the update to a file
    :param movies:
    :return:
    """

    name_movie = input(Fore.GREEN +
                       "Please enter the movie name to update:")

    for movie in movies:
        if name_movie == movie['Title']:
            new_rating = validate_rating()
            update_movie(name_movie, new_rating)
            print(Fore.BLUE +
                  f"Movie {name_movie} successfully updated!")
            return None

    print(Fore.RED + f"Movie {name_movie} doesn't exist!")
    return None


def stats_movie(movies: list):
    """
    Print Stats about the dictionary like Average, Median, Best, Worst
    Limit the display of the calculated stats to 1f
    :param movies:
    :return:
    """

    ratings = [movie['Rating'] for movie in movies]

    # Average
    average = sum(ratings) / len(movies)
    print(Fore.BLUE + f"Average rating: {average:.1f}")

    # Median
    s_values = sorted(ratings)
    lengths = len(movies)
    if lengths % 2 == 0:
        print(Fore.BLUE + f"Median rating: "
                          f"{((s_values[lengths // 2 - 1] + s_values[lengths // 2]) / 2):.1f}")
    else:
        print(Fore.BLUE + f"Median rating: {(s_values[lengths // 2]):.1f}")

    # Best
    max_value = max(ratings)
    for movie in movies:
        if movie['Rating'] == max_value:
            print(Fore.BLUE + f"Best movie: {movie['Title']},"
                              f" {movie['Rating']}")

    # Worst
    min_value = min(ratings)
    for movie in movies:
        if movie['Rating'] == min_value:
            print(Fore.BLUE + f"Worst movie: {movie['Title']},"
                              f" {movie['Rating']}")


def random_movie(movies: list):
    """
    Give out a random movie
    :param movies:
    :return:
    """

    today_movie = random.choice([movie['Title'] for movie in movies])
    today_rating = next(movie['Rating'] for movie in movies if
                        movie['Title'] == today_movie)

    print(Fore.BLUE + f"Your movie for tonight: {today_movie},"
                      f" it's rated {today_rating}")


def search_movie(movies: list):
    """
    Search for a movie, Case insensitive
    :param movies:
    :return:
    """

    part_search = input(Fore.GREEN + "Please enter part of the movie's name: ")

    match_found = False
    fuzzy_matches = []
    for movie in movies:
        if part_search.lower() in movie['Title'].lower():
            print(Fore.BLUE + f"{movie['Title'], movie['Rating']}")
            match_found = True
        elif fuzz.ratio(part_search.lower(), movie['Title'].lower()) > 50:
            fuzzy_matches.append(movie['Title'])

    if not match_found:
        if fuzzy_matches:
            print(Fore.BLUE + f"The movie {part_search} does not exist."
                              f" Did you mean:")
            for match in fuzzy_matches:
                print(match)
        else:
            print(Fore.RED + "No movies found!")


def ranking_by_rating(movies: list):
    """
    rank the movies by rating descending
    :param movies:
    :return:
    """

    sorted_by_rating = (
        sorted(movies, key=lambda movie: movie['Rating'], reverse=True))
    for value in sorted_by_rating:
        print(Fore.BLUE + f"{value['Title']}: {value['Rating']}")


def ranking_by_year(movies: list):
    """
    Rank the movies by year
    Ask if the user wants to see the latest movies first or last
    :param movies:
    :return:
    """

    ranking = validate_ranking()

    sorted_by_year = sorted(movies, key=lambda movie: movie['Year'],
                            reverse=ranking)

    for value in sorted_by_year:
        print(Fore.BLUE + f"{value['Year']}: {value['Title']}")


def filter_movies(movies: list):
    """
    Filter a list of movies based on specific criteria
    such as minimum rating, start year, and end year
    :param movies:
    :return:
    """

    rating = input("Enter minimum rating (leave blank for no "
                         "minimum rating):")
    try:
        rating = float(rating) if rating else START_RATING
    except ValueError:
        print(Fore.RED + "Invalid rating. Using Start Rating.")

    start_year = input("Enter start year (leave blank for no "
                           "start year):")
    try:
        start_year = int(start_year) if start_year else START_YEAR
    except ValueError:
        print(Fore.RED + "Invalid starting year. Using default start year.")
        start_year = START_YEAR

    end_year = input("Enter end year (leave blank for no end year): ")
    try:
        end_year = int(end_year) if end_year else END_YEAR
    except ValueError:
        print(Fore.RED + "Invalid end year. Using default end year.")
        end_year = END_YEAR

    filtered_movies = []
    for movie in movies:
        if (start_year <= movie.get('Year') <= end_year and
                movie.get('Rating') >= rating):
            filtered_movies.append(movie)

    found_movies= sorted(filtered_movies,
                         key=lambda k:( movie['Year'], movie['Rating']))

    if not found_movies:
        print(Fore.BLUE + "No movies were found")
    else:
        for movie in found_movies:
            print(Fore.BLUE +
                  f"{movie['Title']} ({movie['Year']}): {movie['Rating']}")


def histogram(movies: list):
    """
    Create a histogram of the ratings of the movies
    :param movies:
    :return:
    """

    hist_list = [movie['Rating'] for movie in movies]
    plt.hist(hist_list, bins=40, color='skyblue', edgecolor='black')

    plt.title('Rating of Movies')
    plt.xlabel('Ratings')
    plt.ylabel('Frequencies')

    name = input(Fore.GREEN + "Please enter a name for the histogram:")
    plt.savefig(f"{name}.png")

    plt.show()


def generate_website(movies: list):
    """
    Read the html template
    Create a new html file with output data
    :param movies:
    :return:
    """
    html_content = load_html("web/index_template.html")

    replace_info = display_movie_info(html_content, movies)

    save_html("web/index.html", replace_info)
    print(Fore.GREEN + "Website was successfully generated"
                       " to the file index.html.")


def pause():
    """
    Give the user a pause to read output and then print menu again
    :return:
    """
    input(Fore.CYAN + "Press Enter to continue...")


def main():
    """
    Get the input of the user and match it to one of the functions.
    The data is stored in an extra db for persistent storage
    :return:
    """

    # Dictionary to get functions
    menu_functions = {
        1: print_movies,
        2: adds_movie,
        3: deletes_movie,
        4: updates_movie,
        5: stats_movie,
        6: random_movie,
        7: search_movie,
        8: ranking_by_rating,
        9: ranking_by_year,
        10: filter_movies,
        11: histogram,
        12: generate_website
    }

    while True:
        print_menu()

        try:
            option = int(input())

            if option == 0:
                print("Bye!")
                return False
            if option in menu_functions:
                menu_functions[option](list_movies())
                pause()
            else:
                print(Fore.RED + "Wrong input")
                pause()

        except ValueError:
            print(Fore.RED + "The option should only be a number")
            pause()


if __name__ == "__main__":
    main()

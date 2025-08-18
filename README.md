# Movies

Movies is an application which stores Movies in a SQL DB with CRUD and analytics.
It also provides getting information about a movie via an API and generates a website.

## Installation

All required imports are listed in the requirements.txt.

## Run

1. To start with a new DB, delete movies.db, its just an example what the DB looks like.
2. For the API you need a API Key from [OMDb](https://www.omdbapi.com/)
3. Create an .env in api and add you API Key like this: API_KEY={your API Key} 
4. Run the movies.py file

## Features

    1.  List movies - list all movies in the DB
    2.  Add movie
    3.  Delete movie 
    4.  Update movie 
    5.  Stats - print Stats about your movies (Average, Median, Best, Worst)
    6.  Random movie 
    7.  Search movie 
    8.  Movies sorted by rating
    9.  Movies sorted by year
    10. Filter movie
    11. Create Rating Histogram
    12. Generate Website 

## Roadmap

* [ ] User Profiles
* [ ] Adding Notes
* [ ] Add Rating to Website
* [ ] Add IMDB Link
* [ ] Add Country Flag

## Additional Information
In storage there are two different options to store your data: in a JSON file and in a SQL SB.
The current version works with a SQL DB.
Movies.db, data.json in storage and index.html are examples of what the corresponding storage and website look like.
from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()


def list_movies():
    """
    Retrieve all movies from the database.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    # {row[0]: {"year": row[1], "rating": row[2]} for row in movies}
    return [{"Title": row[0], "Year": row[1], "Rating": row[2]} for row in movies]


def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (Title, Year, Rating) VALUES (:Title, :Year, :Rating)"),
                               {"Title": title, "Year": year, "Rating": rating})
            connection.commit()
            # print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :Title"),
                               {"Title": title})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """
    Update a movie's rating in the database.
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :Rating WHERE title = :Title"),
                               {"Title": title, "Rating": rating})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")

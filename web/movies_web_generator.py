def load_html(file_path):
    """Load the content of an HTML file"""

    with open(file_path, "r", encoding='utf-8') as handle:
        return handle.read()


def save_html(file_path, content):
    """Save the content to an HTML file"""

    with open(file_path, "w", encoding='utf-8') as handle:
        return handle.write(content)


def collect_movie_info(data:dict):
    """
    Collect the data for every single movie
    :param data:
    :return: The stylized info for every movie
    """
    output = ""
    output += '<li class="movie-grid">'
    output += '<div class="movie">'

    output += ('<img class="movie-poster" '
               f'src={data.get("Poster")}>')

    output += ('<div class="movie-title">'
               + f'{data.get("Title")}'
               + '</div>')

    output += ('<div class="movie-year">'
               + f'{data.get("Year")}'
               + '</div>')

    output += '</div>'
    output += '</li>'

    return output


def display_movie_info(html_content, movie_data:list):
    """
    Collect the stylized information
    :return: The replaced information for the grid
    """
    output = ""

    for data in movie_data:
        output += collect_movie_info(data)

    replace_info = html_content.replace("__TEMPLATE_MOVIE_GRID__", output)

    return replace_info
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_info_from_api(title):
    """
    Get the information from the movie API as JSON
    """
    api_url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={title}'
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return "Error:", response.status_code, response.json()
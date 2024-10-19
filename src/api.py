"""
API module to interact with the Trello API.
"""

import os
import sys
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
from src.constants import TRELLO_API_BASE_URL

load_dotenv()

API_KEY: str = os.getenv('TRELLO_API_KEY')
TOKEN: str = os.getenv('TRELLO_TOKEN')

if not API_KEY or not TOKEN:
    print('Error: Ensure TRELLO_API_KEY and TRELLO_TOKEN are set in environment variables.')
    sys.exit(1)

def trello_get(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """
    Perform GET requests to Trello API.

    Args:
        endpoint (str): The API endpoint to call.
        params (Optional[Dict]): Additional parameters for the API call.

    Returns:
        Dict: JSON response from the API.
    """
    url = f"{TRELLO_API_BASE_URL}/{endpoint}"
    default_params = {'key': API_KEY, 'token': TOKEN}
    if params:
        default_params.update(params)
    response = requests.get(url, params=default_params)
    response.raise_for_status()
    return response.json()

def trello_post(endpoint: str, data: Optional[Dict] = None) -> Dict:
    """
    Helper function to perform POST requests to Trello API.

    Args:
        endpoint (str): The API endpoint to call.
        data (Optional[Dict]): Data to send in the POST request.

    Returns:
        Dict: JSON response from the API.
    """
    url = f"{TRELLO_API_BASE_URL}/{endpoint}"
    default_data = {'key': API_KEY, 'token': TOKEN}
    if data:
        default_data.update(data)
    response = requests.post(url, data=default_data)
    response.raise_for_status()
    return response.json()

def get_boards() -> List[Dict]:
    """
    Retrieve all boards of the user.

    Returns:
        List[Dict]: A list of board objects, each containing 'name' and 'id'.
    """
    return trello_get('members/me/boards', params={'fields': 'name,id'})

def get_lists(board_id: str) -> List[Dict]:
    """
    Retrieve all lists (columns) of a board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        List[Dict]: A list of list objects, each containing 'name' and 'id'.
    """
    return trello_get(f'boards/{board_id}/lists', params={'fields': 'name,id'})

def get_labels(board_id: str) -> List[Dict]:
    """
    Retrieve all labels of a board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        List[Dict]: A list of label objects, each containing 'name', 'color', and 'id'.
    """
    return trello_get(f'boards/{board_id}/labels', params={'fields': 'name,color,id'})

def create_label(board_id: str, name: str, color: Optional[str]) -> Dict:
    """
    Create a new label on a board.

    Args:
        board_id (str): The ID of the board.
        name (str): The name of the new label.
        color (Optional[str]): The color of the new label.

    Returns:
        Dict: The created label object.
    """
    data = {'name': name, 'color': color, 'idBoard': board_id}
    return trello_post('labels', data=data)

def create_card(list_id: str, name: str, desc: str, label_ids: str) -> Dict:
    """
    Create a new card in a list (column).

    Args:
        list_id (str): The ID of the list (column) to add the card to.
        name (str): The name of the card.
        desc (str): The description of the card.
        label_ids (str): Comma separated string of label IDs.

    Returns:
        Dict: The created card object.
    """
    data = {'idList': list_id, 'name': name, 'desc': desc}
    if label_ids:
        data['idLabels'] = label_ids
    return trello_post('cards', data=data)

def add_comment(card_id: str, text: str) -> Dict:
    """
    Add a comment to a card.

    Args:
        card_id (str): The ID of the card.
        text (str): The text of the comment.

    Returns:
        Dict: The created comment object.
    """
    data = {'text': text}
    return trello_post(f'cards/{card_id}/actions/comments', data=data)

'''
Unit tests for the API functions.

Use pytest and mock the 'requests' library to simulate API calls.
Each test function sets up a mock response, calls an API function, and
asserts that the function returns the expected data. Simulated responses
are created using MagicMock without making actual network requests.
'''

import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from src.api import get_boards, get_lists, create_card, add_comment

@pytest.fixture
def mock_requests():
    with patch('src.api.requests') as mock_requests:
        yield mock_requests

def test_get_boards(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = [{'id': '1', 'name': 'Test Board'}]
    mock_requests.get.return_value = mock_response

    boards = get_boards()
    assert len(boards) == 1
    assert boards[0]['name'] == 'Test Board'

def test_get_lists(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = [{'id': '1', 'name': 'To Do'}]
    mock_requests.get.return_value = mock_response

    lists = get_lists('board_id')
    assert len(lists) == 1
    assert lists[0]['name'] == 'To Do'

def test_create_card(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = {'id': '1', 'name': 'Test Card'}
    mock_requests.post.return_value = mock_response

    card = create_card('list_id', 'Test Card', 'Description', 'label1,label2')
    assert card['name'] == 'Test Card'

def test_add_comment(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = {'id': '1', 'data': {'text': 'Test Comment'}}
    mock_requests.post.return_value = mock_response

    comment = add_comment('card_id', 'Test Comment')
    assert comment['data']['text'] == 'Test Comment'

"""
CLI tool to add cards to a Trello board.
"""

import sys
import os
# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional, List, Dict, Tuple
import requests
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from constants import VALID_COLORS, MIN_CARD_TITLE_LENGTH
from src.api import get_boards, get_lists, get_labels, create_label, create_card, add_comment

console = Console()

def cli() -> None:
    add_card()

def select_board() -> Optional[str]:
    """
    Select a board from the available boards.

    Returns:
        Optional[str]: The ID of the selected board, or None if no board was selected.
    """
    boards = get_boards()
    if not boards:
        console.print("[bold red]No boards were found.[/bold red]", style="red")
        return None
    board_choices: Dict[str, Dict] = {str(i): board for i, board in enumerate(boards, start=1)}
    board_panel = Panel("\n".join([f"{idx}. {board['name']}" for idx, board in board_choices.items()]), 
                        title="[italic]Select an available board[/italic]", 
                        expand=False)
    console.print(board_panel)
    
    board_selection = Prompt.ask("\nSelect a board", choices=board_choices.keys())
    selected_board = board_choices[board_selection]
    console.print(f"[italic]Selected Board: {selected_board['name']}[/italic]\n", style="green")
    return selected_board['id']

def select_list(board_id: str) -> Optional[str]:
    """
    Select a list from available lists in the board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        Optional[str]: The ID of the selected list, or None if no list was selected.
    """
    lists = get_lists(board_id)
    if not lists:
        console.print(Panel("[bold red]No columns found in this board.[/bold red]"), style="red")
        return None
    list_choices: Dict[str, Dict] = {str(i): lst for i, lst in enumerate(lists, start=1)}
    list_panel = Panel("\n".join([f"{idx}. {lst['name']}" for idx, lst in list_choices.items()]), 
                       title="[italic]Select an available column[/italic]", 
                       expand=False)
    console.print(list_panel)
    
    list_selection = Prompt.ask("\nSelect a column", choices=list_choices.keys())
    selected_list = list_choices[list_selection]
    console.print(f"[italic]Selected Column: {selected_list['name']}[/italic]\n", style="green")
    return selected_list['id']

def get_card_details() -> Tuple[str, str]:
    """
    Get card title and description from the user.

    Returns:
        Tuple[str, str]: A tuple containing the card title and description.
    """
    console.print("[bold]Add Card Details[/bold]")
    card_title = Prompt.ask("Enter card title")
    while len(card_title.strip()) < MIN_CARD_TITLE_LENGTH:
        console.print(Panel(f"[bold red]Card title must be at least {MIN_CARD_TITLE_LENGTH} characters long.[/bold red]"), style="red")
        card_title = Prompt.ask("Enter card title")
    card_desc = Prompt.ask("Enter card description (optional)", default="")
    return card_title, card_desc

def select_labels(board_id: str) -> List[str]:
    """
    Select or create labels for the card.

    Args:
        board_id (str): The ID of the board.

    Returns:
        List[str]: A list of selected label IDs.
    """
    labels = get_labels(board_id)
    label_choices: Dict[str, Dict] = {str(i): label for i, label in enumerate(labels, start=1)}
    selected_label_ids: List[str] = []

    while True:
        console.print("\n")
        label_options = create_label_options(label_choices)
        label_panel = Panel(
            label_options,
            title="[italic]Select available labels[/italic]",
            expand=False
        )
        console.print(label_panel)
        
        label_selection = Prompt.ask("\nSelect a label (or 'F' to finish)", default="F")
        
        if label_selection.upper() == 'F':
            break
        
        if label_selection == '0':
            new_label = create_new_label(board_id)
            selected_label_ids.append(new_label['id'])
            label_choices[str(len(label_choices) + 1)] = new_label
        elif label_selection in label_choices:
            selected_label_ids.append(label_choices[label_selection]['id'])
            console.print(f"\n[italic]{len(selected_label_ids)} label(s) selected.[/italic]\n", style="green")
        else:
            console.print(f"Invalid selection: {label_selection}", style="red")

    return selected_label_ids

def create_label_options(label_choices: Dict[str, Dict]) -> str:
    options = []
    for idx, label in label_choices.items():
        name = label['name'] if label['name'] else 'No Name'
        color = label['color'] if label['color'] else 'No Color'
        options.append(f"{idx}. {name} ({color})")
    
    options.append("0. Create a new label")
    options.append("F. Finish selecting labels")
    
    return "\n".join(options)

def create_new_label(board_id: str) -> Dict:
    """
    Create a new label.

    Args:
        board_id (str): The ID of the board.

    Returns:
        Dict: The created label object.
    """
    label_name = Prompt.ask("Enter new label name")
    while not label_name.strip():
        console.print(Panel("[bold red]Label name cannot be empty.[/bold red]"), style="red")
        label_name = Prompt.ask("Enter new label name")
    label_color = Prompt.ask(
        "Enter label color",
        choices=VALID_COLORS,
        default='blue'
    )
    new_label = create_label(board_id, label_name, None if label_color == 'null' else label_color)
    console.print(f"\n[italic]New label '{label_name}' created.[/italic]\n", style="green")
    return new_label

def add_card() -> None:
    """Add a card to a Trello board."""
    while True:
        try:
            console.print("\n")
            board_id = select_board()
            if not board_id:
                if not Confirm.ask("\nNo board selected. Do you want to try again?", default=True):
                    break
                continue

            list_id = select_list(board_id)
            if not list_id:
                if not Confirm.ask("\nNo list selected. Do you want to try again?", default=True):
                    break
                continue

            card_title, card_desc = get_card_details()
            selected_label_ids = select_labels(board_id)

            if not selected_label_ids:
                console.print("[italic]No labels selected.[/italic]\n", style="blue")
            else:
                console.print(f"[italic]{len(selected_label_ids)} label(s) selected.[/italic]\n", style="green")

            card = create_card(list_id, card_title, card_desc, ','.join(selected_label_ids))

            add_comment_option = Confirm.ask("\nDo you want to add a comment?", default=False)
            if add_comment_option:
                comment_text = Prompt.ask("Enter your comment")
                add_comment(card['id'], comment_text)
                console.print("\n[italic]Comment added to the card.[/italic]\n", style="green")

            console.print(f"[italic]Card '{card_title}' was successfully added.[/italic]\n", style="green")

            if not Confirm.ask("\nDo you want to add another card?", default=False):
                break

        except requests.HTTPError as http_err:
            console.print("[bold red]HTTP error occurred. Please check your API key and token.[/bold red]", style="red")
            console.print(f"Error details: {http_err}", style="red")
            if not Confirm.ask("\nDo you want to try again?", default=True):
                break
        except Exception as err:
            console.print(f"[bold red]An error occurred: {err}[/bold red]", style="red")
            if not Confirm.ask("\nDo you want to try again?", default=True):
                break

if __name__ == '__main__':
    cli()

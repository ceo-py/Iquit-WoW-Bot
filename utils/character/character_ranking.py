from settings import RAIDER_IO_BASE_URL_FOR_CHARACTER
from utils.super_scripts_text import generate_superscript_numbers
from settings import CHARACTER_ROLES


def filter_and_sort_characters_by_role(characters: list, role: str) -> list:
    """
    Filter and sort Characters based on the specified role.

    Args:
        Characters (list): List of Characters objects to be filtered and sorted.
        role (str): Role to filter and sort by. Choices are:
            - "total": Filter and sort by total rating
            - "dps": Filter and sort by DPS rating
            - "heal": Filter and sort by healer rating
            - "tank": Filter and sort by tank rating
            If an invalid role is provided, filtering and sorting will default to total rating.

    Returns:
        list: Filtered and sorted list of rank objects based on the specified role.
    """
    return sorted(
        [
            char
            for char in characters
            if getattr(char, CHARACTER_ROLES.get(role, "total_rating")) > 0
        ],
        key=lambda x: (-getattr(x, CHARACTER_ROLES.get(role, "total_rating")), x.name),
    )


def format_ranks_for_embed(characters: list, role: str, positions: int) -> str:
    """
    Format ranks for embed based on the specified role and number of positions.

    Args:
        characters (list): List of Characters objects to be formatted.
        role (str): Role to sort by. Choices are:
            - "total": Sort by total rating
            - "dps": Sort by DPS rating
            - "heal": Sort by healer rating
            - "tank": Sort by tank rating
            If an invalid role is provided, sorting will default to total rating.
        positions (int): Number of top positions to include in the formatted output.

    Returns:
        str: Formatted string of rank objects based on the specified role and positions.
    """
    output = [f"{x}. n/a" for x in range(1, positions + 1)]
    sorted_characters = filter_and_sort_characters_by_role(characters, role)

    for pos, character in enumerate(sorted_characters[:positions]):
        rating = generate_superscript_numbers(
            getattr(character, CHARACTER_ROLES.get(role, "total_rating"))
        )
        output[pos] = (
            f"[{pos + 1}.{character.name.capitalize()} {rating}]({RAIDER_IO_BASE_URL_FOR_CHARACTER}"
            f"/{character.region}/{character.realm}/{character.name})"
        )

    return output

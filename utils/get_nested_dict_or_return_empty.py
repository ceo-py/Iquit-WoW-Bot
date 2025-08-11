from typing import Any, Dict, List, Union


def get_nested_dict_or_return_empty(
    source: Dict[str, Any], key: str, default: Union[List[Dict], List[Any]] = None
) -> Dict[str, Any]:
    """
    Safely retrieves the first dictionary from a list stored under a given key in a source dictionary.
    If the key is missing or the list is empty, returns an empty dictionary.

    Args:
        source (Dict[str, Any]): The dictionary to search.
        key (str): The key whose value should be a list of dictionaries.
        default (Union[List[Dict], List[Any]], optional): The default value to use if the key is missing. Defaults to [{}].

    Returns:
        Dict[str, Any]: The first dictionary in the list, or an empty dictionary if not found.
    """
    if not isinstance(source, dict):
        raise TypeError(f"source must be a dict, got {type(source).__name__}")
    if not isinstance(key, str):
        raise TypeError(f"key must be a str, got {type(key).__name__}")

    if default is None:
        default = [{}]

    value = source.get(key, default)
    if isinstance(value, list) and value:
        first_item = value[0]
        if isinstance(first_item, dict):
            return first_item
    return {}

TYPES = {
    "total": "total_rating",
    "dps": "dps_rating",
    "heal": "healer_rating",
    "tank": "tank_rating",
}


def sort_ranks_base_on_role(ranks: list, role: str) -> list:
    return sorted(
        ranks, key=lambda x: (-getattr(x, TYPES.get(role, "total_rating")), x.name)
    )

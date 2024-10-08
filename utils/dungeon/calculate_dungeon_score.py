# reference https://mythicplanner.com/

BASE_SCORES = {
    2: 165,
    3: 180,
    4: 205,
    5: 220,
    6: 235,
    7: 265,
    8: 280,
    9: 295,
    10: 320,
    11: 335,
    12: 365,
    13: 380,
    14: 395,
    15: 410,
    16: 425,
    17: 440,
    18: 455,
    19: 470,
    20: 485,
}


def calculate_on_time_rating(base_score: int, pt: int) -> float:
    final_rating = base_score + (pt * 37.5)
    return round(final_rating, 1)


def calculate_dungeon_score(key_level: int, t_limit_ms: int, t_run_ms: int) -> float:
    """
    Calculate rating for dungeon.

    :param key_level: Key level of the dungeon (2 to 20)
    :param t_limit_ms: Dungeon time limit (in milliseconds)
    :param t_run_ms: Your dungeon run time (in milliseconds)
    :return: The final rating for the dungeon run
    """
    if key_level < 2 or key_level > 20:
        raise ValueError("Key level must be between 2 and 20.")

    base_score = BASE_SCORES[key_level]
    pt = (t_limit_ms - t_run_ms) / t_limit_ms

    return (
        calculate_on_time_rating(base_score, pt)
        if t_limit_ms >= t_run_ms
        else calculate_over_time_rating(base_score, pt)
    )


def calculate_over_time_rating(base_score: int, pt: int) -> float:
    final_rating = base_score + (pt * 37.5) - 15

    if pt <= -0.40:
        final_rating = 0

    return round(final_rating, 1)

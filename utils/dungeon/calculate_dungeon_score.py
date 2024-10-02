# Dictionary for base scores for key levels 2 to 20
BASE_SCORES = {
    2: 165, 3: 180, 4: 205, 5: 220, 6: 235, 7: 265, 8: 280, 9: 295, 10: 320,
    11: 335, 12: 365, 13: 380, 14: 395, 15: 410, 16: 425, 17: 440, 18: 455, 19: 470, 20: 485
}

# Function to calculate rating when the dungeon is completed on time or ahead of time
def calculate_on_time_rating(key_level, t_limit_ms, t_run_ms):
    """
    Calculate rating for an on-time run or completed before the time limit.
    
    :param key_level: Key level of the dungeon (2 to 20)
    :param t_limit_ms: Dungeon time limit (in milliseconds)
    :param t_run_ms: Your dungeon run time (in milliseconds)
    :return: The final rating for the dungeon run
    """
    if key_level < 2 or key_level > 20:
        raise ValueError("Key level must be between 2 and 20.")
    
    # Fetch the base score for the given key level
    base_score = BASE_SCORES[key_level]
    
    # Calculate time percentage PT
    pt = (t_limit_ms - t_run_ms) / t_limit_ms
    
    # Cap PT at 40%
    pt = min(pt, 0.40)
    
    # Calculate the final rating using the formula
    final_rating = base_score + (pt * 37.5)
    
    return round(final_rating, 2)

# Function to calculate rating when the dungeon is completed over the time limit
def calculate_over_time_rating(key_level, t_limit_ms, t_run_ms):
    """
    Calculate rating for an over-time run.
    
    :param key_level: Key level of the dungeon (2 to 20)
    :param t_limit_ms: Dungeon time limit (in milliseconds)
    :param t_run_ms: Your dungeon run time (in milliseconds)
    :return: The final rating for the dungeon run
    """
    if key_level < 2 or key_level > 20:
        raise ValueError("Key level must be between 2 and 20.")
    
    # Fetch the base score for the given key level
    base_score = BASE_SCORES[key_level]
    
    # Calculate time percentage PT (it will be negative since over time)
    pt = (t_limit_ms - t_run_ms) / t_limit_ms
    
    # Cap PT at -40% if it's too much over time
    pt = max(pt, -0.40)
    
    # Calculate the final rating using the overtime formula (subtracting 15 points from the base)
    final_rating = base_score + (pt * 37.5) - 15
    
    # If PT is more than 40% over the limit, the run gets 0 rating
    if pt <= -0.40:
        final_rating = 0
    
    return round(final_rating, 2)

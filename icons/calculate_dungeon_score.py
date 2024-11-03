import math

# Data
DungeonAbbreviations = {
    375: "mots",
    376: "nw",
    377: "dos",
    378: "hoa",
    379: "pf",
    380: "sd",
    381: "soa",
    382: "top",
    391: "strt",
    392: "gmbt",
}

DungeonBaseScores = [0, 40, 45, 55, 60, 65, 75, 80, 85, 100]

TimerConstants = {"Threshold": 0.4, "MaxModifier": 5, "DepletionPunishment": 5}


# Math Functions
def round(num):
    return math.floor(num + 0.5) if num >= 0 else math.ceil(num - 0.5)


def format_number(num, precision, no_prefix=False):
    if num is None:
        return "nil"
    format_string = f"{{:.{precision}f}}"
    absolut_value_string = format_string.format(num)
    if no_prefix:
        return absolut_value_string
    else:
        return ("+" if num > 0 else "") + absolut_value_string


def pad_string(s, length):
    result = str(s)
    while len(result) < length:
        result = " " + result
    return result


# WoW Functions
def compute_time_modifier(par_time_percentage):
    percentage_offset = 1 - par_time_percentage
    if percentage_offset > TimerConstants["Threshold"]:
        return TimerConstants["MaxModifier"]
    elif percentage_offset > 0:
        return (
            percentage_offset
            * TimerConstants["MaxModifier"]
            / TimerConstants["Threshold"]
        )
    elif percentage_offset == 0:
        return 0
    elif percentage_offset > -TimerConstants["Threshold"]:
        return (
            percentage_offset
            * TimerConstants["MaxModifier"]
            / TimerConstants["Threshold"]
            - TimerConstants["DepletionPunishment"]
        )
    else:
        return None


def compute_scores(dungeon_id, level, time_in_seconds, par_time):
    base_score = DungeonBaseScores[min(level, 10)] + max(0, level - 10) * 5
    par_time_fraction = time_in_seconds / par_time
    time_score = compute_time_modifier(par_time_fraction)
    format_number(par_time_fraction * 100, 2)
    return {
        "baseScore": base_score,
        "timeScore": base_score + time_score if time_score is not None else 0,
        "timeBonus": time_score,
        "parTimePercentageString": pad_string(
            format_number(par_time_fraction * 100, 2, True), 7
        )
        + "%",
    }


def compute_key_base_score(affix_score_data):
    return affix_score_data["baseScore"] + affix_score_data["timeBonus"]


def compute_affix_score_sum(score1, score2):
    return max(score1, score2) * 1.5 + min(score1, score2) * 0.5


total_score = 0


def build_key_data_string(blizzard_scores, affix_score_data):
    global total_score
    blizzard_tyrannical = blizzard_scores["Tyrannical"]["baseScore"]
    computed_tyrannical = compute_key_base_score(affix_score_data["Tyrannical"])
    blizzard_fortified = blizzard_scores["Fortified"]["baseScore"]
    computed_fortified = compute_key_base_score(affix_score_data["Fortified"])
    computed_key_score = compute_affix_score_sum(
        computed_tyrannical, computed_fortified
    )
    total_score += computed_key_score
    return (
        f"Tyrannical  {pad_string(blizzard_tyrannical, 3)} | {pad_string(round(computed_tyrannical), 3)} = "
        f"{pad_string(affix_score_data['Tyrannical']['baseScore'], 3)}{pad_string(format_number(affix_score_data['Tyrannical']['timeBonus'], 2), 6)}"
        f"{affix_score_data['Tyrannical']['parTimePercentageString']}\n"
        f"Fortified   {pad_string(blizzard_fortified, 3)} | {pad_string(round(computed_fortified), 3)} = "
        f"{pad_string(affix_score_data['Fortified']['baseScore'], 3)}{pad_string(format_number(affix_score_data['Fortified']['timeBonus'], 2), 6)}"
        f"{affix_score_data['Fortified']['parTimePercentageString']}\n"
        f"complete     {pad_string(blizzard_scores['Complete'], 3)} | {pad_string(round(computed_key_score), 3)}"
    )


def compute_tt_enhancement(
    dungeon_id, par_time, blizzard_affix_score_data, blizzard_total_score
):
    computed_affix_score_data = {
        "Tyrannical": {
            "baseScore": 0,
            "timeScore": 0,
            "timeBonus": 0,
            "parTimePercentageString": "   0.00%",
        },
        "Fortified": {
            "baseScore": 0,
            "timeScore": 0,
            "timeBonus": 0,
            "parTimePercentageString": "   0.00%",
        },
    }
    blizzard_scores = {
        "Tyrannical": {"baseScore": 0},
        "Fortified": {"baseScore": 0},
        "Complete": 0,
    }
    if blizzard_affix_score_data is not None:
        for info in blizzard_affix_score_data:
            computed_affix_score_data[info["name"]] = compute_scores(
                dungeon_id, info["level"], info["durationSec"], par_time
            )
            blizzard_scores[info["name"]] = {"baseScore": info["score"]}
    if blizzard_total_score is not None:
        blizzard_scores["Complete"] = blizzard_total_score
    return build_key_data_string(blizzard_scores, computed_affix_score_data)


def print_score_table():
    for dungeon_id, abbreviation in DungeonAbbreviations.items():
        par_time = 1000  # Placeholder for C_ChallengeMode.GetMapUIInfo(dungeon_id)
        blizzard_affix_score_data = [
            {"name": "Tyrannical", "level": 10, "durationSec": 1200, "score": 100},
            {"name": "Fortified", "level": 10, "durationSec": 1300, "score": 90},
        ]  # Placeholder for C_MythicPlus.GetSeasonBestAffixScoreInfoForMap(dungeon_id)
        blizzard_total_score = 190  # Placeholder for C_MythicPlus.GetSeasonBestAffixScoreInfoForMap(dungeon_id)
        print(f"{abbreviation} - Dungeon Name Placeholder")
        print("        Blizzard | Computed")
        print(
            compute_tt_enhancement(
                dungeon_id, par_time, blizzard_affix_score_data, blizzard_total_score
            )
        )
    current_score = 500  # Placeholder for C_ChallengeMode.GetOverallDungeonScore()
    print("========================================")
    print(
        f"Total        {pad_string(current_score, 3)} | {pad_string(round(total_score), 3)}"
    )
    print("========================================")


print_score_table()

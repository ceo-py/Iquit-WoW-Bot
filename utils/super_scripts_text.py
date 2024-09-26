def generate_superscript_numbers(numbers: int) -> str:
    numbers_superscript = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
    }
    return ("").join(numbers_superscript[x] for x in str(numbers))


def generate_superscript_stars(stars: int) -> str:
    stars_superscript = {
        0: "",
        1: "⁺",
        2: "⁺⁺",
        3: "⁺⁺⁺",
    }
    return stars_superscript[stars]

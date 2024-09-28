def convert_dict_k_v_small_letters(dictionary: dict):
    return {k.lower().strip(): str(v).lower().strip() for k, v in dictionary.items()}

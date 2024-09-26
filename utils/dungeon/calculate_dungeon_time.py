def time_difference(par_time: int, clear_time: int) -> float:
    difference = par_time - clear_time
    percentage_difference = abs((difference / clear_time) * 100)

    return round(percentage_difference, 1)


def convert_ms_to_min_sec(milliseconds: int) -> tuple:
    total_seconds = milliseconds / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    return minutes, int(seconds)


def generate_calculated_dungeon_time_message_for_discord(
    clear_time_ms: int, par_time_ms: int
) -> str:
    time_text = "Under" if par_time_ms > clear_time_ms else "Over"
    times_ms = sorted([clear_time_ms, par_time_ms])
    time_difference_percent = time_difference(clear_time_ms, par_time_ms)
    minutes, seconds = convert_ms_to_min_sec(times_ms[-1] - times_ms[0])
    return f"{time_text} by **{minutes}:{seconds:02} ({time_difference_percent}%)**"

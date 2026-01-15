ZERO = 0
LIST_PENULTIMATE_INDEX = -2
LIST_LAST_INDEX = -1

NUM_ROWS = 3
ROW_LEN = 5
NUM_FULL_HOUSE = NUM_ROWS * ROW_LEN

LOWER_INDEX = 0
UPPER_INDEX = 1

row_index = {
    "FIRST_ROW": 0,
    "SECOND_ROW": 1,
    "THIRD_ROW": 2
}

ROW_INDEX_LIMITS = [
    (0, 5),
    (5, 10),
    (10, 15)
]
CALL_SEQ_RANGE_LIMITS = (1, 90)
CALL_SEQ_RANDOMNESS_CHECK_ITERS = 10

CALL_SEQ_RANDOM_LEN_LIMITS = (16, 76)
CALL_SEQ_LEN_RANDOMNESS_CHECK_ITERS = 10

MIN_NUM_GAME_PLAYERS = 1
NUM_PLAYERS = 4
round_player_index = {
    "PLAYER_ONE": 1,
    "PLAYER_TWO": 2,
    "PLAYER_THREE": 3,
    "PLAYER_FOUR": 4
}

round_game_type = {
    "FASTEST_FIRST_ROW": 1,
    "FASTEST_SECOND_ROW": 2,
    "FASTEST_THIRD_ROW": 3,
    "FASTEST_FULL_HOUSE": 4,
    "FASTEST_EARLY_FIVE": 5
}
round_game_name = {
    round_game_type["FASTEST_FIRST_ROW"]: "FASTEST-FIRST-ROW",
    round_game_type["FASTEST_SECOND_ROW"]: "FASTEST-SECOND-ROW",
    round_game_type["FASTEST_THIRD_ROW"]: "FASTEST-THIRD-ROW",
    round_game_type["FASTEST_FULL_HOUSE"]: "FASTEST-FULL-HOUSE",
    round_game_type["FASTEST_EARLY_FIVE"]: "FASTEST-EARLY-FIVE"
}
game_claim_player_index = {
    "FASTEST_FIRST_ROW": round_player_index["PLAYER_ONE"],
    "FASTEST_SECOND_ROW": round_player_index["PLAYER_THREE"],
    "FASTEST_THIRD_ROW": round_player_index["PLAYER_TWO"],
    "FASTEST_FULL_HOUSE": round_player_index["PLAYER_FOUR"],
    "FASTEST_EARLY_FIVE": round_player_index["PLAYER_THREE"]
}

game_win_claim_types = {
    "TECHNICALLY_INACCURATE": 1,
    "TECHNICALLY_ACCURATE_BUT_INVALID": 2,
    "TECHNICALLY_ACCURATE_AND_POTENTIALLY_VALID_BUT_UNRAISED": 3, # Only applicable to a non-claiming player in a game
    "TECHNICALLY_ACCURATE_AND_VALID": 4
}

possible_fastest_single_row_game_player_types = {
    "FASTEST_FIRST_ROW": 1,
    "FASTEST_SECOND_ROW": 2,
    "FASTEST_THIRD_ROW": 3
}

possible_fastest_multi_row_game_player_types = {
    "FASTEST_FULL_HOUSE": 4,
    "FASTEST_EARLY_FIVE": 5
}

possible_claiming_player_types = {
    "TECHNICALLY_INACCURATE": 1,
    "TECHNICALLY_ACCURATE_BUT_INVALID": 2,
    "TECHNICALLY_ACCURATE_AND_VALID": 3
}

possible_claiming_player_technically_inaccurate_sub_types = {
    "TECHNICALLY_INACCURATE_TYPE_1": 1,
    "TECHNICALLY_INACCURATE_TYPE_2": 2,
    "TECHNICALLY_INACCURATE_TYPE_3": 3
}

possible_claiming_player_technically_accurate_but_invalid_sub_types = {
    "TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1": 1,
    "TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2": 2,
    "TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3": 3
}

possible_claiming_player_technically_accurate_and_valid_sub_types = {
    "TECHNICALLY_ACCURATE_AND_VALID_TYPE_1": 1,
    "TECHNICALLY_ACCURATE_AND_VALID_TYPE_2": 2,
    "TECHNICALLY_ACCURATE_AND_VALID_TYPE_3": 3
}

possible_non_claiming_player_types = {
    "TECHNICALLY_INACCURATE": 1,
    "TECHNICALLY_ACCURATE_BUT_INVALID": 2,
    "TECHNICALLY_ACCURATE_AND_POTENTIALLY_VALID_BUT_UNRAISED": 3
}

NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW = 2

fastest_early_five_claim_ticket_row_matches_distro = {
    possible_claiming_player_types["TECHNICALLY_INACCURATE"]: {
        possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]: 1,
        possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]: 2,
        possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]: 1
    },
    possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]: {
        possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]: 2,
        possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]: 1,
        possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]: 2
    },
    possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]: {
        possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]: 2,
        possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]: 2,
        possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]: 1
    }
}
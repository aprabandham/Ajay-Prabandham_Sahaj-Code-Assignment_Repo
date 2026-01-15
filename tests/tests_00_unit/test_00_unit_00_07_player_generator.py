from src.player_generator.player_generator import PlayerGenerator
from src.common import NUM_PLAYERS, round_game_type, game_claim_player_index
from src.player.player import Player
from src.claim_validator.claim_validator import ClaimValidator

import pytest

num_players = NUM_PLAYERS
game_type = round_game_type["FASTEST_FIRST_ROW"]
claim_player_index = game_claim_player_index["FASTEST_FIRST_ROW"]
claim_validator = ClaimValidator(game_type)

def test_fastest_first_row_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_first_row_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_first_row_player_generator_init_game_type_lt_lower_limit_not_allowed():
    game_type = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_first_row_player_generator_init_game_type_gt_upper_limit_not_allowed():
    game_type = 6

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_first_row_player_generator_claim_player_index_lt_lower_limit_not_allowed():
    claim_player_index = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_first_row_player_generator_claim_player_index_gt_upper_limit_not_allowed():
    claim_player_index = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_first_row_player_generator_generate_player_list_returned_not_empty():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) != 0

def test_fastest_first_row_player_generator_generate_player_list_len_is_as_expected():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) == NUM_PLAYERS

def test_fastest_first_row_player_generator_generate_player_list_only_one_claiming_player():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    claiming_player_count = 0
    for player in player_list:
        if player.player_index == game_claim_player_index["FASTEST_FIRST_ROW"]:
            claiming_player_count += 1

    assert claiming_player_count == 1


game_type = round_game_type["FASTEST_SECOND_ROW"]
claim_player_index = game_claim_player_index["FASTEST_SECOND_ROW"]
claim_validator = ClaimValidator(game_type)

def test_fastest_second_row_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_second_row_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_second_row_player_generator_init_game_type_lt_lower_limit_not_allowed():
    game_type = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_second_row_player_generator_init_game_type_gt_upper_limit_not_allowed():
    game_type = 6

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_second_row_player_generator_claim_player_index_lt_lower_limit_not_allowed():
    claim_player_index = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_second_row_player_generator_claim_player_index_gt_upper_limit_not_allowed():
    claim_player_index = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_second_row_player_generator_generate_player_list_returned_not_empty():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) != 0

def test_fastest_second_row_player_generator_generate_player_list_len_is_as_expected():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) == NUM_PLAYERS

def test_fastest_second_row_player_generator_generate_player_list_only_one_claiming_player():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    claiming_player_count = 0
    for player in player_list:
        if player.player_index == game_claim_player_index["FASTEST_SECOND_ROW"]:
            claiming_player_count += 1

    assert claiming_player_count == 1


game_type = round_game_type["FASTEST_THIRD_ROW"]
claim_player_index = game_claim_player_index["FASTEST_THIRD_ROW"]
claim_validator = ClaimValidator(game_type)

def test_fastest_third_row_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_third_row_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_third_row_player_generator_init_game_type_lt_lower_limit_not_allowed():
    game_type = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_third_row_player_generator_init_game_type_gt_upper_limit_not_allowed():
    game_type = 6

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_third_row_player_generator_claim_player_index_lt_lower_limit_not_allowed():
    claim_player_index = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_third_row_player_generator_claim_player_index_gt_upper_limit_not_allowed():
    claim_player_index = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_third_row_player_generator_generate_player_list_returned_not_empty():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) != 0

def test_fastest_third_row_player_generator_generate_player_list_len_is_as_expected():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) == NUM_PLAYERS

def test_fastest_third_row_player_generator_generate_player_list_only_one_claiming_player():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    claiming_player_count = 0
    for player in player_list:
        if player.player_index == game_claim_player_index["FASTEST_THIRD_ROW"]:
            claiming_player_count += 1

    assert claiming_player_count == 1


game_type = round_game_type["FASTEST_FULL_HOUSE"]
claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
claim_validator = ClaimValidator(game_type)

def test_fastest_full_house_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_full_house_player_generator_init_num_players_lt_lower_limit_not_allowed():
    num_players = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_full_house_player_generator_init_game_type_lt_lower_limit_not_allowed():
    game_type = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_full_house_player_generator_init_game_type_gt_upper_limit_not_allowed():
    game_type = 6

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_full_house_player_generator_claim_player_index_lt_lower_limit_not_allowed():
    claim_player_index = 0

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_full_house_player_generator_claim_player_index_gt_upper_limit_not_allowed():
    claim_player_index = 5

    with pytest.raises(ValueError):
        player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)

def test_fastest_full_house_player_generator_generate_player_list_returned_not_empty():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) != 0

def test_fastest_full_house_player_generator_generate_player_list_len_is_as_expected():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    assert len(player_list) == NUM_PLAYERS

def test_fastest_full_house_player_generator_generate_player_list_only_one_claiming_player():
    player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
    player_list = player_gen.generate_player_list()

    claiming_player_count = 0
    for player in player_list:
        if player.player_index == game_claim_player_index["FASTEST_FULL_HOUSE"]:
            claiming_player_count += 1

    assert claiming_player_count == 1

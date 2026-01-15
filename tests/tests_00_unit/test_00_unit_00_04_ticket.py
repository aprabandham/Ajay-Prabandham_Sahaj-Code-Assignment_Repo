from src.ticket.ticket import Ticket
from src.common import NUM_ROWS, ROW_LEN, ROW_INDEX_LIMITS, CALL_SEQ_RANGE_LIMITS, round_game_type, round_player_index, game_claim_player_index, row_index, LOWER_INDEX, UPPER_INDEX, ZERO
import pytest

false_five = [False] * ROW_LEN
ticket_nums = [1, 9, 7, 3, 5, 75, 90, 60, 53, 88, 30, 22, 48, 36, 55]

ticket_arr = []
for i in range (0, NUM_ROWS):
    ticket_arr.append(
        list(
            zip(
                ticket_nums[ROW_INDEX_LIMITS[i][LOWER_INDEX]:ROW_INDEX_LIMITS[i][UPPER_INDEX]], 
                false_five
            )
        )
    )

game_type = round_game_type["FASTEST_FIRST_ROW"]
player_index = round_player_index["PLAYER_ONE"]
claim_player_index = game_claim_player_index["FASTEST_FIRST_ROW"]

def test_init_ticket_fastest_first_row_incorrect_num_rows_gt_required():
    ticket_arr = [
        [(1, False), (9, False), (7, False), (3, False), (5, False)],
        [(75, False), (90, False), (60, False), (53, False), (88, False)],
        [(30, False), (22, False), (48, False), (36, False), (55,False)],
        [(47, False), (42, False), (69, False), (12, False), (19,False)]
    ]

    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_num_rows_lt_required():
    ticket_arr = [
        [(1, False), (9, False), (7, False), (3, False), (5, False)],
        [(47, False), (42, False), (69, False), (12, False), (19,False)]
    ]

    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_row_len_gt_required():
    ticket_arr = [
        [(1, False), (9, False), (7, False), (3, False), (5, False)],
        [(75, False), (90, False), (60, False), (53, False), (88, False), (16, False)],
        [(30, False), (22, False), (48, False), (36, False), (55,False)],
    ]

    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_row_len_lt_required():
    ticket_arr = [
        [(1, False), (9, False), (7, False), (3, False), (5, False)],
        [(75, False), (60, False), (53, False), (88, False)],
        [(30, False), (22, False), (48, False), (36, False), (55,False)],
    ]

    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_player_index_lt_lower_bound():
    player_index = ZERO
    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_player_index_gt_upper_bound():
    player_index = 5
    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_claim_player_index_lt_lower_bound():
    claim_player_index = ZERO
    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_claim_player_index_gt_upper_bound():
    claim_player_index = 5
    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_game_type_lt_lower_bound():
    game_type = ZERO
    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_ticket_fastest_first_row_incorrect_game_type_gt_upper_bound():
    game_type = 6
    with pytest.raises(ValueError):
        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_ticket_fastest_first_row_get_first_row():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
    assert ticket_arr[row_index["FIRST_ROW"]] == ticket.get_first_row()

def test_ticket_fastest_first_row_get_second_row():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
    assert ticket_arr[row_index["SECOND_ROW"]] == ticket.get_second_row()

def test_ticket_fastest_first_row_get_third_row():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
    assert ticket_arr[row_index["THIRD_ROW"]] == ticket.get_third_row()

def test_ticket_fastest_first_row_get_all_rows():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
    assert ticket_arr == ticket_arr == ticket.get_all_rows()

def test_ticket_fastest_first_row_not_empty():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
    assert ticket.get_first_row() and ticket.get_second_row() and ticket.get_third_row()

def test_ticket_fastest_first_row_fully_populated():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
    assert len(ticket.get_first_row()) == ROW_LEN and len(ticket.get_second_row()) == ROW_LEN and len(ticket.get_third_row()) == ROW_LEN

def test_ticket_fastest_first_row_all_nums_within_range():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

    ticket_nums_flatlist = []
    ticket_nums_flatlist.extend(ticket.get_first_row())
    ticket_nums_flatlist.extend(ticket.get_second_row())
    ticket_nums_flatlist.extend(ticket.get_third_row())

    all_nums_within_range = True

    for elem in ticket_nums_flatlist:
        if elem[LOWER_INDEX] < CALL_SEQ_RANGE_LIMITS[LOWER_INDEX] or elem[LOWER_INDEX] > CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]:
            all_nums_within_range = False
            break

    assert all_nums_within_range

def test_ticket_fastest_first_row_all_nums_unique():
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

    ticket_all_nums = []
    ticket_all_nums.extend(ticket.get_first_row())
    ticket_all_nums.extend(ticket.get_second_row())
    ticket_all_nums.extend(ticket.get_third_row())

    ticket_all_nums_set = set(ticket_all_nums)
    ticket_all_nums_set_as_list = list(ticket_all_nums_set)

    assert len(ticket_all_nums) == len(ticket_all_nums_set_as_list)

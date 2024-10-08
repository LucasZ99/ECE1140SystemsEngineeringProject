import pickle
import sys
import json


def run_plc(occupancy_list):
    two_way_occupied = False
    loop_occupied = False
    zero_speed_flags = [False] * 4
    unsafe_close_blocks = []
    unsafe_toggle_switches = [False, False]

    # check if loop is occupied
    for i in range(9, 24):
        if occupancy_list[i]:
            loop_occupied = True

    # Check if two-way section is occupied
    for i in range(0, 9):
        # if there is an occupancy
        if occupancy_list[i] is True:
            two_way_occupied = True

    for i in range(24, 28):
        if occupancy_list[i] is True:
            zero_speed_flags = [True] * 4

    # Switching logic
    # check if switches are safe to toggle
    if occupancy_list[0] or occupancy_list[1] or occupancy_list[2]:
        unsafe_toggle_switches[0] = True
    if occupancy_list[6] or occupancy_list[7] or occupancy_list[8] or occupancy_list[22] or occupancy_list[23]:
        unsafe_toggle_switches[1] = True

    # if two-way section is not occupied
    if two_way_occupied is False:
        # if the entire section is empty, get ready for entry
        if loop_occupied is False:
            switch_loop = True
            switch_entry = True
        # if the loop is occupied
        else:
            switch_loop = False
            switch_entry = False
    # if the two-way section is occupied
    else:
        switch_loop = True
        switch_entry = False

    return \
        [
            switch_entry,
            switch_loop,
            False,  # no rr crossing exists
            zero_speed_flags,
            unsafe_close_blocks,
            unsafe_toggle_switches
        ]


def main():

    with open('occupancy_file.pkl', 'rb') as f:
        occupancy_list = pickle.load(f)

    result = run_plc(list(occupancy_list))

    with open('plc_result.pkl', 'wb') as f:
        pickle.dump(result, f)
        f.close()


if __name__ == '__main__':
    main()

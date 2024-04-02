import sys
import json


def run_plc(occupancy_list):
    two_way_occupied = False
    loop_occupied = False
    zero_speed_flags = [False] * 4

    # check if loop is occupied
    for i  in range(9, 24):
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

    return [switch_entry, switch_loop, False, zero_speed_flags]


def main():
    arg_json = sys.argv[1]
    occupancy_list = json.loads(arg_json)
    result = run_plc(occupancy_list)
    print(json.dumps(result))


if __name__ == '__main__':
    main()

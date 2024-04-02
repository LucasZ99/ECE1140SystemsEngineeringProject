import sys
import json


def run_plc(occupancy_list):
    # check for occupancy in 2 way section
    two_way_occupied = False
    # check for occupancy in loop
    loop_occupied = False
    rr_active = False
    zero_speed_flags = [False] * 4
    for i  in range(0, 12):
        if occupancy_list[i]:
            loop_occupied = True
    for i in range(12, 27):
        # if there is an occupancy
        if occupancy_list[i] is True:
            two_way_occupied = True
            if i in range(17, 20):
                rr_active = True
    for i in range(28, 32):
        if occupancy_list[i] is True:
            zero_speed_flags = [True] * 4

    # Switching logic
    # if the two-way section is not occupied
    if two_way_occupied is False:
        # if the entire section isn't occupied,
        if loop_occupied is False:
            switch_loop = True
            switch_entry = False
        else:
            switch_loop = False
            switch_entry = True
    else:
        switch_loop = True
        switch_entry = True

    return [switch_loop, switch_entry, rr_active, zero_speed_flags]


def main():
    arg_json = sys.argv[1]
    occupancy_list = json.loads(arg_json)
    result = run_plc(occupancy_list)
    print(json.dumps(result))


if __name__ == '__main__':
    main()

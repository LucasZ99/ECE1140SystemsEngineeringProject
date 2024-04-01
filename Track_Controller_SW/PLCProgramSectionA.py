import sys
import json


def run_plc(occupancy_list):
    # check for occupancy in 2 way section
    zone_FED_occupied = False
    rr_active = False
    zero_speed_flags = [False] * 4
    for i in range(12, 27):
        # if there is an occupancy
        if occupancy_list[i] is True:
            zone_FED_occupied = True
            if i in range(17, 20):
                rr_active = True
    for i in range(28, 32):
        if occupancy_list[i] is True:
            zero_speed_flags = [True] * 4

    # Switching logic
    if zone_FED_occupied is False:
        switch_1 = False
        switch_2 = True
    else:
        switch_1 = True
        switch_2 = False

    return [switch_1, switch_2, rr_active, zero_speed_flags]


def main():
    arg_json = sys.argv[1]
    occupancy_list = json.loads(arg_json)
    result = run_plc(occupancy_list)
    print(json.dumps(result))


if __name__ == '__main__':
    main()

import sys
import json


def run_plc(occupancy_list, zero_speed_flag_list, zone_DEF_flag, zone_AB_flag):

    # Check for safe following distance first
    # for each block
    for i in range(0, 27):
        # if there is an occupancy
        if occupancy_list[i] is True:
            # check if there's another occupancy within 4 blocks
            for j in range(i + 1, i + 5):
                # if there is another occupancy within 4 blocks
                if occupancy_list[j] is True:
                    for k in range(i, j):
                        # the train must stop
                        zero_speed_flag_list[k] = True
                # if there isn't another occupancy within 4 blocks
                else:
                    # the train can continue moving through those blocks
                    zero_speed_flag_list[j] = False

    # Switching logic
    if zone_DEF_flag is True:
        switch_1 = True
        switch_2 = True
    else:
        switch_1 = False
        switch_2 = False
    if zone_AB_flag is True:
        if zone_DEF_flag is True:
            zero_speed_flag_list[0:4] = [True] * 4

    return [zero_speed_flag_list, switch_1, switch_2]



def main():
    args_json = sys.argv[1]
    args_list = json.loads(args_json)
    occupancy_list = args_list[0]
    zero_speed_flag_list = args_list[1]
    zone_DEF_flag = args_list[2]
    zone_AB_flag = args_list[3]
    result = run_plc(occupancy_list, zero_speed_flag_list, zone_DEF_flag, zone_AB_flag)
    print(json.dumps(result))


if __name__ == '__main__':
    main()

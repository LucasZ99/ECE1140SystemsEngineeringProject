import board
import neopixel
import socket
import time
import json

numBlocks = 94

pixels1 = neopixel.NeoPixel(board.D18, numBlocks, brightness=.1)

bufferSize = 3072
ServerIP = '192.168.1.184'
# ServerIP = '172.20.10.5'
ServerPort = 2222
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((ServerIP, ServerPort))
print('Server is up')

while True:
    # decoding data
    received_data, address = RPIsocket.recvfrom(bufferSize)
    decoded_data = received_data.decode('utf-8')
    received_dict = json.loads(decoded_data)
    # print(received_dict)

    # parsing json
    blocks = {int(key): value for key, value in received_dict["blocks"].items()}
    mode = bool(received_dict["mode"])
    rr_cross = bool(received_dict["rr_cross"])
    zero_speed = {int(key): value for key, value in received_dict["zero_speed"].items()}
    strip_index = 0

    # print(mode)

    # normal: display only occupancies
    if not mode:
        for index in blocks:
            if blocks[index]:
                if rr_cross and (
                        index == 108 or index == 109 or index == 107):  # special case for rr_cross active and occ
                    pixels1[strip_index] = (158, 10, 84)
                else:
                    pixels1[strip_index] = (84, 158, 128)  # other occs
            else:
                pixels1[strip_index] = (0, 0, 0)  # shut off
            strip_index += 1

        # debug: display zero speed flags as well
    if mode:
        for index in blocks:
            if blocks[index]:
                print(index)
                if rr_cross and (
                        index == 108 or index == 109 or index == 107):  # special case for rr_cross active and occ
                    pixels1[strip_index] = (158, 10, 84)
                else:
                    pixels1[strip_index] = (84, 158, 128)  # other occs

            elif zero_speed[index]:  # zero_speed flags
                pixels1[strip_index] = (50, 0, 0)
            # print(index)

            else:
                pixels1[strip_index] = (0, 0, 0)  # shut off
            strip_index += 1

# print(message)
# print('Client:', address[0])

# RPIsocket.sendto(bytesToSend,address)
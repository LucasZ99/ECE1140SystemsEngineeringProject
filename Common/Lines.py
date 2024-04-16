from Common.GreenLine import *


def stop_name(line_id: int, block_id: int) -> str:
    block_id = abs(block_id)
    if block_id in GREEN_LINE[STATIONS]:
        name = GREEN_LINE[BLOCKS][block_id].name + " (STATION: %s)" % GREEN_LINE[STATIONS][block_id]
    else:
        name = GREEN_LINE[BLOCKS][block_id].name
    return name


def get_line_blocks() -> dict[int: Block]:
    return GREEN_LINE[BLOCKS]


def get_line_route() -> list[int]:
    return GREEN_LINE[ROUTE]


def get_line_blocks_in_route_order() -> dict[int, Block]:
    blocks_in_route_order = {}
    for block in get_line_route():
        blocks_in_route_order[abs(block)] = get_line_blocks()[abs(block)]

    return blocks_in_route_order


# linked lists path implementation
# Initialise the Node
class Node:
    def __init__(self, data):
        self.item = data
        self.next = None
        self.prev = None


# Class for doubly Linked List
class DoublyLinkedList:
    def __init__(self):
        self.start_node = None
    # Insert Element to Empty list

    def InsertToEmptyList(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
        else:
            print("The list is empty")
    # Insert element at the end

    def InsertToEnd(self, data):
        # Check if the list is empty
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            return
        n = self.start_node
        # Iterate till the next reaches NULL
        while n.next is not None:
            n = n.next
        new_node = Node(data)
        n.next = new_node
        new_node.prev = n
    # Delete the elements from the start

    def DeleteAtStart(self):
        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return
        if self.start_node.next is None:
            self.start_node = None
            return
        self.start_node = self.start_node.next
        self.start_prev = None
    # Delete the elements from the end

    def delete_at_end(self):
        # Check if the List is empty
        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return
        if self.start_node.next is None:
            self.start_node = None
            return
        n = self.start_node
        while n.next is not None:
            n = n.next
        n.prev.next = None
    # Traversing and Displaying each element of the list

    def Display(self):
        if self.start_node is None:
            print("The list is empty")
            return
        else:
            n = self.start_node
            while n is not None:
                print("Element is: ", n.item)
                n = n.next
        print("\n")

# Switches

# 13-12, 1-13

# 28-29, 150-28

# SWITCH 57-0, 57-0

# SWITCH 0-63, 0-63

# SWITCH 76-77, 77-101

# SWITCH 85-86, 100-85

# Dictionary


GREEN_LINE = [
    # Green line: line 0
    {
        # 12 -> 1
        12: [11],
        11: [10],
        10: [9],
        9: [8],
        8: [7],
        7: [6],
        6: [5],
        5: [4],
        4: [3],
        3: [2],
        2: [1],
        1: [13],  # SWITCH 13-12, 1-13

        # 13 <-> 28
        13: [12, 14],  # SWITCH 13-12, 1-13
        14: [13, 15],
        15: [14, 16],
        16: [15, 17],
        17: [16, 18],
        18: [17, 19],
        19: [18, 20],
        20: [19, 21],
        21: [20, 22],
        22: [21, 23],
        23: [22, 24],
        24: [23, 25],
        25: [24, 26],
        26: [25, 27],
        27: [26, 28],
        28: [27, 29],  # SWITCH 28-29, 150-28

        150: [28],  # SWITCH 28-29, 150-28

        # 29 -> 57
        29: [30],
        30: [31],
        31: [32],
        32: [33],
        33: [34],
        34: [35],
        35: [36],
        36: [37],
        37: [38],
        38: [39],
        39: [40],
        40: [41],
        41: [42],
        42: [43],
        43: [44],
        44: [45],
        45: [46],
        46: [47],
        47: [48],
        48: [49],
        49: [50],
        50: [51],
        51: [52],
        52: [53],
        53: [54],
        54: [55],
        55: [56],
        56: [57],
        57: [0],  # SWITCH 57-0, 57-0

        # yard
        0: [63],  # SWITCH 0-63, 0-63

        # 63 -> 76
        63: [64],
        64: [65],
        65: [66],
        66: [67],
        67: [68],
        68: [69],
        69: [70],
        70: [71],
        71: [72],
        72: [73],
        73: [74],
        74: [75],
        75: [76],
        76: [77],  # SWITCH 76-77, 77-101

        # 77 <-> 85
        77: [78, 101],  # SWITCH 76-77, 77-101
        78: [77, 79],
        79: [78, 80],
        80: [79, 81],
        81: [80, 82],
        82: [81, 83],
        83: [82, 84],
        84: [83, 85],
        85: [84, 86],  # SWITCH 85-86, 100-85

        # 86 <-> 100
        86: [87],
        87: [88],
        88: [89],
        89: [90],
        90: [91],
        91: [92],
        92: [93],
        93: [92],
        94: [95],
        95: [96],
        96: [97],
        97: [98],
        98: [99],
        99: [100],
        100: [85],  # SWITCH 85-86, 100-85

        # 101 -> 150
        101: [102],
        102: [103],
        103: [104],
        104: [105],
        105: [106],
        106: [107],
        107: [108],
        108: [109],
        109: [110],
        110: [111],
        111: [112],
        112: [113],
        113: [114],
        114: [115],
        115: [116],
        116: [117],
        117: [118],
        118: [119],
        119: [120],
        120: [121],
        121: [122],
        122: [123],
        123: [124],
        124: [125],
        125: [126],
        126: [127],
        127: [128],
        128: [129],
        129: [130],
        130: [131],
        131: [132],
        132: [133],
        133: [134],
        134: [135],
        135: [136],
        136: [137],
        137: [138],
        138: [139],
        139: [140],
        140: [141],
        141: [142],
        142: [143],
        143: [144],
        144: [145],
        145: [146],
        146: [147],
        147: [148],
        148: [149],
        149: [150]
    }
]

GREEN_LINE_ONE_PATH = [
    {
        # 12 -> 1
        "12": ["11"],
        "11": ["10"],
        "10": ["9"],
        "9": ["8"],
        "8": ["7"],
        "7": ["6"],
        "6": ["5"],
        "5": ["4"],
        "4": ["3"],
        "3": ["2"],
        "2": ["1"],
        "1": ["13"],
        # 13 -> 28
        "13": ["14"],
        "14": ["15"],
        "15": ["16"],
        "16": ["17"],
        "17": ["18"],
        "18": ["19"],
        "19": ["20"],
        "20": ["21"],
        "21": ["22"],
        "22": ["23"],
        "23": ["24"],
        "24": ["25"],
        "25": ["26"],
        "26": ["27"],
        "27": ["28"],
        "28": ["29"],
        # 29 -> 57
        "29": ["30"],
        "30": ["31"],
        "31": ["32"],
        "32": ["33"],
        "33": ["34"],
        "34": ["35"],
        "35": ["36"],
        "36": ["37"],
        "37": ["38"],
        "38": ["39"],
        "39": ["40"],
        "40": ["41"],
        "41": ["42"],
        "42": ["43"],
        "43": ["44"],
        "44": ["45"],
        "45": ["46"],
        "46": ["47"],
        "47": ["48"],
        "48": ["49"],
        "49": ["50"],
        "50": ["51"],
        "51": ["52"],
        "52": ["53"],
        "53": ["54"],
        "54": ["55"],
        "55": ["56"],
        "56": ["57"],
        "57": ["0"],
        # yard
        "0": ["63"],
        # 63 -> 76
        "63": ["64"],
        "64": ["65"],
        "65": ["66"],
        "66": ["67"],
        "67": ["68"],
        "68": ["69"],
        "69": ["70"],
        "70": ["71"],
        "71": ["72"],
        "72": ["73"],
        "73": ["74"],
        "74": ["75"],
        "75": ["76"],
        "76": ["77"],
        # 77 -> 85
        "77": ["78"],
        "78": ["79"],
        "79": ["80"],
        "80": ["81"],
        "81": ["82"],
        "82": ["83"],
        "83": ["84"],
        "84": ["85"],
        "85": ["86"],
        # 86 -> 100
        "86": ["87"],
        "87": ["88"],
        "88": ["89"],
        "89": ["90"],
        "90": ["91"],
        "91": ["92"],
        "92": ["93"],
        "93": ["92"],
        "94": ["95"],
        "95": ["96"],
        "96": ["97"],
        "97": ["98"],
        "98": ["99"],
        "99": ["100"],
        "100": ["85b"],
        # 77 <- 85
        "77b": ["101"],
        "78b": ["77b"],
        "79b": ["78b"],
        "80b": ["79b"],
        "81b": ["80b"],
        "82b": ["81b"],
        "83b": ["82b"],
        "84b": ["83b"],
        "85b": ["84b"],
        # 101 -> 150
        "101": ["102"],
        "102": ["103"],
        "103": ["104"],
        "104": ["105"],
        "105": ["106"],
        "106": ["107"],
        "107": ["108"],
        "108": ["109"],
        "109": ["110"],
        "110": ["111"],
        "111": ["112"],
        "112": ["113"],
        "113": ["114"],
        "114": ["115"],
        "115": ["116"],
        "116": ["117"],
        "117": ["118"],
        "118": ["119"],
        "119": ["120"],
        "120": ["121"],
        "121": ["122"],
        "122": ["123"],
        "123": ["124"],
        "124": ["125"],
        "125": ["126"],
        "126": ["127"],
        "127": ["128"],
        "128": ["129"],
        "129": ["130"],
        "130": ["131"],
        "131": ["132"],
        "132": ["133"],
        "133": ["134"],
        "134": ["135"],
        "135": ["136"],
        "136": ["137"],
        "137": ["138"],
        "138": ["139"],
        "139": ["140"],
        "140": ["141"],
        "141": ["142"],
        "142": ["143"],
        "143": ["144"],
        "144": ["145"],
        "145": ["146"],
        "146": ["147"],
        "147": ["148"],
        "148": ["149"],
        "149": ["150"],
        # 150
        "150": ["28b"],
        # 13 <- 28
        "13b": ["12"],
        "14b": ["13b"],
        "15b": ["14b"],
        "16b": ["15b"],
        "17b": ["16b"],
        "18b": ["17b"],
        "19b": ["18b"],
        "20b": ["19b"],
        "21b": ["20b"],
        "22b": ["21b"],
        "23b": ["22b"],
        "24b": ["23b"],
        "25b": ["24b"],
        "26b": ["25b"],
        "27b": ["26b"],
        "28b": ["27b"],
    }
]

# Step 1: 12 to 1
path_12_to_1 = list(range(12, 0, -1))

# Step 2: 13 to 57
path_13_to_57 = list(range(13, 58))

# Step 3: 0 (Directly added to the list later)
# Step 4: 63 to 100
path_63_to_100 = list(range(63, 101))

# Step 5: 85 to 77
path_85_to_77 = list(range(85, 76, -1))

# Step 6: 101 to 150
path_101_to_150 = list(range(101, 151))

# Step 7: 28 to 13
path_28_to_13 = list(range(28, 12, -1))

# Combining all paths, with explicit jumps where needed
full_path = [0] + \
            path_63_to_100 + \
            path_85_to_77 + \
            path_101_to_150 + \
            path_28_to_13 + \
            path_12_to_1 + \
            path_13_to_57

# Printing the full path
print(full_path)

# could be useful for CTC
def find_all_paths(graph, start, end, path=[]):
    """
    Find all possible paths between start and end in a graph using DFS.

    Args:
    - graph (dict): The graph represented as an adjacency list.
    - start: The starting node.
    - end: The target node.
    - path (list): Current path being explored.

    Returns:
    - List of all possible paths from start to end.
    """
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


# TODO: (implement switches, possibly by updating our dict every time a switch is flipped, which would mean originally,
#       our dict would only point to first element of switch)

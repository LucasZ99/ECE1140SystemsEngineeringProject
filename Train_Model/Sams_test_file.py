string = "0, 0, False, False, 0, , True, False"
lst = string.split(",", -1)
print(lst)
print(int(lst[0]))
print(int(lst[1]))
print(bool(lst[2]))
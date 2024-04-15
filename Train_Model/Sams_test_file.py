index = 1
train_name_list = [f'Train {index}']
print(train_name_list)

if f'Train {index}' in train_name_list:
    print("removing train in ui")
    train_name_list.remove(f'Train {index}')

print(train_name_list)
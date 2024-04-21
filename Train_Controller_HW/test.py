switchdirs_dict ={
    #downs
    "[1, 16]":0,
    "[16, 1]":0,
    "[32, 72]":0,
    "[43, 67]":0,
    #ups
    "[0, 9]":1,
    "[27, 76]":1,
    "[76, 27]":1,
    "[38, 71]":1,
    "[71, 38]":1,
    "[72, 32]":1,
    "[67, 43]":1,
    "[52, 66]":1,
    "[66, 52]":1,
    #back to yard, delete
    "[9, 0]":2
}

#[block, direction] (dir: 0:down, 1:up)
RL_LAjump_dict ={
    "[67, 1]":[43,42,41,40],
    "[1, 1]":[16,17,18,19],
    "[0, 0]":[9,8,7,6],
    "[0, 1]":[9,8,7,6],
    "[76, 0]":[27,26,25,24],
    "[72, 1]":[32,31,30,29],
    "[71, 0]":[38,37,36,35],
    "[66, 0]":[52,51,50,49]
}

apparr=[]

temp = [67, 1]
print(f"<{str(temp)}>")
'''if str(temp) in switchdirs_dict:
    print( switchdirs_dict[ str(temp) ] )
else:
    print("not in")'''
    
if str(temp) in RL_LAjump_dict:
    print( RL_LAjump_dict[ str(temp) ] )
    for x in RL_LAjump_dict[ str(temp) ]: apparr.append(x)
else:
    print("not in")
    
print(apparr)

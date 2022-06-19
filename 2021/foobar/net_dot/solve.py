flag = 'GLUG'

enc = [2410,2404,2430,2408,2391,2381,2333,2396,2369,2332,2398,2422,2332,2397,2416,2370,2393,2304,2393,2333,2416,2376,2371,2305,2377,2391]

# for sum_all in range(2349,2349+1):
#     # print (sum_all)
#     temp =[]
#     for index in range(4):
#         temp.append(enc[index] + (index % 2 * 2 + index % 3) ^ sum_all)
#
#     temp1 = "".join(chr(i) for i in temp)
#     # print (temp1)
#
#     print (sum_all)
#     print (temp1)



# values[index] = numArray[index] - (index % 2 * 2 + index % 3) ^ Program.sum_all(password);
# for sum_all in range(2400-2000,2400+40000):
#     temp =[]
#     for index in range(4):
#         temp.append(ord(flag[index]) - (index % 2 * 2 + index % 3) ^ sum_all)
#         if enc[index] == temp[index]:
#             print (sum_all)
#             print (temp)
# 2349
print (len(enc))
flag =[]
# values[index] = numArray[index] - (index % 2 * 2 + index % 3) ^ Program.sum_all(password);
for index in range(26):

    for flag_temp in range(20,127):
        temp = flag_temp - (index % 2 * 2 + index % 3) ^ 2349
        if enc[index] == temp:
            print (temp)
            flag.append(chr(flag_temp))
            break
print ("".join(flag))
# 2349

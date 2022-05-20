# f = open('input_signal.txt')

# for line in f:
#     print(len(line))
#     i = 0
#     line = line.replace('0', '0')
#     line = line.replace('1', ' ')
#     # print(line)
#     temp = ['' for _ in range(8)]
#     # print(temp)
#     while i < len(line):
#         if i % 64 == 0:
#             print('')
#             print(str(line[i:i+8]), i)
#         else:
#             print(str(line[i:i+8]), i)

#         i = i + 8

#     i = 0
#     p = 5
#     while i < len(line):
#         # if i % 64 == 0:
#         #     temp[i] += line[i::8]
#         # else:
#         temp[(i/p)%p] += line[i:i+p] + '|'

#         i = i + p

#     for i in range(p):
#         print(temp[i])


# f = open('input_signal.txt')

# for line in f:
#     print(len(line))
#     line = line.replace('0', ' ')
#     line = line.replace('1', 'O')
#     temp = ['' for _ in range(8)]

#     i = 0
#     p = 8
#     while i < len(line):
#         temp[(i/p)%p] += line[i:i+p] + '|'
#         i = i + p

#     for i in range(p):
#         print(temp[i])

f = open('input_signal.txt')


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

for line in f:
    print(len(line))
    line = line.replace('0', ' ')
    line = line.replace('1', 'O')
    temp = ['' for _ in range(8)]

    i = 0
    p = 8
    while i < len(line):
        temp[(i//p)%p] += line[i:i+p] + '|'
        i = i + p
# for i in range(p):
#     print(temp[i])
# print()
swapPositions(temp, 2, 6)
swapPositions(temp, 3, 5)
swapPositions(temp, 6, 5)
swapPositions(temp, 4, 0)
swapPositions(temp, 7, 3)
# temp = temp[::-1]
# swapPositions(temp, 3, 7)
for i in range(p):
    print(temp[i])

# 20
# HTB{B.....-.......i}
# break
# Breako
# HTB{BL1NKS_C1RsU17!}

#   OOOO  |   OO   |  0OOOOO|    OO  |   OOOOO|     OO |    O  O|O   O  O|    OO  |  OOOO  |        |     O  |    O  O| O   O  |     O  |  O   O |    O  O| OOOOOO |   OO   |  OO    |
# O       |O  OO   |OOO0  OO|O   O   |OOO   OO|O OOOOO |O   O   |OO     O|O O  O  |O  OO   |O       |OO      |O   O   |OO   O  |O       |O O   O |O   O   |O   O   |O       |O  O    |
#   O  O O|   OO  O|  OO  OO|    O  O|  OO  OO|     OOO|    O OO|O    O O|   O O O| O    OO|       O|     O O|    O OO| O   O O|   OOO O|  O   OO|    O OO|   O   O|   OO  O|   O   O|
#   O  O O|OOOOOOOO|  OO  OO|    O  O|  OO  OO|     OOO|    OO O|O     OO|  O  O O| O    OO|       O|  OOOO O|    OO O| O   O O|       O|  O   OO|    OO O|  O    O|   OO  O|   O   O|
#  OOOOOO |   OO   | OOOOOOO| OOO    | OOOOOOO|  OOOOO |OOOOOOOO|O      O| O   O  |   OO   |OOOOOOOO|  OOOO  |OOOOOOOO| O   O  |OOOOOOOO|  OOOOO |OOOOOOOO|    O   |   OO   |    OOO |
#         |OOOOOOOO|  OOOOOO| OOO    |  OOOOOO|     OO |    O   |O      O| O   O  | O    O |        |        |    O   |  OOOO  |        |  O   O |    O   | OOOOO  |   OO   |    OOO |
# O O  O  |O  OO   |OOO0  OO|O   O   |OOO   OO|O    OO |O   O   |O O    O|O  O O  |O  OO   |O       |OO      |O   O   |OO   O  |O OOOO  |O O   O |O   O   |O   O   |O  OO   |O  O    |
#   O  O  |   OO   |  OOOOOO|    OO  |  OOOOOO|     OO |    O   |O  O   O|    OO  |   OO   |        |  OOOO  |    O   |  OOOO  |     O  |  O   O |    O   |    O   |   OO   |  OO    |

#         |
# O       |
#        O|
#        O|
#         |
#         |
# O       |
#         |

# 00  |00 0|0   | 0 0|000 |000 |000 | 00 |000 |00  |0   |   0|0000|0000|0   | 000|000 |00  |0   |   0|0000|0000|00  | 000|0000|0000|    | 000| 000| 000| 000| 0 0|0000|000 |0 00| 00 |00  |0 00|00  |  00|0000|0000|    | 000|0 00|0 00|0 00|  00|0000|000 |    | 0  |00 0|00 0|00  | 0 0|0000|0000|    | 000|0   |000 |0000| 000|000 |000 |000 | 00 |00  |000 |0000| 00 |
#   00|0 0 |   0|0 00| 000| 00 | 000| 000|    |00  |    |00  |  00| 00 |0000| 000|    |00  |    |00  |0  0|0   |   0|0  0| 00 | 0  |    | 000| 00 |0 0 |000 |000 |  00|0 0 |0 00|0 00|  00|00  |  00|0000| 00 | 0  |    | 000|0 00|0 0 |0 00|0 00|0 00|  0 |    |  00|00 0|00  |   0|00 0| 00 | 0  |    | 000|   0|000 | 000| 000| 000| 00 | 000| 000|0000|000 |   0|0000|
#  000|00 0|0000|00 0| 00 |    |    |000 |   0|00  |00  |00  | 000|0000|0   |0000|   0|00  |00  |00  | 0  |0000|0000|0000| 000|0000|0000|0000|  00| 000| 000| 00 | 0 0|00 0|0 00|0000| 00 |0 0 |0000|00  | 000|0000|0000|0000|  00|0 00|00  |00  | 000|0000|0000|0000| 0 0|00 0|00 0|00 0| 000|0000|0000|0000| 000|00 0|0   |0000| 000|000 |000 |000 | 00 |000 |0000|00  |
# 0000|0 0 |0000|0 00| 000|    |    | 000|00  |00  |    |    | 000| 00 |0000|  00|00  |00  |    |    |   0|0   |0  0|0  0| 000|  0 | 000| 000|000 |00  |000 |000 |0 00|0 0 |0 00|  00| 000|00  |0000|  00| 000|  0 | 000| 000|0 00|0 0 |  00|  00|0000|000 |0000|0 00|00 0|00  |00 0|00 0| 000|  0 | 000| 000| 000|000 |  00| 000|0000| 00 | 000| 000|0000|000 |   0|0000|


# 00   |0 00 | 00 0|  000| 000 |00000|  00 |    0| 000 |   00|00  0| 00  |     |  0 0|  00 |00000|0000 |000 0|00 00|000  |000  | 0000|000 0|000  |0 000|00  0|00000|     |00000| 0 00|00  0|  000|     |000 0|000 0|   00|0 00 |00   |00000|000 0|00 00|000 0|00  0|0 000| 0000|0000 |00000| 000 | 00  |00 00|00   | 0000|
#  00 0|0 0  |000 0|000  |     |0    | 00  |00  0|00000|000  |0000 |00  0|  000|     |    0|0  00|0  00|00 00|   00| 0000|00 00|0 0 0|00 00|  00 |0  00|00000|00000|00000|0000 |    0|00000| 0000|   00|000 0| 0 00|  000|00000|     |00 00|00  0|0 0 0|0  00|     |0000 |00 00|    0|  000| 00 0|00000|00000|00000|
# 00000|    0|0 000|00   |   00|    0|0    |0    |00 00| 0000|     |0  0 |  00 |00000|00000|000 0|00  0|0 000|000  |00  0|0 000| 00 0| 00 0|00  0|0  00|  000|000 0|000 0|00  0| 00  |00   |000 0|00 00|00 00|0 0 0| 0000|00000| 0000|00 00|0 000| 000 |0 000|    0|0000 |0 00 |0 000| 0000|00  0|0  00| 000 |   0 |
# 000 0|00000|00  0|     |  000|00  0|   00|  000| 0000| 000 |  000|     |     |0   0|  0 0|0  00|     |0000 |0000 |00000|0  00|0 0 0| 0000|000 0|00 00|00000|00000|00000|00000|  000| 0000|  000|0 000|  000| 000 |    0|   0 |0000 |0 0 0|  00 |000 0|0000 |000 0|     |0000 | 0000|00000|00000|000  |000 0|00 00|
# 0 0 0|000 0|00 00| 000 |000  |0  00|     |0  00| 00 0|00000|  00 | 00  |00000|0000 |000  |0 000|    0|000 0|0  00|  0 0| 0 00| 000 |00  0|000  |00 0 |000 0|0    |00000|00000|00000|00 00|0  0 | 0000| 000 |0000 |00000|00000|0    | 000 |    0|00 00|0  00|00 00|0 000|0000 |000 0|0  00|  000|0000 |00 00|0000 |


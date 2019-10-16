
SIZE = 26

POSITION = {column + str(row) : x+SIZE*y for x, column in enumerate([chr(i) for i in range(ord("A"), ord("A")+SIZE)]) for y, row in enumerate(range(1,SIZE+1))}

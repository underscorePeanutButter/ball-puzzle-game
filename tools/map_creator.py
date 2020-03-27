map_data = [["None" for k in range(10)] for i in range(10)]

print("Puzzle Game Map Creator")

while True:
    print()
    print("Current Map Data:")
    print()
    for row in map_data:
        print(" ".join([str(value) for value in row]))
        print()
    print()

    row = input("Row to Change/Add (leave empty to finalize): ")
    if row == "":
        break
    row = int(row)

    column = int(input("Column to Change/Add: "))
    value = input("New Value: ")

    map_data[row][column] = value

print()
print("Finalizing... ", end="")

map_data_string = "["
for row in map_data[:-1]:
    map_data_string += "[" + ",".join(row) + "],\\\n"
map_data_string += "[" + ",".join(map_data[-1]) + "]"
map_data_string += "]"

with open("mapdata.txt", "w+") as file:
    file.write(map_data_string)

print("done.")

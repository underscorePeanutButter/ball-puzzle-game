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
    print("Visual:")
    print()
    print(" " + "".join([str(i) for i in range(10)]))

    i = 0
    for row in map_data:
        row_string = str(i) + ""
        for column in row:
            if column == "None":
                row_string += " "
            elif column.startswith("Wall"):
                row_string += "="
            elif column.startswith("Wedge"):
                if "ul" in column or "dr" in column:
                    row_string += "/"
                else:
                    row_string += "\\"
        print(row_string)
        i += 1
    print()



    column = input("Column to Change/Add (leave empty to finalize): ")
    if column == "":
        break
    column = int(column)
    row = int(input("Row to Change/Add: "))

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

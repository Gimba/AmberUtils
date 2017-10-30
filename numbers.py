with open("numbers.txt", 'r') as f:
    max = ""
    min = ""

    for line in f:
        line = float(line)
        if not max:
            max = line
        if not min:
            min = line

        if line > max:
            max = line
        if line < min:
            min = line

print min
print max
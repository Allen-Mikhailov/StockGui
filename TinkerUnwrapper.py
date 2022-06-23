import pandas

inputFile = "./rawTinkers.txt"
rawtext = open(inputFile, "r").read()

lines = rawtext.splitlines()


extracted = []
for i in range(len(lines)):
    rawline = lines[i]
    splitline = rawline.split(" ")
    cuts = len(splitline)

    if (cuts < 3):
        print(i)
        continue

    price = splitline[-1]
    Symbol = splitline[-2]

    name = splitline[:-2]

    line = []
    extracted.append(line)
import pandas

inputFile = "./rawTinkers.txt"
rawtext = open(inputFile, "r").read()

lines = rawtext.splitlines()


extracted = []
for i in range(lines):
    rawline = lines[i]
    splitline = rawline.split(" ")
    cuts = len(splitline)

    price = splitline[-1]
    Symbol = splitline[cuts-2]

    print(price)

    line = []
    extracted.append(line)
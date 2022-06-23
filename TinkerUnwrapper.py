import pandas

inputFile = "./rawTinkers.txt"
rawtext = open(inputFile, "r").read()

lines = rawtext.splitlines()


extracted = []
for i in range(len(lines)):
    rawline = lines[i]
    splitline = rawline.split(" ")
    cuts = len(splitline)

    price = splitline[-1]
    Symbol = splitline[-2]

    name = "".join(splitline[:-2])

    line = [name, Symbol, price]
    extracted.append(line)

df = pandas.DataFrame(extracted, columns=["Name", "Symbol", "Market Cap"])
df.to_csv("Tinkers.csv")
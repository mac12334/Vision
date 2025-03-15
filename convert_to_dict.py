def getString(filename: str) -> list[str]:
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines

def evenFurther(lines: list[str]) -> list[list[str]]:
    split = []
    for i in range(len(lines)):
        l = lines[i].strip().split(" ")
        split.append(l)
    return split

def convertToCorrectVal(twoD: list[list[str]]) -> list[list[int | float]]:
    ret = []
    for y in twoD:
        i = [int(y[0])]
        for x in range(3):
            i.append(float(y[x + 1]))
        ret.append(i)
    return ret

def conToDict(correctVal: list[list[int | float]]) -> dict[int, list[float]]:
    data = {}
    for l in correctVal:
        key = l[0]
        value = [l[1],l[2],l[3]]
        data[key] = value
    return data

def allInOne(filename: str) -> dict[int, list[float]]:
    lines = getString(filename)
    split = evenFurther(lines)
    correct = convertToCorrectVal(split)
    data = conToDict(correct)
    return data
from io import TextIOWrapper
import os
import random
import sys
from loguru import logger

# https://github.com/Delgan/loguru/issues/138#issuecomment-1491571574
# min_level = "DEBUG"
min_level = "INFO"

def min_level_filter(record):
    return record["level"].no >= logger.level(min_level).no

logger.remove()
logger.add(sys.stderr, format="[{time:HH:mm:ss.SSS} | <level>{level: <8}</level>] {message}", filter=min_level_filter)



def find_diff(input, x):
    b = {}
    result = {}
    
    for i, v in enumerate(input[x-1]):
        b[i] = v - 1
    
    for i, v in enumerate(input):
        if i + 1 == x:
            continue
        current = {}
        for ii in sorted(list(b.items())):
            current[ii[1]] = v[ii[0]]
        current = [v for k, v in sorted(current.items())]
        l = len(current)
        c = 0
        for ii, vv in enumerate(current):
            for iii in range(ii+1, l):
                if vv > current[iii]:
                    c = c + 1
        result[i + 1] = c
    return dict(sorted(result.items(), key=lambda x:x[1])) 

def file_reader(file: TextIOWrapper):
    lines = file.readlines()
    info = lines[0].split()
    if len(info) != 2:
        raise Exception("Invalid input was provided.") 
    info = [int(i) for i in info]
    result = {}
    if len(lines) != info[0]+1:
        raise Exception("Invalid input was provided.") 
    for i in range(1,info[0]+1):
        arr = []
        inputting = lines[i].split()
        if (len(inputting) != info[1]+1) or (inputting[0] in result):
            raise Exception("Invalid input was provided.") 
        for j in range(1, info[1]+1):
            arr.append(int(inputting[j]))
        result[int(inputting[0])] = arr
    return list(dict(sorted(result.items())).values())

def out(output, x):
    s = str(x)
    for k, v in output.items():
        s += "\n" + str(k) + " " + str(v)
    return s
    

if __name__ == "__main__":
    logger.info("Starting to work..")
    for filename in os.listdir("./examples"):
        inp = file_reader(open("./examples/" +filename))
        x = random.randint(1,len(inp))
        logger.debug("Working..")
        logger.debug(f"x = {x}, filename = {filename}")
        outname = filename.replace("input", "output").replace(".txt", "_" + str(x) + ".txt")
        towrite = out(find_diff(inp, x), x)
        f = open("./examples_out/" + outname, "w")
        f.write(towrite)
        f.close()
        logger.debug("Finsihed working this part!")
        logger.debug("")
    logger.info("Finished working fully.")
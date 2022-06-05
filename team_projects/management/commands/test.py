from datetime import datetime
import time
from collections import Counter
from tqdm import tqdm

def wtf(result = [], matrix = [], variants = [(1, 2, 3, 4, 5) for i in range(10)], step = 0):
    for i in variants[step]:
        new_matrix = matrix + [i]
        if step < len(variants) - 1:
            wtf(result, matrix = new_matrix, variants = variants, step = step + 1)
        else:
            return new_matrix
    return result


for i in wtf():
    print(i)

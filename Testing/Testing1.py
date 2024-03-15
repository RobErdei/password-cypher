import random
from random import shuffle
import pandas as pd

def generate_keys(charSet, countPerChar):
    baseNumSet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
    # ^Represents int versions of all legal characters allowed in the cypher
    
    keySets = []

    for char in charSet:
        keys = []
        for _ in range(countPerChar):
            shuffle(baseNumSet)
            new_key = tuple(baseNumSet)

            while new_key in keys:  # Checks if randomized key is unique and not apart of the keySets list. Continues to randomize until it's not
                shuffle(baseNumSet)
                new_key = tuple(baseNumSet)
                
            keys.append(new_key)
        
        for i, key in enumerate(keys):
            columnName = char + str(i)
            keySets.append(pd.Series(key, name=columnName))

    keySets = pd.concat(keySets, axis=1)
    keySets.index = ['placeholder'] * len(keySets)
    keySets.index.name = 'placeholder'
    print("Done")
    return keySets

def randomize_created_keys(keySet, count, amount):   # Randomizes order of keys by count of keys used and amount of sequences created
        # ^keySet is the list of all keys in data frame
        sequenceSet = []
        
        for seqSet in range(amount):   # For each sequence
            randomSequence = random.sample(keySet, count)
            sequenceSet.append(''.join(randomSequence))
        
        return sequenceSet

df = generate_keys('BACTVQRU', 6)

column_headers = df.columns.tolist()
print(column_headers)

print(randomize_created_keys(column_headers, 7, 4))
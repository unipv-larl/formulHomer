import Levenshtein as lev
import pandas as pd


def distance_matrix(input, output):
    if 'pattern1' in input:
        columns = ['subj', 'obj', 'verb']
    elif 'pattern2' in input:
        columns = ['obj', 'verb', 'atr', 'subj']
    else:
        columns = []
    df = pd.read_csv(input)
    strings = {}
    for index, row in df.iterrows():
        s = []
        for c in columns:
            s.append(row[c])
        strings[row['id']] = ' '.join(s)

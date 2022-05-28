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
    dm = {}
    for k1 in sorted(strings.keys()):
        occ1 = strings[k1]
        distances = []
        for k2 in sorted(strings.keys()):
            occ2 = strings[k2]
            distances.append(lev.distance(occ1, occ2))
        dm[k1] = distances
    df_out = pd.DataFrame.from_dict(dm)
    df_out.to_csv(output, index=False)


if __name__ == '__main__':
    distance_matrix('pattern1.csv', 'dm1.csv')
    distance_matrix('pattern2.csv', 'dm2.csv')

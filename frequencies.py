import pandas as pd


def frequencies(input_file, mode, output_file):
    df = pd.read_csv(input_file)
    if mode in ['synset', 'lemma_verb']:
        column = list(df[mode])
        keys = list(set(column))
        count = [column.count(k) for k in keys]
        df_out = pd.DataFrame.from_dict({mode: keys, 'frequence': count})
        df_out.to_csv(output_file, index=False)


if __name__ == '__main__':
    frequencies('pattern1.csv', 'synset', 'p1_synset.csv')
    frequencies('pattern1.csv', 'lemma_verb', 'p1_lemmas.csv')
    frequencies('pattern2.csv', 'synset', 'p2_synset.csv')
    frequencies('pattern2.csv', 'lemma_verb', 'p2_lemmas.csv')

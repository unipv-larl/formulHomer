import udapi
import pandas as pd

def pattern1(tb):
    # iterate over sentence of the treebank
    for sent in tb:
        root = sent.get_tree()
        # for each sentence, get the list of nodes in the sentence
        nodes = root.descendants()
        for verb in nodes:
            # check if the node is a verb
            if verb.upos == 'VERB':
                # check if the verb is finite
                if 'VerbForm' not in verb.feats or verb.feats['VerbForm'] not in ['Conv', 'Gdv', 'Ger', 'Inf', 'Part', 'Sup', 'Vnoun']:
                    pass


# tb = udapi.Document('agdt_synsets.conllu')

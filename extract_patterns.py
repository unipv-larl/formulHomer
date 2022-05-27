import udapi
import pandas as pd
from itertools import combinations


def pattern1(tb):
    results = []
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
                    # create a list with all the nodes whose parent is the verb restricting to those nodes who precedes the verb
                    prec_children = verb.children(preceding_only=True)
                    # iterate over the combinations of two preceding children
                    for pair in combinations(prec_children, 2):
                        # looking for a subject and object
                        if pair[0].deprel == 'nsubj' and pair[0].feats['Case'] == 'Nom' and \
                                pair[1].deprel == 'obj' and pair[1].feats['Case'] == 'Acc' and \
                                pair[0].precedes(pair[1]):
                            subj = pair[0]
                            obj = pair[1]
                            results.append({'subj': subj, 'obj': obj, 'verb': verb})
                        elif pair[1].deprel == 'nsubj' and pair[1].feats['Case'] == 'Nom' and \
                                pair[0].deprel == 'obj' and pair[0].feats['Case'] == 'Acc' and \
                                pair[1].precedes(pair[1]):
                            subj = pair[1]
                            obj = pair[0]
                            results.append({'subj': subj, 'obj': obj, 'verb': verb})
    return results


if __name__ == '__main__':
    tb = udapi.Document('agdt_synsets.conllu')

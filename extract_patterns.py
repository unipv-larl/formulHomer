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
            # check if the node is a verb and if its position in verse is final
            if verb.upos == 'VERB' and verb.misc['PositionInVerse'] == 'final':
                # check if the verb is finite
                if 'VerbForm' not in verb.feats or verb.feats['VerbForm'] not in ['Conv', 'Gdv', 'Ger', 'Inf', 'Part',
                                                                                  'Sup', 'Vnoun']:
                    # create a list with all the nodes whose parent is the verb restricting to those nodes who precedes the verb
                    prec_children = verb.children(preceding_only=True)
                    # restricting the list to nodes that belong to the same verse
                    same_verse = [node for node in prec_children if node.misc['Ref'] == verb.misc['Ref']]
                    # iterate over the combinations of two preceding children
                    for pair in combinations(same_verse, 2):
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


def pattern2(tb):
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
                if 'VerbForm' not in verb.feats or verb.feats['VerbForm'] not in ['Conv', 'Gdv', 'Ger', 'Inf', 'Part',
                                                                                  'Sup', 'Vnoun']:
                    # restricting the list of children to nodes that belong to the same verse
                    same_verse_children = [node for node in verb.children if node.misc['Ref'] == verb.misc['Ref']]
                    # iterate over the combinations of two preceding children
                    for pair in combinations(same_verse_children, 2):
                        # looking for a subject and object
                        if pair[0].deprel == 'nsubj' and pair[0].feats['Case'] == 'Nom' and \
                                pair[1].deprel == 'obj' and pair[1].feats['Case'] == 'Acc' and \
                                pair[1].precedes(verb) and verb.precedes(pair[0]):
                            subj = pair[0]
                            obj = pair[1]
                            # looking for an attribute
                            for atr in subj.children:
                                if atr.misc['xrel'] == 'ATR' and atr.precedes(subj) and verb.precedes(atr):
                                    results.append({'obj': obj, 'verb': verb, 'atr': atr, 'subj': subj})
                                    break
                        elif pair[1].deprel == 'nsubj' and pair[1].feats['Case'] == 'Nom' and \
                                pair[0].deprel == 'obj' and pair[0].feats['Case'] == 'Acc' and \
                                pair[0].precedes(verb) and verb.precedes(pair[1]):
                            subj = pair[1]
                            obj = pair[0]
                            # looking for an attribute
                            for atr in subj.children:
                                if atr.misc['xrel'] == 'ATR' and atr.precedes(subj) and verb.precedes(atr):
                                    results.append({'obj': obj, 'verb': verb, 'atr': atr, 'subj': subj})
                                    break
    return results


def dict_res2csv(results, output_path):
    if not results:
        print("Nothing in results list")
    else:
        dictionary = {'id': []}
        for k in results[0]:
            dictionary[k] = []
        dictionary['ref'] = []
        dictionary['lemma_verb'] = []
        dictionary['synset'] = []
        for r in results:
            dictionary['id'].append(f"occ{results.index(r) + 1}")
            for k in r:
                dictionary[k].append(r[k].form)
            dictionary['synset'].append(r['verb'].misc['Synset'])
            dictionary['lemma_verb'].append(r['verb'].lemma)
            dictionary['ref'].append(r['verb'].misc['Ref'])
        df = pd.DataFrame.from_dict(dictionary)
        df.to_csv(output_path, index=False)


if __name__ == '__main__':
    tb = udapi.Document('agdt_synsets.conllu')
    p1 = pattern1(tb)
    p2 = pattern2(tb)
    dict_res2csv(p1, "pattern1.csv")
    dict_res2csv(p2, "pattern2.csv")

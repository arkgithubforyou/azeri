import sys
import getopt
import dill
import utils
from configurations import config



## referenced from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(s1, s2):
    """
    08.10.2018
    :param s1: word1
    :param s2: word2
    :return: levenshtein distance
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        #         print(current_row)
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        #             print('ins', insertions, 'del', deletions, 'sub', substitutions)
        previous_row = current_row
    #         print(current_row)

    return previous_row[-1]

def Inflection_extraction(s1, s2):
    """
    yz
    08.10.2018
    compare lemma and inflection to form inflection rule
    """
    least_len = min(len(s1), len(s2))
    LV_distance = levenshtein(s1, s2)
    t = 0
    for i in range(least_len):
        if s1[i] != s2[i]:
            break
        t+=1
    inflection = list()
    if len(s1) == t:
        inflection.append('0')
    else:
        inflection.append(s1[t:])
    if len(s2) == t:
        inflection.append('0')
    else:
        inflection.append(s2[t:])
    inflection = tuple(inflection)
    return inflection

def inflect(lemma, inflection, rules_feature):
    """
    apply the feature matching changing rule
    :param lemma:
    :param inflection: 
    :return: descriptions
    """
    rule = 0
    length = -1
    vowel_list = ['a', 'i', 'ı', 'ə', 'ö', 'ü', 'u', 'o', 'e']
    round_vowel = ['a', 'ı','u', 'o']

    feature = 0
    lv1 = 0
    if len(lemma) >1:
        inflection = Inflection_extraction(lemma, inflection)
            
        if rules_feature[inflection] == list():
            for rule_feature in rules_feature:          ## find inflection with LV distance = 1
                if rule_feature == None:
                    break
#                     print(rule_feature)
                rule_feature_list = list(rule_feature)
                if rule_feature_list[0] == '0':
                    stem = lemma
                elif rules_feature[rule_feature] != []:
                    stem = lemma[:len(lemma)-len(rules_feature[rule_feature][-1][0])]
                if rule_feature_list[1] == '0':
                    inflected_form_proposed = stem
                elif rules_feature[rule_feature] != []:
#                         print(rules_feature[rule_feature])
                    inflected_form_proposed = stem + rules_feature[rule_feature][-1][1]
                if levenshtein(inflected_form_proposed, inflection) == 1:
                    inflection = rule_feature
                    lv1 = 1
                    break
        if rules_feature[inflection] == list() and lv1 == 0:
            for rule_feature in rules_feature:          ## find inflection with LV distance = 2
                if rule_feature == None:
                    break
                rule_feature_list = list(rule_feature)
                if rule_feature_list[0] == '0':
                    stem = lemma
                elif rules_feature[rule_feature] != []:
                    stem = lemma[:len(lemma)-len(rules_feature[rule_feature][-1][0])]
                if rule_feature_list[1] == '0':
                    inflected_form_proposed = stem
                elif rules_feature[rule_feature] != []:
                    inflected_form_proposed = stem + rules_feature[rule_feature][-1][1]
                if levenshtein(inflected_form_proposed, inflection) == 2:
                    inflection = rule_feature
#                         lv1 = 1
                    break
        if len(rules_feature[inflection]) > 1:
            feature = 0
            for rule_feature in rules_feature[inflection]:   # check if last two letters of lemma match that of any feature
                if lemma[-2:] == rule_feature[0]:
                    feature = rule_feature[-1]
                    break
            if feature == 0:   
                if lemma[-1] in vowel_list:   # extract vowel in last two letters of lemma
                    vowel = lemma[-1]
                elif lemma[-2] in vowel_list:
                    vowel = lemma[-2]
                else:
                    vowel = 'no_vowel'
                        
                for rule_feature in rules_feature[inflection]:  # 
                    if vowel == rule_feature[1]:
                        feature = rule_feature[-1]
                        break
            if feature == 0:
                if vowel in round_vowel:
                    round_vowel_feature = 'round_vowel'
                elif vowel == 'no_vowel':
                    round_vowel_feature = 'no_vowel'
                else:
                    round_vowel_feature = 'no_round_vowel'
                for rule_feature in rules_feature[inflection]:
                    if round_vowel_feature == rule_feature[2]:
                        feature = rule_feature[-1]
                        break
            if feature == 0:
                for rule_feature in rules_feature[inflection]:
                    if lemma[-1] == rule_feature[3]:
                        feature = rule_feature[-1]
                        break
            if feature == 0:
                feature = rules_feature[inflection][0][-1]
        elif len(lemma) == 1:
#                 print(inflection, rules_feature[inflection])
            feature = rules_feature[inflection][0][-1]
        # else:
        #     no_cat += 1
            
##        if feature == elements[2]:
##            correct_num += 1
##    if len(elements) >1: print(feature, elements[2], lemma, inflection)
                    


    
        
    return feature
    


def batch_inflect(train_data, test_data):
    """
    perform task2 inflection on specific train and test data
    :param train_data:
    :param test_data:
    :return: the statistics, and the output
    """
    rules = utils.generate_rules_task3(train_data)
    # print('rules', rules)
    output = list()
    correct_list = list()
    for test_item in test_data:
        output_item = dict()
        output_item['lemma'] = test_item['lemma']
        output_item['inflection'] = test_item['inflection']
        output_item['descriptions'] = inflect(output_item['lemma'], output_item['inflection'], rules)
        output.append(output_item)
        if output_item['descriptions'] == test_item['descriptions']:
            correct_list.append(test_item)
    train_count = len(train_data)
    test_count = len(test_data)
    correct_count = len(correct_list)

    return train_count, test_count, correct_count, output


if __name__ == '__main__':
    opts = utils.getopt_for_naocanzhujiao(sys.argv[1:])
    if '-g' in opts:
        print('Group L01: Azeri')
        print('Guo Yanzhe, 2571732')
        print('Zhai Fangzhou, 2566641')
        print('Zhu Dawei, 2549931')
        exit(0)
    if '-tr' in opts:
        ''' update train file path '''
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        dill.dump((opts['-tr'], test_file), open(config.config_file, 'wb'))
    if '-te' in opts:
        ''' update test file path '''
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        dill.dump((train_file, opts['-te']), open(config.config_file, 'wb'))
    if '-a' in opts:
        ''' perform task 1 and evaluate accuracy '''
        # load data
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        train_data = utils.load_data(train_file, 3)
        test_data = utils.load_data(test_file, 3)
        ''' perform inflection '''
        tr_c, te_c, co_c, _ = batch_inflect(train_data, test_data)
        ''' output accuracy '''
        print('trained on: ' + train_file)
        print('- training instances : ' + str(tr_c))
        print('tested on: ' + test_file)
        print('- testing instances : ' + str(te_c))
        print('- correct instances : ' + str(co_c))
        print('- accuracy : ' + str(round(co_c/te_c, 3)))
    if '-l' in opts:
        ''' perform task 1 and evaluate accuracy '''
        # load data
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        train_data = utils.load_data(train_file, 3)
        test_data = utils.load_data(test_file, 3)
        ''' perform inflection '''
        tr_c, te_c, co_c, results = batch_inflect(train_data, test_data)
        ''' output accuracy '''
        print('trained on: ' + train_file)
        print('- training instances : ' + str(tr_c))
        print('tested on: ' + test_file)
        print('- testing instances : ' + str(te_c))
        print('- correct instances : ' + str(co_c))
        print('- accuracy : ' + str(round(co_c / te_c, 3)))
        print('-------------------results--------------------')
        ''' output results '''
        for item in results:
            print(item['descriptions'])
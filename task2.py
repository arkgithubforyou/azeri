import sys
import getopt
import dill
import utils
from configurations import config
import utils2

def inflect(lemma, description, rules):
    """
    apply the feature matching changing rule
    :param lemma:
    :param description: a SET of features
    :return: inflected word
    """
    rule = 0
    length = -1
    vowel_list = ['a', 'i', 'ı', 'ə', 'ö', 'ü', 'u', 'o', 'e']
    round_vowel = ['a', 'ı','u', 'o']


    if len(rules[description]) > 1:
        ## to match feature 1
        for rule_in_list in rules[description]:
            if lemma[-2:] == rule_in_list[2]:
                rule = rule_in_list
                break
        ## to match feature 2
        if rule == 0:
            if lemma[-1] in vowel_list:  
                vowel = lemma[-1]
            elif lemma[-2] in vowel_list:
                vowel = lemma[-2]
            else:
                vowel = 'no_vowel'
            for rule_in_list in rules[description]:
                if vowel == rule_in_list[3]:
                    rule = rule_in_list
                    break
        ## to match feature 3
        if rule == 0:
            if vowel in round_vowel:
                for rule_in_list in rules[description]:
                    if rule_in_list[4] == 'round_vowel':
                        rule = rule_in_list
                        break
            else:
                for rule_in_list in rules[description]:
                    if rule_in_list[4] == 'no_round_vowel':
                        rule = rule_in_list
                        break
        ## to match feature 4
        if rule == 0:
            for rule_in_list in rules[description]:
                if vowel == rule_in_list[5]:
                    rule = rule_in_list
                    break
        if rule == 0:
            rule = rules[description][0]
    ## if no rule matches, use first rule
    elif len(rules[description]) >0:
        rule = rules[description][0]
#         print(elements, rules[description])
    else:
        return lemma
    if rule[0] == '0':
        stem = lemma
#       print(stem)
    else:
        stem = lemma[:len(lemma)-len(rule[0])]
    if rule[1] == '0':
        inflected_form = stem
    else:
        inflected_form = stem + rule[1]
        
    return inflected_form
    


def batch_inflect(train_data, test_data):
    """
    perform task2 inflection on specific train and test data
    :param train_data:
    :param test_data:
    :return: the statistics, and the output
    """
    rules = utils2.generate_rules_task2(train_data)
    # print('rules', rules)
    output = list()
    correct_list = list()
    for test_item in test_data:
        output_item = dict()
        output_item['lemma'] = test_item['lemma']
        output_item['descriptions'] = test_item['descriptions']
        output_item['inflection'] = inflect(output_item['lemma'], output_item['descriptions'], rules)
        output.append(output_item)
        if output_item['inflection'] == test_item['inflection']:
            correct_list.append(test_item)
    train_count = len(train_data)
    test_count = len(test_data)
    correct_count = len(correct_list)

    return train_count, test_count, correct_count, output


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'agl', ['tr:', 'te:'])
    opts = dict(opts)
    if '-g' in opts:
        print('Group L01: Azeri')
        print('Guo Yanzhe, 2571732')
        print('Zhai Fangzhou, 2566641')
        print('Zhu Dawei, 2549931')
        exit(0)
    if '--tr' in opts:
        ''' update train file path '''
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        dill.dump((opts['-tr'], test_file), open(config.config_file, 'wb'))
    if '--te' in opts:
        ''' update test file path '''
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        dill.dump((opts['-te'], test_file), open(config.config_file, 'wb'))
    if '-a' in opts:
        ''' perform task 1 and evaluate accuracy '''
        # load data
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        train_data = utils.load_data(train_file)
        test_data = utils.load_data(test_file)
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
        train_data = utils.load_data(train_file)
        test_data = utils.load_data(test_file)
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
            print(item['inflection'])

import sys
import getopt
import dill
import utils
from configurations import config

def inflect(lemma, description, rules):
    """
    apply the longest suffix changing rule
    :param lemma:
    :param description: a SET of features
    :return: inflected word
    """
    rule = None
    length = -1
    ''' find longest matching rule '''
    for rule_identifier in rules:
        rule_item = rules[rule_identifier]
        pre = rule_item['pre']
        ''' matching rule '''
        if lemma.find(pre) != -1 and lemma.find(pre) + len(pre) == len(lemma) and description in rule_item['instances']:
            if len(pre) > length:
                rule = rule_item
                length = len(pre)
    ''' apply rule '''
    if rule is None:
        ''' return lemma if no matching rule is found '''
        return lemma
    else:
        ''' perform longest matching rule '''
        return lemma[:lemma.find(rule['pre'])] + rule['post']


def batch_inflect(train_data, test_data):
    """
    perform task1 inflection on specific train and test data
    :param train_data:
    :param test_data:
    :return: the statistics, and the output
    """
    rules = utils.generate_rules(train_data)
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
    if '-tr' in opts:
        ''' update train file path '''
        train_file, test_file = dill.load(open(config.config_file, 'rb'))
        dill.dump((opts['-tr'], test_file), open(config.config_file, 'wb'))
    if '-te' in opts:
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
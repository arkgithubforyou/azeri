from configurations import config
from collections import defaultdict

def clean_str(s):
    """
    remove ending underscores from strings
    :param s:
    :return:
    """
    r = s
    while r != '':
        if r[-1] == '_':
            r = r[:-1]
        else:
            break
    return r


def generate_rules(data):
    """
    Ark
    03.08.2018

    generate suffix changing rules.
    NOTE: Due to data statistics, the Azeri language has NO prefix.

    :param data: data used for rule generation. list of dictionaries.
    :return: a dictionary, each item represent a rule
        key: 'pre2post'
        value: dictionary
            pre: before transformation
            post: after transformation
            count:
            instances: feature combinations for which the rule was applied
            minimal: whether the rule is minimal
    """
    rules = dict()
    for inflection_item in data:
        lemma = inflection_item['lemma']
        inflection = inflection_item['inflection']

        ''' align words '''
        if len(lemma) < len(inflection):
            lemma += (len(inflection) - len(lemma)) * '_'
        else:
            inflection += (len(lemma) - len(inflection)) * '_'
        ''' skip trivial rules '''
        pointer = len(lemma) - 1
        while lemma[pointer] == '_':
            pointer -= 1
        if pointer != len(lemma) - 1:
            pointer += 1
        ''' extract rules '''
        is_minimal_rule = True
        while pointer >= 0:
            pre = clean_str(lemma[pointer:])
            post = clean_str(inflection[pointer:])
            rule_identifier = pre + '->' + post
            if rule_identifier not in rules:
                rule_item = dict()
                rule_item['pre'] = pre
                rule_item['post'] = post
                rule_item['count'] = 1
                rule_item['instances'] = list([inflection_item['descriptions']])
                rule_item['minimal'] = is_minimal_rule
                rules[rule_identifier] = rule_item
            else:
                rules[rule_identifier]['count'] += 1
                rules[rule_identifier]['instances'].append(inflection_item['descriptions'])
                rules[rule_identifier]['minimal'] = is_minimal_rule
            is_minimal_rule = False
            pointer -= 1
    return rules

def generate_rules_task2(data):
    """
    yz
    08.08.2018
    generate suffix changing rules.
    NOTE: Due to data statistics, the Azeri language has NO prefix.
    :param data: data used for rule generation. list of dictionaries.
    :return: a dictionary, each item represent rules of a description
        key: 'cat'
        value: a list of 6 elements
            element 1: suffix to be removed from lemma
            element 2: suffix to be added to form inflected form
            element 3: feature 1: last two letters of lemma
            element 4: feature 2: vowel in last two letters (no consecutive vowels is observed)
            element 5: feature 3: identify 'a', 'ı','u', 'o' in the last two letters
            element 6: feature 4: last letter of lemma
            (feature 1-4 are defined in terms of lemma)
    """
    rules = defaultdict(list)
    count_pre_diff = 0
    no_change = ['0', '0']
    vowel_list = ['a', 'i', 'ı', 'ə', 'ö', 'ü', 'u', 'o', 'e']
    round_vowel = ['a', 'ı','u', 'o']
    for item in data:
        if len(item['lemma']) >1:
            cat = item['descriptions']
            if item['lemma'][:2] == item['inflection'][:2]:
                count_pre_diff += 1
            least_len = min(len(item['lemma']), len(item['inflection']))
            t = 0
            for i in range(least_len):
                if item['lemma'][i] != item['inflection'][i]:
                    break
                t+=1
            rule = list()
            if len(item['lemma']) == t:
                rule.append('0')
            else:
                rule.append(item['lemma'][t:])
            if len(item['inflection']) == t:
                rule.append('0')
            else:
                rule.append(item['inflection'][t:])
            rule.append(item['lemma'][-2:])        ## feature 1: last two letters
            if item['lemma'][-1] in vowel_list:  ## feature 2: vowel in last two letters
                rule.append(item['lemma'][-1])
            elif item['lemma'][-2] in vowel_list:
                rule.append(item['lemma'][-2])
            else:
                rule.append('no_vowel')
            if item['lemma'][-1] in round_vowel or item['lemma'][-2] in round_vowel: ## feature 3: identify 'a', 'ı','u', 'o' in the last two letters
                rule.append('round_vowel')
            elif rule[-1] == 'no_vowel':
                rule.append('no_vowel')
            else:
                rule.append('no_round_vowel')
            rule.append(item['lemma'][-1])        ## feature 4: last letter
            
            if rule not in rules[cat]:
                rules[cat].append(rule)
    # print(rules)
    return rules


def generate_rules_task3(data):
    """
    yz
    08.10.2018
    generate features
    NOTE: Due to data statistics, the Azeri language has NO prefix.
    :param data: data used for rule generation. list of dictionaries.
    :return: a dictionary, each item represent rules of an inflection type
        key: 'inflection type'
        value: a list of 5 elements
            element 1: feature 1: last two letters of lemma
            element 2: feature 2: vowel in last two letters (no consecutive vowels is observed)
            element 3: feature 3: identify 'a', 'ı','u', 'o' in the last two letters
            element 4: feature 4: last letter of lemma
            element 5: description
            (feature 1-4 are defined in terms of lemma)
    """
    rules_feature = defaultdict(list)
    count_pre_diff = 0
    no_change = ['0', '0']
    vowel_list = ['a', 'i', 'ı', 'ə', 'ö', 'ü', 'u', 'o', 'e']
    round_vowel = ['a', 'ı', 'u', 'o']
    for item in data:
        if len(item['lemma']) > 1:
            inflected_form = item['inflection']
            #             print(rules[cat])
            if item['lemma'][:2] == item['inflection'][:2]:
                count_pre_diff += 1
            least_len = min(len(item['lemma']), len(item['inflection']))
            t = 0
            #             print(len(item['lemma']), len(item['inflection']), least_len)
            for i in range(least_len):
                #                 print(i)
                if item['lemma'][i] != item['inflection'][i]:
                    break
                t += 1
            #                 print(t, item['lemma'][i], item['inflection'][i])
            rule_feature = list()
            inflection = list()
            if len(item['lemma']) == t:
                inflection.append('0')
            else:
                inflection.append(item['lemma'][t:])
            if len(item['inflection']) == t:
                inflection.append('0')
            else:
                inflection.append(item['inflection'][t:])
            inflection = tuple(inflection)
            rule_feature.append(item['lemma'][-2:])  ## feature 1: last two letters
            if item['lemma'][-1] in vowel_list:  ## feature 2: vowel in last two letters
                rule_feature.append(item['lemma'][-1])
            elif item['lemma'][-2] in vowel_list:
                rule_feature.append(item['lemma'][-2])
            else:
                rule_feature.append('no_vowel')
            if item['lemma'][-1] in round_vowel or item['lemma'][
                -2] in round_vowel:  ## feature 3: identify 'a', 'ı','u', 'o' in the last two letters
                rule_feature.append('round_vowel')
            elif rule_feature[-1] == 'no_vowel':
                rule_feature.append('no_vowel')
            else:
                rule_feature.append('no_round_vowel')
            rule_feature.append(item['lemma'][-1])  ## feature 4: last letter

            rule_feature.append(item['descriptions'])  ## add type/label of the inflection

            if rule_feature not in rules_feature[inflection]:
                rules_feature[inflection].append(rule_feature)

    return rules_feature


def clean_str(s):
    """
    remove ending underscores from strings
    :param s:
    :return:
    """
    r = s
    while r != '':
        if r[-1] == '_':
            r = r[:-1]
        else:
            break
    return r


def generate_rules(data):
    """
    Ark
    03.08.2018

    generate suffix changing rules.
    NOTE: Due to data statistics, the Azeri language has NO prefix.

    :param data: data used for rule generation. list of dictionaries.
    :return: a dictionary, each item represent a rule
        key: 'pre2post'
        value: dictionary
            pre: before transformation
            post: after transformation
            count:
            instances: feature combinations for which the rule was applied
            minimal: whether the rule is minimal
    """
    rules = dict()
    for inflection_item in data:
        lemma = inflection_item['lemma']
        inflection = inflection_item['inflection']

        ''' align words '''
        if len(lemma) < len(inflection):
            lemma += (len(inflection) - len(lemma)) * '_'
        else:
            inflection += (len(lemma) - len(inflection)) * '_'
        ''' skip trivial rules '''
        pointer = len(lemma) - 1
        while lemma[pointer] == '_':
            pointer -= 1
        if pointer != len(lemma) - 1:
            pointer += 1
        ''' extract rules '''
        is_minimal_rule = True
        while pointer >= 0:
            pre = clean_str(lemma[pointer:])
            post = clean_str(inflection[pointer:])
            rule_identifier = pre + '->' + post
            if rule_identifier not in rules:
                rule_item = dict()
                rule_item['pre'] = pre
                rule_item['post'] = post
                rule_item['count'] = 1
                rule_item['instances'] = list([inflection_item['descriptions']])
                rule_item['minimal'] = is_minimal_rule
                rules[rule_identifier] = rule_item
            else:
                rules[rule_identifier]['count'] += 1
                rules[rule_identifier]['instances'].append(inflection_item['descriptions'])
                rules[rule_identifier]['minimal'] = is_minimal_rule
            is_minimal_rule = False
            pointer -= 1
    return rules


def load_data(data_file, task=1):
    """
    read data files.
    task=1,2: lemma + description
    task=3: lemma + inflection
    :return: a list of dictionaries giving the lemma, the inflected form and the description as a string
    """
    data = list()
    with open(data_file,encoding='utf-8') as fin:
        buffer = fin.readline()
        while buffer != '':
            splitted_buffer = buffer.split('\t')
            if((len(splitted_buffer) != 2) & (len(splitted_buffer) != 3)):
                raise ValueError('WRONG format in the data, except: a row with 2 or 3 strings, got:', splitted_buffer)
            item = dict()

            if(len(splitted_buffer) == 3):
                item['lemma'] = splitted_buffer[0]
                item['inflection'] = splitted_buffer[1]
                item['descriptions'] = splitted_buffer[2].strip() # strip() remove "\n" from the string
            elif(task == 1 or task == 2):
                assert(len(splitted_buffer) == 2)
                item['lemma'] = splitted_buffer[0]
                # item['inflection'] = splitted_buffer[1]
                item['descriptions'] = splitted_buffer[2].strip() # strip() remove "\n" from the string
            elif task == 3:
                assert (len(splitted_buffer) == 2)
                item['lemma'] = splitted_buffer[0]
                item['inflection'] = splitted_buffer[1]
                # item['descriptions'] = splitted_buffer[2]
            data.append(item)
            buffer = fin.readline()

    return data


def getopt_for_naocanzhujiao(args):
    """
    parse cmd arguments
    :param args:
    :return:
    """
    opts = dict()
    for (i, arg) in enumerate(args):
        if arg in ['-a', '-g', '-l']:
            opts[arg] = ''
        if arg in ['-tr', '-te']:
            opts[arg] = args[i + 1]
    return opts


"==============  not for submission  ==============="
def str_cmp(s1, s2):
    i = 0
    while i<len(s1) and i<len(s2):
        if s1[i] == s2[i]:
            i += 1
        else:
            break
    if i == 0:
        print('------------------prefix detected------------------')
        print(i, len(s1), len(s2))

p = config.train_path_high
d = load_data(p)
rls = generate_rules(d)

pass

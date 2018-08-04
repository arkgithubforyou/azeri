from configurations import config


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


def load_data(data_file):
    """
    read 3-column data files
    :return: a list of dictionaries giving the lemma, the inflected form and the description as a string
    """
    data = list()
    with open(data_file,encoding='utf-8') as fin:
        buffer = fin.readline()
        while buffer != '':
            splitted_buffer = buffer.split('\t')
            item = dict()
            item['lemma'] = splitted_buffer[0]
            item['inflection'] = splitted_buffer[1]
            item['descriptions'] = splitted_buffer[2]
            data.append(item)
            buffer = fin.readline()

    return data




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

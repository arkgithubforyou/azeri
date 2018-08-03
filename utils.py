from configurations import config

def load_data(data_file):
    """
    read 3-column data files
    :return: a list of dictionaries
    """
    data = list()
    with open(data_file,encoding='utf-8') as fin:
        buffer = fin.readline()
        while buffer != '':
            splitted_buffer = buffer.split()
            item = dict()
            item['lemma'] = splitted_buffer[0]
            item['inflection'] = splitted_buffer[1]
            item['descriptions'] = splitted_buffer[2].split(';')
            data.append(item)
            buffer = fin.readline()

    return data


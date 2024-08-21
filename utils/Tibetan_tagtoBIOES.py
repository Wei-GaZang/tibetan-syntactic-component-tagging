# 保存txt文件
def served_txt(list_file, name):
    """
    保存txt文件
    :param list_file: 保存内容
    :param name: 文件名
    """

    file = open(r'/Users/weiriwa/PycharmProjects/NCRFpp/sample_data/' + name, mode='w', encoding='utf-8')
    for i in list_file:
        file.write(i + '\n')
    file.close()
    print(name)

def open_txet(path):
    with open(path, 'r', encoding='utf-8') as f:
        dataset = []
        for lines in f.readlines():
            lines = lines.replace('\n', '').strip()
            new_row = lines.split('[')
            sentece_list = []
            for row in new_row:
                if row != '':
                    w_l = row.split(']')
                    sentece_list.append([w_l[0].strip(), w_l[1].strip()])
            # print(sentece_list)
            dataset.append(sentece_list)
            # break
    print('有：', len(dataset), '行')
    return dataset


tag_list = ['sub', 'obj', 'pre', 'hed', 'atr', 'adv', 'com']
case_sub = ['bo', 'cl', 'ci', 'cr', 'cj', 'cp']
case_obj = ['ls']
case_adv = ['ba', 'by', 'bc', 'lg', 'lt', 'lh', 'ld', 'jg', 'cp', 'cb']
case_art = ['gi']




def lien2bios(dataset):
    data_BIOE = []
    try:
        for sentence in dataset:
            new_sentence = ''
            # print(sentence)
            for word in sentence:
                if word[1] in tag_list:
                    sent = word[0].split(' ')
                    if len(sent) > 2:
                        for i in range(len(sent)-1):
                            if i == 0:
                                new_sentence += sent[i] + ' B-' + word[1] + '\n'
                            else:
                                new_sentence += sent[i] + ' I-' + word[1] + '\n'
                        new_sentence += sent[-1] + ' E-' + word[1] + '\n'
                    elif len(sent) == 2:
                        new_sentence += sent[0] + ' B-' + word[1] + '\n'
                        new_sentence += sent[1] + ' E-' + word[1] + '\n'
                    else:
                        new_sentence += word[0] + ' S-' + word[1] + '\n'
                else:
                    sent = word[0].split(' ')
                    if len(sent) > 1:
                        for w in sent:
                            new_sentence += w + ' O\n'
                    else:
                        new_sentence += word[0] + ' O\n'
            # print(new_sentence)
            data_BIOE.append(new_sentence)
    except Exception:
        print(word)
    return data_BIOE

def bioe2case_cappos(data_BIOE):
    """
    句法成分与虚词分开
    句法成分标记为： 1， 虚词标记为： 0
    """
    data_cappos = []
    count = 0
    for lien in data_BIOE:
        word_list = lien.strip().split('\n')
        # print(count, '\n')
        new_lien = ''
        for w in word_list:
            words = w.split(' ')
            w_l = words[0].split('_')
            cap = 0
            if words[1] != 'O':
                cap = 1
            new_lien += w_l[0] + ' [Cap]' + str(cap) + ' [POS]' + w_l[1] + ' ' + words[1] + '\n'
        data_cappos.append(new_lien)

        count += 1
    return data_cappos

def bioe2rul_efeatures(data_BIOE):
    """
    按格助词的句法成分功能
    粗粒度的规则知识融合
    """
    data_cappos = []
    count = 0
    for lien in data_BIOE:
        word_list = lien.strip().split('\n')
        # print(count, '\n')
        new_lien = ''
        for w in word_list:
            words = w.split(' ')
            w_l = words[0].split('_')
            cap = 0
            if w_l[1] in case_sub:
                cap = 1
            elif w_l[1] == 'ls':
                cap = 2
            elif w_l[1] == 'gi':
                cap = 3
            elif w_l[1] in case_adv:
                cap = 4

            new_lien += w_l[0] + ' [Cap]' + str(cap) + ' [POS]' + w_l[1] + ' ' + words[1] + '\n'
        data_cappos.append(new_lien)

        count += 1
    return data_cappos

def bioe2knowledge_features(data_bioe, rule_bioe):
    """
        按规则或模型标注的结果进行数据预处理 融入规则知识特征：cap
        主语：1
        宾语：2
        谓语：3
        主要动词：4
        定语：5
        状语：6
        补语：7
        虚词：0
    """
    data_cappos = []
    print(len(data_bioe), len(rule_bioe))
    for sentence, rule in zip(data_bioe, rule_bioe):

        word_list = sentence.strip().split('\n')
        rule_list = rule.strip().split('\n')

        new_lien = ''
        for w, r in zip(word_list, rule_list):
            # print(w, r)
            words = w.split(' ')
            w_l = words[0].split('_')

            rules = r.split(' ')
            # r_l = rules[0].split('_')
            cap = 0
            if rules[1] != 'O':
                if rules[1].split('-')[1] in tag_list:
                    cap = tag_list.index(rules[1].split('-')[1]) + 1

            new_lien += w_l[0] + ' [Cap]' + str(cap) + ' [POS]' + w_l[1] + ' ' + words[1] + '\n'
        data_cappos.append(new_lien)
        # print(new_lien)
    return data_cappos




if __name__ == '__main__':
    dataset = open_txet(r'/Users/weiriwa/PycharmProjects/NCRFpp/sample_data/t_sentence.train')
    data_BIOE = lien2bios(dataset)
    rule_dataset = open_txet(r'/Users/weiriwa/PycharmProjects/NCRFpp/sample_data/t_sentence.train')
    rule_data_BIOE = lien2bios(rule_dataset)
    data_features = bioe2knowledge_features(data_BIOE, rule_data_BIOE)
    # data_cappos = bioe2rul_efeatures(data_BIOE)
    served_txt(data_features, 'ti2_sentence.train')

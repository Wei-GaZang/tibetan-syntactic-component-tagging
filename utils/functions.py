# -*- coding: utf-8 -*-
# @Author: Jie
# @Date:   2017-06-15 14:23:06
# @Last Modified by:   Jie Yang,     Contact: jieynlp@gmail.com
# @Last Modified time: 2019-02-14 12:23:52
from __future__ import print_function
from __future__ import absolute_import
import sys
import numpy as np

case = ['gj', 'ls', 'lg', 'lt', 'ld', 'lh', 'bo', 'ba', 'bc', 'by', 'bg', 'gi', 'cv', 'cl', 'cn', 'cb', 'ci',
        'ck', 'ca', 'ct', 'cc', 'cf', 'cz', 'cu', 'cg', 'ce', 'cs', 'cm', 'cy', 'cr', 'cj', 'cp', 'cq', 'fh', 'fg',
        'fz', 'fj', 'df', 'rf', 'ww', 'ee']

def normalize_word(word):
    new_word = ""
    for char in word:
        if char.isdigit():
            new_word += '0'
        else:
            new_word += char
    return new_word

def convert_sentence_2_conll(char_list, default_tag):
    token_list = []
    for char in char_list:
        '''将空格替换为逗号, chinese'''
        if char == ' ':
            char = '，'
        token_list.append('\t'.join([char, default_tag]))
    return token_list

def forecast_pre_data(char_list, default_tag):
    token_list = []
    for token in char_list:
        token_w = token.split('_')
        feature_pos = '[POS]' + token_w[1]
        feature_cap = '[Cap]'
        if token_w[1] in case:
            feature_cap += '0'
        else:
            feature_cap += '1'
        token_list.append('\t'.join([token_w[0], feature_cap, feature_pos, default_tag]))
    return token_list


def read_instance(input_file, word_alphabet, char_alphabet, feature_alphabets, label_alphabet, number_normalized,
                  max_sent_length, sentence_classification=False, split_token='\t', char_padding_size=-1,
                  char_padding_symbol='</pad>'):
    feature_num = len(feature_alphabets)
    in_lines = open(input_file, 'r', encoding="utf8").readlines()
    instence_texts = []
    instence_Ids = []
    words = []
    features = []
    chars = []
    labels = []
    word_Ids = []
    feature_Ids = []
    char_Ids = []
    label_Ids = []

    # # if sentence classification data format, splited by \t
    if sentence_classification:
        for line in in_lines:
            if len(line) > 2:
                pairs = line.strip().split(split_token)
                sent = pairs[0]
                if sys.version_info[0] < 3:
                    sent = sent.decode('utf-8')
                original_words = sent.split()
                for word in original_words:
                    words.append(word)
                    if number_normalized:
                        word = normalize_word(word)
                    word_Ids.append(word_alphabet.get_index(word))
                    # # get char
                    char_list = []
                    char_Id = []
                    for char in word:
                        char_list.append(char)
                    if char_padding_size > 0:
                        char_number = len(char_list)
                        if char_number < char_padding_size:
                            char_list = char_list + [char_padding_symbol] * (char_padding_size - char_number)
                        assert (len(char_list) == char_padding_size)
                    for char in char_list:
                        char_Id.append(char_alphabet.get_index(char))
                    chars.append(char_list)
                    char_Ids.append(char_Id)

                label = pairs[-1]
                label_Id = label_alphabet.get_index(label)
                # # get features
                feat_list = []
                feat_Id = []
                for idx in range(feature_num):
                    feat_idx = pairs[idx + 1].split(']', 1)[-1]
                    feat_list.append(feat_idx)
                    feat_Id.append(feature_alphabets[idx].get_index(feat_idx))
                # # combine together and return, notice the feature/label as different format with sequence labeling task
                if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
                    instence_texts.append([words, feat_list, chars, label])
                    instence_Ids.append([word_Ids, feat_Id, char_Ids, label_Id])
                words = []
                features = []
                chars = []
                char_Ids = []
                word_Ids = []
                feature_Ids = []
                label_Ids = []
        if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
            instence_texts.append([words, feat_list, chars, label])
            instence_Ids.append([word_Ids, feat_Id, char_Ids, label_Id])
            words = []
            features = []
            chars = []
            char_Ids = []
            word_Ids = []
            feature_Ids = []
            label_Ids = []

    else:
        # ## for sequence labeling data format i.e. CoNLL 2003
        for line in in_lines:
            if len(line) > 2:
                pairs = line.strip().split()
                word = pairs[0]
                if sys.version_info[0] < 3:
                    word = word.decode('utf-8')
                words.append(word)
                if number_normalized:
                    word = normalize_word(word)
                label = pairs[-1]
                labels.append(label)
                word_Ids.append(word_alphabet.get_index(word))
                label_Ids.append(label_alphabet.get_index(label))
                # # get features
                feat_list = []
                feat_Id = []
                for idx in range(feature_num):
                    feat_idx = pairs[idx + 1].split(']', 1)[-1]
                    feat_list.append(feat_idx)
                    feat_Id.append(feature_alphabets[idx].get_index(feat_idx))
                features.append(feat_list)
                feature_Ids.append(feat_Id)
                # # get char
                char_list = []
                char_Id = []
                # 添加音节切分方法
                if '_' in word:
                    w_word = word.split('_')[0]
                    syllables = w_word.split('་')
                    for syllable in syllables:
                        if syllable != '':
                            char_list.append(syllable)
                else:
                    syllables = word.split('་')
                    for syllable in syllables:
                        if syllable != '':
                            char_list.append(syllable)

                # for char in word:
                #     char_list.append(char)
                if char_padding_size > 0:
                    char_number = len(char_list)
                    if char_number < char_padding_size:
                        char_list = char_list + [char_padding_symbol] * (char_padding_size - char_number)
                    assert (len(char_list) == char_padding_size)
                else:
                    # ## not padding
                    pass
                for char in char_list:
                    char_Id.append(char_alphabet.get_index(char))
                chars.append(char_list)
                char_Ids.append(char_Id)
            else:
                if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
                    instence_texts.append([words, features, chars, labels])
                    instence_Ids.append([word_Ids, feature_Ids, char_Ids, label_Ids])
                words = []
                features = []
                chars = []
                labels = []
                word_Ids = []
                feature_Ids = []
                char_Ids = []
                label_Ids = []
        if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
            instence_texts.append([words, features, chars, labels])
            instence_Ids.append([word_Ids, feature_Ids, char_Ids, label_Ids])
            words = []
            features = []
            chars = []
            labels = []
            word_Ids = []
            feature_Ids = []
            char_Ids = []
            label_Ids = []
    return instence_texts, instence_Ids

def read_origin_sentence(token_list, word_alphabet, char_alphabet, feature_alphabets, label_alphabet,
                  number_normalized, max_sent_length, default_tag,
                  char_padding_size=-1, char_padding_symbol='</pad>'):
    feature_num = len(feature_alphabets)
    if feature_num > 0:
        in_lines = forecast_pre_data(token_list, default_tag)
    else:
        in_lines = convert_sentence_2_conll(token_list, default_tag)  # 添加初始化标签 S-Y
    instence_texts = []
    instence_Ids = []
    words = []
    features = []
    chars = []
    labels = []
    word_Ids = []
    feature_Ids = []
    char_Ids = []
    label_Ids = []

    # ## for sequence labeling data format i.e. CoNLL 2003
    for line in in_lines:
        if len(line) > 2:
            pairs = line.strip().split()
            word = pairs[0]
            if sys.version_info[0] < 3:
                word = word.decode('utf-8')
            words.append(word)
            if number_normalized:
                word = normalize_word(word)
            label = pairs[-1]
            labels.append(label)
            word_Ids.append(word_alphabet.get_index(word))
            label_Ids.append(label_alphabet.get_index(label))
            # # get features
            feat_list = []
            feat_Id = []
            for idx in range(feature_num):
                feat_idx = pairs[idx + 1].split(']', 1)[-1]
                feat_list.append(feat_idx)
                feat_Id.append(feature_alphabets[idx].get_index(feat_idx))
            features.append(feat_list)
            feature_Ids.append(feat_Id)
            # # get char
            char_list = []
            char_Id = []
            # for char in word:
            #     char_list.append(char)
            # 在这里添加了藏文音节切分方法
            if '_' in word:
                w_word = word.split('_')[0]
                syllables = w_word.split('་')
                for syllable in syllables:
                    if syllable != '':
                        char_list.append(syllable)
            else:
                syllables = word.split('་')
                for syllable in syllables:
                    if syllable != '':
                        char_list.append(syllable)

            if char_padding_size > 0:
                char_number = len(char_list)
                if char_number < char_padding_size:
                    char_list = char_list + [char_padding_symbol] * (char_padding_size - char_number)
                assert (len(char_list) == char_padding_size)
            else:
                # ## not padding
                pass
            for char in char_list:
                char_Id.append(char_alphabet.get_index(char))
            chars.append(char_list)
            char_Ids.append(char_Id)
        else:
            if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
                instence_texts.append([words, features, chars, labels])
                instence_Ids.append([word_Ids, feature_Ids, char_Ids, label_Ids])
            elif len(words) >= max_sent_length:
                instence_texts.append([words[0:max_sent_length], features[0:max_sent_length], chars[0:max_sent_length], labels[0:max_sent_length]])
                instence_Ids.append([word_Ids[0:max_sent_length], feature_Ids[0:max_sent_length], char_Ids[0:max_sent_length], label_Ids[0:max_sent_length]])

            words = []
            features = []
            chars = []
            labels = []
            word_Ids = []
            feature_Ids = []
            char_Ids = []
            label_Ids = []
    if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
        instence_texts.append([words, features, chars, labels])
        instence_Ids.append([word_Ids, feature_Ids, char_Ids, label_Ids])
    elif len(words) >= max_sent_length:
        instence_texts.append([words[0:max_sent_length], features[0:max_sent_length], chars[0:max_sent_length],
                               labels[0:max_sent_length]])
        instence_Ids.append([word_Ids[0:max_sent_length], feature_Ids[0:max_sent_length], char_Ids[0:max_sent_length],
                             label_Ids[0:max_sent_length]])

        words = []
        features = []
        chars = []
        labels = []
        word_Ids = []
        feature_Ids = []
        char_Ids = []
        label_Ids = []
    return instence_texts, instence_Ids

def convert_conll_segment_2_single_line(text_lines):
    sentence = ''
    new_list = text_lines.split('  ')
    for i, line in enumerate(new_list):
        line = line.strip()
        if len(line) == 0:
            continue
        else:
            try:
                token_list = line.split(' ')
                if len(token_list) == 2:
                    if token_list[1].startswith('S'):
                        sentence += ' [ ' + token_list[0] + ' ]' + token_list[1].split('-')[1]
                    elif token_list[1].startswith('B'):
                        sentence += ' [ ' + token_list[0] + ' '
                    elif token_list[1].startswith('I'):
                        sentence += token_list[0] + ' '
                    elif token_list[1].startswith('E'):
                        sentence += token_list[0] + ' ]' + token_list[1].split('-')[1]
                    elif token_list[1].startswith('O'):
                        sentence += ' [ ' + token_list[0] + ' ]' + token_list[0].split('_')[1]
            except Exception:
                print(new_list)
                print(token_list)
    return sentence

# 构建预处理嵌入
def build_pretrain_embedding(embedding_path, word_alphabet, embedd_dim=100, norm=True):
    embedd_dict = dict()
    if embedding_path != None:
        embedd_dict, embedd_dim = load_pretrain_emb(embedding_path)
    alphabet_size = word_alphabet.size()
    scale = np.sqrt(3.0 / embedd_dim)
    pretrain_emb = np.empty([word_alphabet.size(), embedd_dim])
    perfect_match = 0
    case_match = 0
    not_match = 0
    for word, index in word_alphabet.iteritems():
        if word in embedd_dict:
            if norm:
                pretrain_emb[index, :] = norm2one(embedd_dict[word])
            else:
                pretrain_emb[index, :] = embedd_dict[word]
            perfect_match += 1
        elif word.lower() in embedd_dict:
            if norm:
                pretrain_emb[index, :] = norm2one(embedd_dict[word.lower()])
            else:
                pretrain_emb[index, :] = embedd_dict[word.lower()]
            case_match += 1
        else:
            pretrain_emb[index, :] = np.random.uniform(-scale, scale, [1, embedd_dim])
            not_match += 1
    pretrained_size = len(embedd_dict)
    print("Embedding:\n     pretrain word:%s, prefect match:%s, case_match:%s, oov:%s, oov%%:%s" % (
    pretrained_size, perfect_match, case_match, not_match, (not_match + 0.) / alphabet_size))
    return pretrain_emb, embedd_dim


def norm2one(vec):
    root_sum_square = np.sqrt(np.sum(np.square(vec)))
    return vec / root_sum_square


def load_pretrain_emb(embedding_path):
    embedd_dim = -1
    embedd_dict = dict()
    with open(embedding_path, 'r', encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                continue
            tokens = line.split()
            if embedd_dim < 0:
                embedd_dim = len(tokens) - 1
            elif embedd_dim + 1 != len(tokens):
                # # ignore illegal embedding line
                continue
                # assert (embedd_dim + 1 == len(tokens))
            embedd = np.empty([1, embedd_dim])
            embedd[:] = tokens[1:]
            if sys.version_info[0] < 3:
                first_col = tokens[0].decode('utf-8')
            else:
                first_col = tokens[0]
            embedd_dict[first_col] = embedd
    return embedd_dict, embedd_dim


if __name__ == '__main__':
    a = np.arange(9.0)
    print(a)
    print(norm2one(a))

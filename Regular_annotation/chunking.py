# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2022/12/29 21:55
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2022/12/29 21:55

"""
原始句子，切分组块
"""
from Utils import utils as us


# import utils as us

class Case_chunking:
    """
    对藏文句子在虚词、动词位置进行切分，从而实现一种粗颗粒度的组块切分
        在虚词中不包含 gi 属格助词
    """
    def __init__(self, sentence):
        self.sentence = sentence
        self.case = ['ls', 'lg', 'lt', 'ld', 'lh', 'jg', 'bo', 'ba', 'bc', 'by', 'bg', 'cv', 'cl', 'cn',
                     'ci', 'ck', 'ca', 'ct', 'cc', 'cg', 'ce', 'cs', 'cy', 'cr', 'cj',
                     'cp', 'cq', 'fh', 'fz', 'fj', 'cu']  # 'cd', 'cm', 'rf','cf', 'cz', 'fg',
        self.case_c = ['cv', 'cl', 'cn', 'cd', 'ci', 'ck', 'ca', 'ct', 'cc', 'cf', 'cz', 'cu', 'cg', 'ce', 'cs',
                       'cm', 'cy', 'cr', 'cj', 'cp', 'cq', 'fh', 'fg', 'fz', 'fj', 'rf', 'ci', 'rz']
        self.verb_label = ['vt', 'vi', 'vj', 'vc', 'ad']
        self.chun_str = []
        self.words = sentence.split(' ')
        self.word_list, self.label_list = us.word_label(self.words)
        self.v_index = self.verb_index()
        self.verb_chunk = self.verb_chunking()
        for verb_c in self.verb_chunk:
            word_list_c, label_list_c = us.word_label(verb_c.strip().split(' '))
            self.c_index = self.caes_index(label_list_c)
            self.chun_str.append(self.chunking(verb_c.strip().split(' ')))
        self.chunk_list = self.blocking_mark()

    def caes_index(self, label_list):
        """
        标记格助词的索引
        :param label_list: 词性标记列表
        :return: 返回标注格助词的索引位置
        """
        c_index = []
        for l in label_list:
            if l == '':
                continue
            if l in self.case:
                c_index.append('c')
            else:
                c_index.append('o')
        return c_index

    def chunking(self, words):
        """
        按格助词切分
        :return: 组块列表，标记串
        """
        chunking_list = []
        chunk_str = ''
        for i in range(0, len(self.c_index)):
            if self.c_index[i] == 'c':
                chunk_str += words[i] + ' '
                chunking_list.append(chunk_str)
                chunk_str = ''
            else:
                chunk_str += words[i] + ' '
        if chunk_str != '':
            chunking_list.append(chunk_str)
        return chunking_list

    def verb_chunking(self):
        """
        按动词分块儿
        :return: 返回块列表
        """
        chunking_list = []
        chunk_str = ''
        for i in range(0, len(self.v_index)):
            if self.v_index[i] == 'c':
                chunking_list.append(chunk_str)
                chunk_str = ''
                chunk_str += self.words[i] + ' '
            else:
                chunk_str += self.words[i] + ' '
        chunking_list.append(chunk_str)
        return chunking_list

    def verb_index(self):
        """
        标记动词索引
        :return: 返回标注动词的索引位置
        """
        v_index = []
        for l in self.label_list:
            if l in self.verb_label:
                v_index.append('c')
            else:
                v_index.append('o')
        return v_index

    def blocking_mark(self):
        """
        组块在源列表中的索引标注
        :return: 返回标记的组块列表
        """
        chunk_list = []
        start = 0
        end = 0
        for chunk_l in self.chun_str:
            for chunk in chunk_l:
                chunk = chunk.strip()
                if len(chunk_list) == 0:
                    end = start + len(chunk.split(' ')) - 1
                else:
                    start = end + 1
                    end = end + len(chunk.split(' '))
                label = chunk[len(chunk)-2:]
                chunk_list.append([chunk, start, end, label])
        return chunk_list
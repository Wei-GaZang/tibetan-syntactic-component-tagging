# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2023/1/14 18:46
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2023/1/14 18:46

from Utils import utils as us


class MatchProcessing:
    def __init__(self, component_labels, chunk_list):
        self.component_labels = component_labels
        self.chunk_list = chunk_list
        self.case = ['bo', 'cl', 'ci', 'ls', 'ba', 'by', 'bg', 'bc', 'lt', 'lh', 'ld', 'lg', 'jg', 'cq', 'ct', 'ww',
                     'vu', 'us', 'uu', 'ud', 'uq', 'cy']

        self.supplement()

    def un_case_marker(self):
        for chunk in self.chunk_list:
            if chunk[-1] not in self.case:
                print(chunk)
                self.numeral_phrase(chunk)

    def numeral_phrase(self, chunk):
        word_list, label_list = us.word_label(chunk[0].strip().split(' '))
        for i, l in enumerate(label_list):
            if l in ['as', 'mj', 'mx', 'mg', 'pj', 'qg', 'ql', 'qb', 'qc']:  # ad 待考证
                if len(label_list) - 1 != i:
                    if label_list[i + 1] in ['as', 'mj', 'mx', 'mg', 'pj', 'qg', 'ql', 'qb', 'qc']:  # 'rr'
                        label_list[i + 1] = 'atr'

    def supplement(self):
        un_mark, sub_bool, hed = self.check_sentence_pattern()
        if un_mark:
            if hed == 'vt':
                for i, com in enumerate(self.component_labels):
                    if com[-1] == 'O':
                        self.component_labels[i][-1] = 'obj'
            elif hed == 'vi':
                for i, com in enumerate(self.component_labels):
                    if com[-1] == 'O':
                        if sub_bool:
                            self.component_labels[i][-1] = 'obj'
                        else:
                            self.component_labels[i][-1] = 'sub'
            elif hed == 'vj':
                for i, com in enumerate(self.component_labels):
                    if com[-1] == 'O':
                        if sub_bool:
                            self.component_labels[i][-1] = 'obj'
                        else:
                            self.component_labels[i][-1] = 'sub'
            elif hed == 'vc':
                for i, com in enumerate(self.component_labels):
                    if com[-1] == 'O':
                        if sub_bool:
                            self.component_labels[i][-1] = 'obj'
                        else:
                            self.component_labels[i][-1] = 'sub'
            elif hed == 'ad':
                for i, com in enumerate(self.component_labels):
                    if com[-1] == 'O':
                        if sub_bool:
                            self.component_labels[i][-1] = 'obj'
                        else:
                            self.component_labels[i][-1] = 'sub'
            else:
                pass

    def check_sentence_pattern(self):
        sub_bool = False
        hed = None
        un_mark = False
        for com in self.component_labels:
            if com[-1] == 'sub':
                sub_bool = True
            elif com[-1] == 'hed':
                hed = com[-2]
            elif com[-1] == 'O':
                un_mark = True
        return un_mark, sub_bool, hed

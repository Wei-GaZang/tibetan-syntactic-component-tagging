# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2023/1/7 17:22
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2023/1/7 17:22
from Utils import utils as us


class complement:
    def __init__(self, component_labels, chunk_list):
        self.component_labels = component_labels
        self.chunk_list = chunk_list
        self.case_com = ['vu', 'us', 'uu', 'ud', 'uq', 'cy']
        self.pre_label = ['vt', 'vi', 'vc', 'vj', 'ad']
        self.tagging()

    def tagging(self):
        for chunk in self.chunk_list:
            _, label_list = us.word_label(chunk[0].split(' '))
            if label_list[0] in self.pre_label:
                self.dimensions_in_tagging(chunk, 'com')

    def dimensions_in_tagging(self, chunk, tag):
        for l in range(chunk[1], chunk[2]):
            if self.component_labels[l][2] in self.case_com:  # self.component_labels[l][3] == 'O' and
                self.component_labels[l][3] = tag

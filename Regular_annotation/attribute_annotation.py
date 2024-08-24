# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2023/1/3 15:07
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2023/1/3 15:07

"""
实现标注定语
有属格助词的前置定语
通格助词的后置定语
"""

from Utils import utils as us


class Attribute:

    def __init__(self, component_labels, chunk_list):
        self.component_labels = component_labels
        self.chunk_list = chunk_list
        self.tagging()


    def tagging(self):
        for chunk in self.chunk_list:
            word_list, label_list = us.word_label(chunk[0].strip().split(' '))
            if 'gi' in label_list:
                index = us.end_index(label_list, 'gi')
                self.dimensions_in_tagging(chunk, index, 'atr')


    def dimensions_in_tagging(self, chunk, index, tag):
        for l in range(0, index):
            if self.component_labels[chunk[1] + l][3] == 'O':
                self.component_labels[chunk[1] + l][3] = tag

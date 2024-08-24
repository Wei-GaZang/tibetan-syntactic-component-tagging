# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2023/1/7 0:09
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2023/1/7 0:09

class Verb_tagging(object):

    def __init__(self, component_labels, chunk_list):
        self.component_labels = component_labels
        self.chunk_list = chunk_list
        self.pre_label = ['vt', 'vi', 'vc', 'vj', 'ad']
        self.tagging()


    def count_verb(self):
        pre_count = 0
        for ponent in self.component_labels:
            if ponent[2] in self.pre_label:
                pre_count += 1
        # print(pre_count)
        return pre_count

    def tagging(self):
        per_count = self.count_verb()
        if per_count == 0:
            pass
        elif per_count == 1:
            self.single()

    def single(self):
        for i, com in enumerate(self.component_labels):
            if com[2] in self.pre_label:
                self.component_labels[i][3] = 'hed'
            elif com[2] == 'ww':
                self.component_labels[i][3] = 'ww'
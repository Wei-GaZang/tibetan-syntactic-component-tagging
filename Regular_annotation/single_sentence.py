# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2022/12/29 23:42
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2022/12/29 23:42

class Single:
    def __init__(self, component_labels, chunk_list):
        self.case_sub = ['bo', 'cl', 'ci']
        self.case_obj = ['ls']
        self.case_adv = ['ba', 'by', 'bg', 'bc', 'lt', 'lh', 'ld', 'lg', 'jg', 'cq', 'ct']  #
        self.adv_tag = ['dc', 'dp', 'dw', 'dx', 'dl', 'nt']

        self.component_labels = component_labels
        self.chunk_list = chunk_list
        self.tagging()
        self.adverbial_tag()

    def tagging(self):
        for chunk in self.chunk_list:
            if chunk[-1] in self.case_adv:
                self.dimensions_in_tagging(chunk, 'adv')
            elif chunk[-1] in self.case_obj:
                self.dimensions_in_tagging(chunk, 'obj')
            elif chunk[-1] in self.case_sub:
                self.dimensions_in_tagging(chunk, 'sub')


    def dimensions_in_tagging(self, chunk, tag):
        for l in range(chunk[1], chunk[2]):
            if self.component_labels[l][3] == 'O':
                self.component_labels[l][3] = tag
        self.component_labels[chunk[2]][3] = chunk[-1]

    def adverbial_tag(self):
        for i, com in enumerate(self.component_labels):
            if com[2] in self.adv_tag:
                self.component_labels[i][3] = 'adv'
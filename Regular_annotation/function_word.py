# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2023/1/11 21:01
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2023/1/11 21:01

class Function:
    def __init__(self, component_labels, chunk_list):
        self.component_labels = component_labels
        self.chunk_list = chunk_list
        self.function_word = ['rz', 'rf', 'ry', 'cv', 'cn', 'cb', 'ck', 'cd', 'ca', 'ct', 'cc', 'cf', 'cz', 'cu', 'cg',
                         'ce', 'cs', 'cm', 'cy', 'cr', 'cj', 'cp', 'cq', 'df', 'fh', 'fg', 'fz', 'fj']
        self.tagging()

    def tagging(self):
        for i, com in enumerate(self.component_labels):
            if com[2] in self.function_word:
                self.component_labels[i][3] = com[2]
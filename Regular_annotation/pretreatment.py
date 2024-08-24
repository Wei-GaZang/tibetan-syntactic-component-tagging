# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2022/12/30 10:12
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2022/12/30 10:12


class Pretreatment:
    # 待标注句子
    sentence = ''
    # 句法成分标记等数据结构
    component_labels = []
    # 格助词
    case = ['ls', 'lg', 'lt', 'ld', 'lh', 'jg', 'bo', 'ba', 'bc', 'by', 'bg', 'cl', 'gi']

    def __init__(self, ti_sentence):
        """
        预处理
        :param ti_sentence: 待分析的句子
        """
        self.sentence = ti_sentence
        # print(self.sentence)
        words = self.sentence.split(' ')
        # 句法成分标记等数据结构
        self.component_labels.clear()
        try:
            for word in words:
                if word == '':
                    continue
                chars = word.split('_')
                if chars[1] in self.case:
                    self.component_labels.append([word, chars[0], chars[1], chars[1]])
                else:
                    self.component_labels.append([word, chars[0], chars[1], 'O'])
        except IndexError:
            print(ti_sentence)

    # 检查句中是否有动词 返回动词数量
    def predicate(self):
        """
        vt:及物动词
        vi:不及物动词
        vc:判断动词
        vj:存在动词
        vu:助动词
        检查句中是否有动词
        :return: 返回动词数量
        """
        pre_label = ['vt', 'vi', 'vc', 'vj', 'ad']
        pre_tes = 0
        v_label = ''
        for l in self.component_labels:
            if l[2] in pre_label:
                pre_tes += 1
                v_label = l[2]
        return pre_tes, v_label

    # 在list中查找某个标记，返回索引
    def inspect_label(self, tab, start, end):
        """
        返回该标记在list中第一次出现的下标，没有则返回-1
        :param tab: 标记
        :param start: 开始下标
        :param end: 结束下标
        :return: 返回该标记的下标
        """
        sub_index = -1
        for bo in range(start, end):
            if self.component_labels[bo][2] == tab:
                sub_index = bo
                break
        return sub_index

    # 输出标记结果
    def output_output(self):
        label_sentance = '[ '
        single = self.component_labels[0][3]
        for i in range(len(self.component_labels)):
            if single != self.component_labels[i][3] and single != '[':
                label_sentance += ']' + single + ' [ ' + self.component_labels[i][0] + ' '
                single = self.component_labels[i][3]
            else:
                label_sentance += self.component_labels[i][0] + ' '
                single = self.component_labels[i][3]
        label_sentance += ']' + self.component_labels[len(self.component_labels) - 1][3]
        return label_sentance


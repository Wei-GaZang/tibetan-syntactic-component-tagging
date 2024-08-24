# -*- coding: utf-8 -*-
# @Author: WeiRiWa
# @Date:   2022/12/30 10:27
# @Last Modified by:   WeiRiWa,     Contact: 2697112431@qq.com
# @Last Modified time: 2022/12/30 10:27

case_sub = ['bo', 'cl', 'ci', 'cr', 'cj', 'cp']
case_obj = ['ls']
case_adv = ['ba', 'by', 'bc', 'lg', 'lt', 'lh', 'ld', 'jg', 'cp', 'cb']
case_art = ['gi']

def chunking_tagging(chunk_list, component_labels):
    new_chunk_list = []
    for chunk in chunk_list:
        if chunk[-1] in case_sub:
            chunk[-1] = 'sub'
            for i in range(chunk[1], chunk[2]+1):
                component_labels[i][3] = 'sub'
        elif chunk[-1] in case_obj:
            chunk[-1] = 'obj'
            for i in range(chunk[1], chunk[2]+1):
                component_labels[i][3] = 'obj'
        elif chunk[-1] in case_adv:
            chunk[-1] = 'adv'
            for i in range(chunk[1], chunk[2]+1):
                component_labels[i][3] = 'adv'
        elif chunk[-1] == 'ww':
            chunk[-1] = 'hed'
            for i in range(chunk[1], chunk[2]+1):
                component_labels[i][3] = 'hed'
        else:
            pass
        new_chunk_list.append(chunk)
    return new_chunk_list, component_labels
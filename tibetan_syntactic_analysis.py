# -*- coding: utf-8 -*-
import argparse
from utils.data import Data
import torch
from utils.functions import *
from model.seqlabel import SeqLabel
import main

class TibetanSyntacticComponent():
    def __init__(self, config_file_syntactic_component):
        self.data_syntactic_info = Data()
        print("Begin to initialize the parameter and model for syntactic component")

        self.data_syntactic_info.read_config(config_file_syntactic_component)
        print("Load Model from file: ", self.data_syntactic_info.dset_dir)
        new_model_dir = str(self.data_syntactic_info.load_model_dir)
        print("Load Model from file: ", new_model_dir)
        self.data_syntactic_info.load(self.data_syntactic_info.dset_dir)
        self.data_syntactic_info.HP_gpu = torch.cuda.is_available()
        self.data_syntactic_info.HP_batch_size = 16
        self.data_syntactic_info.show_data_summary()

        self.model_syntactic_component = SeqLabel(self.data_syntactic_info)

        if torch.cuda.is_available():
            self.model_syntactic_component.load_state_dict(torch.load(new_model_dir, map_location=torch.device('cuda')))
        else:
            self.model_syntactic_component.load_state_dict(torch.load(new_model_dir, map_location=torch.device('cpu')))

    def tag(self, sentence):
        self.data_syntactic_info.generate_instance_from_origin_str_for_syntactic_component(sentence, default_segment_tag='S-Y')
        _, _, _, _, _, pred_results, _ = main.evaluate(self.data_syntactic_info, self.model_syntactic_component, "raw", None)
        syntactic_component_conll = self.data_syntactic_info.write_decoded_results_into_string(pred_results)
        tagged_result = convert_conll_segment_2_single_line(syntactic_component_conll)
        return tagged_result

    def tag_file(self, input_file_name, output_file_name):
        try:
            with open(input_file_name, 'r', encoding='utf-8') as in_file, open(output_file_name, 'w', encoding='utf-8') as output_file:
                line_number = 0
                for each_line in in_file:
                    each_line = each_line.strip()
                    if len(each_line) == 0:
                        continue
                    line_number += 1

                    if len(each_line) > 0:
                        tagged_result = self.tag(each_line)
                        if line_number % 1000 in range(2):
                            print(f'{line_number}行：\n {each_line}')
                            print(tagged_result)
                        output_file.write(tagged_result + '\n')
        except Exception:
            print(line_number)
            print(each_line)
            exit()


if __name__ == '__main__':
    # 初始化参数分析器
    parser = argparse.ArgumentParser(description='Tuning with NCRF++')
    parser.add_argument('--config_analysis', help='Configuration File for Syntactic analysis',
                        default='demo.online.config')

    args = parser.parse_args()

    # 构造分析器
    lexicalAnalyzer = TibetanSyntacticComponent(args.config_analysis)

    # 调用示例
    sentence = "མཇུག་_nf ཏུ་_lh ང_rr ས་_bo ད་ལྟ_nt འི་_gi བློ་ལྡན་_nn ཕལ་བ་_as རྣམས་_qj ལ་_ls བཤད་_vt རྒྱུ་_us །_ww"
    while sentence.strip() != 'exit':
        tagged_result = lexicalAnalyzer.tag(sentence)
        print("Result: ", tagged_result)
        sentence = input("Enter your input: ")

    # input_file_name = r'G:\WeiRiWa\TibetanCorpus\句子抽取语料\data\Extracted_sentences_51133.txt'
    # output_file_name = r'G:\pythonProject\sequence\NCRFpp\sample_data\12.27_Extracted_sentences_51133.rule'
    #
    # lexicalAnalyzer.tag_file(input_file_name, output_file_name)
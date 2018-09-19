# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 10:42:06 2018

@author: fuhua
"""

import nltk
from nltk.corpus import stopwords
class Tokens(object):
    def __init__(self):
        #创建一个去除标点符号等特殊字符的正则表达式分词器
        self.tokenizer = nltk.RegexpTokenizer('[0-9a-zA-Z]+')
        
    def vocab(self, sentence):
        if sentence == None:
            return None
        #读取sentence的内容，并分词，形成list类型
        token = self.tokenizer.tokenize(sentence)
        
        words = [w.lower() for w in token]  #将tokens中的单词改成小写
        vocab = [w for w in words if(w not in stopwords.words('english'))]  #去除停用词
#        vsort = sorted(set(vocab))  #获取不重复的单词，并排序            
#        tag  = nltk.pos_tag(filtered)  #标注词性
        return vocab




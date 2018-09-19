# -*- coding: utf-8 -*-
"""
Created on Thu May 10 15:40:46 2018

@author: fuhua
"""

#----------------------------------------------------------------------
import os,re
import nltk
import nltk.tree
   
from nltk.tree   import Tree
from nltk.parse  import stanford

#----------------------------------------------------------------------
class StanParser(object):
    def __init__(self):
        #添加stanford环境变量,此处需要手动修改，jar包地址为绝对地址。
        os.environ['STANFORD_PARSER'] = 'D:/practicePython/stanford-parser-full-2018-02-27/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = 'D:/practicePython/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar'

        #为JAVAHOME添加环境变量
        java_path = "D:/Program Files/Java/jdk1.8.0_131/bin"
        os.environ['JAVAHOME'] = java_path
        
        self.parser = stanford.StanfordParser(model_path="D:/practicePython/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    #----------------------------------------------------------------------
    #将段落(字符串)拆分成句子(字符串数组)
    ##############################################################################
    ###############              小故事               ############################
    #吉尼斯世界记录是属于美国著名作家乔伊斯(James Joyce)的名著《尤利西斯》(Ulysses)，
    #被称为"一部二十世纪最伟大的英语小说"。这本书英文版的第十八章全章只有两个标点符号，
    #在第四句和第八句结尾的句号。如果按八句算，那么最长的句子有4391个词。
    #如果按两句算，那么最长的句子有12931个词。
    #英国作家Jonathan Coe在2001年出版的小说《腐烂者俱乐部》(The Rotters' Club)，
    #书中有一句话有13955个词。
    ##############################################################################
    def splitSentence(self, paragraph):  
        filteredsen = []
        para=re.sub(r'\\|\/|\'|\"', " ", paragraph)#去除斜杠/反斜杠\单引号‘双引号“
        para=re.sub(r';+', ";", para)#多个分号变一个分号
        para=re.sub(r',+', ",", para)#多个逗号变一个逗号
        para=re.sub(r'\s+', " ", para)#将连续多个空白字符(如\t\n\r\f)换成一个空格
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')#不好使，有些句子分不开
        sentences = tokenizer.tokenize(para)  
#        sentences = para.split('. ')#暴力分句，简单可靠。注意是（点+空格）
        
        for sentence in sentences:
            words = nltk.tokenize.WordPunctTokenizer().tokenize(sentence)
            if len(words)<100:#正常的、有意义的句子小于100个单词
                filteredsen.append(sentence)
            else:#对于长度超过100的非正常句子，每70个元素生成一个句子（句子越短，parser运行越快）
                sl = len(words)//70
                for r in range(sl):
                    sen = " ".join( words[r*70:(r+1)*70] )
                    filteredsen.append(sen)
                if len(words)%70 != 0:
                    sen = " ".join( words[sl*70:] )
                    filteredsen.append(sen)
        return filteredsen
    #----------------------------------------------------------------------
    #句法标注
    def syntaxTag(self, paragraph):
        sentences = self.splitSentence(paragraph)#将段落(字符串)拆分成句子(字符串数组)
        nlist = ['','','','']#储存最终结果
        for sentence in sentences:
#            print(sentence)
#            print('sen length= ',len(sentence.split()))
#            print('-----------------------')
            #一次处理一个个语句，返回单层iterator
            #不要使用'raw_parse_sents()',防止句子过多，内存溢出
            if sentence.strip(): 
                syntaxes  = self.parser.raw_parse( sentence ) 
                for syntax in syntaxes:
                    for p in self.pp(syntax):
                        if   p[0]=='for':#获得for介词短语，作为知识属性Cause
#                           print('Cause:', p)
                            nlist[0] += (",".join(p)+",")
                        elif p[0]=='to':#获得to介词短语，作为知识属性Motivation
#                           print('Motivation:', p)
                            nlist[1] += (",".join(p)+",")
                        else :#获得除for和to以外的所有介词短语，作为知识属性Scenarios
#                           print('Scenarios:', p)
                            nlist[2] += (",".join(p)+",")
                    
                    np = self.notpp(syntax)#获得除介词以外的所有词汇，作为问(答)上下文
#                   print('Context:', np)
                    nlist[3] += (",".join(np)+",")
#        print(nlist)
        return nlist
    #----------------------------------------------------------------------
    #输出所有'PP'(介词短语)的叶子节点
    def pp(self, tree):
        p = []
        for child in tree:
            if (isinstance(child,Tree) and child.label() != 'PP'):
                p.extend(self.pp(child))
            elif(isinstance(child,Tree)):
                p.append(child.leaves())
        return p
    #----------------------------------------------------------------------
    #输出除了'PP'(介词短语)以外的叶子节点
    def notpp(self, tree):
        np = []
        for child in tree:
            if (isinstance(child,Tree) and child.label() != 'PP'):
                np.extend(self.notpp(child))
            elif(not isinstance(child,Tree)):
                np.append(child)
        return np    





# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:19:19 2018

@author: fuhua
"""

import spacy
import en_core_web_sm
from spacy import displacy

nlp=en_core_web_sm.load()
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
"""Doc被处理 - 例如分成单独的单词和注释 - 它仍然保留原始文本的所有信息，如空格字符。
您可以随时将令牌的偏移量转换为原始字符串，或者通过加入令牌及其尾随的空格来重建原始值。
这样，使用spaCy处理文本时就不会丢失任何信息。"""

#2 符号化
"""在处理过程中，spaCy首先对文本进行标记，即将其分割成单词，标点符号等等。
这是通过应用特定于每种语言的规则来完成的。
例如，句子末尾的标点符号应该分开 - 而“英国”应该保持一个标记。
每个Doc都由单独的令牌组成，我们可以简单地迭代它们："""
for token in doc:
    print(token.text)

# 3词性标注和依赖关系
"""标记后，spaCy可以解析和标记给定的Doc。这就是统计模型出现的地方，
这使得spaCy能够预测哪种标签或标签最有可能适用于这种情况。一个模型由二进制数据组成，
并且通过向系统展示足够的例子来产生在语言上进行概括的预测来产生 
- 例如，在英语之后的一个单词最有可能是一个名词。"""

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)
displacy.serve(doc, style='dep')
"""打开浏览器，输入http://localhost:5000/，就可以看到结果了"""
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:14:43 2018

@author: fuhua
"""

# coding:utf-8
 
# 2.0 使用jieba进行分词,彻底放弃低效的NLPIR,用TextRank算法赋值权重(实测textrank效果更好)
# 2.1 用gensim搞tfidf
# 2.2 sklearn做tfidf和kmeans
# 2.3 将kmeans改成BIRCH,使用传统tfidf
 
import os,sys,time,codecs
import jieba
import glob
#import gensim
#from gensim import corpora,similarities, models
from pprint import pprint
import jieba.analyse

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import Birch

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

start = time.clock()
 
'''#----------------------------------------#'
  '#                                        #'
  '#               载入语料库                #'
  '#                                        #'
  '#----------------------------------------#'''
def PreprocessDoc(root):
    print( '开始载入语料库:')
    allDirPath = [] # 存放语料库中所有文件的绝对路径
    
    g = os.walk(root)
    for par_dir, _, files in g:
        for file in files:
            filepath = os.path.join(par_dir, file)
            allDirPath.append(filepath)

    
    totalFileNum = len(allDirPath)
    print( '总文件数为: ' + str(totalFileNum))
 
    return allDirPath

'''#----------------------------------------#'
  '#                                        #'
  '#             分词+去停用词               #'
  '#                                        #'
  '#----------------------------------------#'''
def DeleteStopWords(data, stopWords):
 
    wordList = []
 
    # 先分一下词
    cutWords = jieba.cut(data)
    for item in cutWords:
        if item not in stopWords: # 分词编码要和停用词编码一致
            wordList.append(item)
 
    return wordList
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#              合成语料文档               #'
  '#                                        #'
  '#----------------------------------------#'''
 
# 每个文档一行,第一个词是这个文档的类别
 
def SaveDoc(allDirPath, docPath, stopWords):
 
    print( '开始合成语料文档:')    
    with codecs.open(docPath,'w') as f:# 把所有的文本都集合在这个文档里
        for filePath in allDirPath:     
            data = codecs.open(filePath, 'rb').read()
            texts = DeleteStopWords(data, stopWords)
            line = '' # 把这些词缩成一行,第一个位置是文档类别,用空格分开
            for word in texts:
                if word == '\n' or word == 'nbsp' or word == '\r\n':
                    continue
                line += word
                line += ' '
            f.write(line + '\n') # 把这行写进文件
    return 0 # 生成文档,不用返回值
 
 
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#                 tf-idf                 #'
  '#                                        #'
  '#----------------------------------------#'''
def TFIDF(docPath):
 
    print( '开始tfidf:')
 
    corpus = [] # 文档语料
 
    with codecs.open(docPath,'r') as f:# 读取语料,一行语料为一个文档
        lines = f.readlines()
    for line in lines:
        corpus.append(line.strip()) # strip()前后空格都没了,但是中间空格还保留
 
    # 将文本中的词语转换成词频矩阵,矩阵元素 a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
 
    # 该类会统计每个词语tfidf权值
    transformer = TfidfTransformer()
 
    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
 
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
 
    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    print( weight)

    # # 输出所有词
    # result = open(docPath, 'w')
    # for j in range(len(word)):
    #     result.write(word[j].encode('utf-8') + ' ')
    # result.write('\r\n\r\n')
    #
    # # 输出所有权重
    # for i in range(len(weight)):
    #     for j in range(len(word)):
    #         result.write(str(weight[i][j]) + ' ')
    #     result.write('\r\n\r\n')
    #
    # result.close()
    return weight
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#                   PCA                  #'
  '#                                        #'
  '#----------------------------------------#'''
def pPCA(weight, dimension):
 
    print( '开始进行PCA主成分分析:')
 
    print( '原有维度: ', len(weight[0]))
    print( '开始降维:')
 
    pca = PCA(n_components=dimension) # 初始化PCA
    X = pca.fit_transform(weight) # 返回降维后的数据
    print( '降维后维度: ', len(X[0]))
    print( X)
 
    return X
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#                 k-means                #'
  '#                                        #'
  '#----------------------------------------#'''
def kmeans(X, k): # X=weight
 
    print( '开始K-Means聚类:')
 
    clusterer = KMeans(n_clusters=k, init='k-means++') # 设置聚类模型
 
    # X = clusterer.fit(weight) # 根据文本向量fit
    # print( X)
    # print( clf.cluster_centers_)
 
    # 每个样本所属的簇
    y = clusterer.fit_predict(X) # 把weight矩阵扔进去fit一下,输出label
    print( y)
 
    # i = 1
    # while i <= len(y):
    #     i += 1
 
    # 用来评估簇的个数是否合适,距离约小说明簇分得越好,选取临界点的簇的个数
    # print( clf.inertia_)
 
    return y
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#                 BIRCH                 #'
  '#                                        #'
  '#----------------------------------------#'''
def birch(X, k): # 待聚类点阵,聚类个数
 
    print( '开始BIRCH聚类:')
 
    clusterer = Birch(n_clusters=k)
 
    y = clusterer.fit_predict(X)
    print( '输出聚类结果:')
    print( y)
 
    return y
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#                轮廓系数                 #'
  '#                                        #'
  '#----------------------------------------#'''
def Silhouette(X, y):
 
    from sklearn.metrics import silhouette_samples, silhouette_score
 
    print( '计算轮廓系数:')
 
    silhouette_avg = silhouette_score(X, y) # 平均轮廓系数
    sample_silhouette_values = silhouette_samples(X, y) # 每个点的轮廓系数
 
    pprint(silhouette_avg)
 
    return silhouette_avg, sample_silhouette_values
 
 
'''#----------------------------------------#'
  '#                                        #'
  '#                  画图                  #'
  '#                                        #'
  '#----------------------------------------#'''
def Draw(silhouette_avg, sample_silhouette_values, y, k):

    print( '开始画图:')
    
    # 创建一个 subplot with 1-row 2-column
    fig, ax1 = plt.subplots(1)
    fig.set_size_inches(18, 7)
 
    # 第一个 subplot 放轮廓系数点
    # 范围是[-1, 1]
    ax1.set_xlim([-0.2, 0.5])
 
    # 后面的 (k + 1) * 10 是为了能更明确的展现这些点
    ax1.set_ylim([0, len(X) + (k + 1) * 10])
 
    y_lower = 10
 
    for i in range(k): # 分别遍历这几个聚类
 
        ith_cluster_silhouette_values = sample_silhouette_values[y == i]
        ith_cluster_silhouette_values.sort()
 
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i
 
        color = cm.nipy_spectral(float(i)/k) # 搞一款颜色
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0,
                          ith_cluster_silhouette_values,
                          facecolor=color,
                          edgecolor=color,
                          alpha=0.7) # 这个系数不知道干什么的
 
        # 在轮廓系数点这里加上聚类的类别号
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
 
        # 计算下一个点的 y_lower y轴位置
        y_lower = y_upper + 10
 
    # 在图里搞一条垂直的评论轮廓系数虚线
    ax1.axvline(x=silhouette_avg, color='red', linestyle="--")
 
    plt.show()
 
 
 
 
 
 
if __name__ == "__main__":
    
    root = 'D:/practicePython/sensitivefactors/cluster/SogouCorpus-ch'
    docPath = 'D:/practicePython/sensitivefactors/cluster/doc.txt'
    
    with codecs.open('D:/practicePython/sensitivefactors/cluster/stopwords.dat', 'r', encoding='utf-8') as f:# 把所有的文本都集合在这个文档里
        stopWords = f.read().split()
        
    k = 3 #聚类数量：3
 
    allDirPath = PreprocessDoc(root)
    SaveDoc(allDirPath, docPath, stopWords)
 
    weight = TFIDF(docPath)
    X = pPCA(weight, dimension=0.8) # 将原始权重数据降维
    # y = kmeans(X, k) # y=聚类后的类标签
    y = birch(X, k)
    silhouette_avg, sample_silhouette_values = Silhouette(X, y) # 轮廓系数
    Draw(silhouette_avg, sample_silhouette_values, y, k)
 
 
end = time.clock()
print( '运行时间: ' + str(end - start))

'''----------* 测试文件编码格式 *-------------'''
#import chardet
#path = 'D:/practicePython/sensitivefactors/cluster/doc.txt'
#f = open(path,'rb')
#data = f.read()
#print(chardet.detect(data)) 
 
 
 

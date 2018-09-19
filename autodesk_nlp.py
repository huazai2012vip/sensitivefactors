# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:49:45 2018

@author: fuhua
"""
import re
import pymysql # 导入pymysql驱动
from stanparser import StanParser
from tokens import Tokens
#----------------------------------------------------------------------
#创建数据库连接
conn   = pymysql.connect(host='localhost', port=3306, user='root',passwd='sa',
                         db='info',charset='utf8')
#创建游标
cursor = conn.cursor(cursor=pymysql.cursors.Cursor)
#执行查询操作，返回符合条件的记录数
#count  = cursor.execute('SELECT * from autodesk ORDER BY Id ASC LIMIT 30')
count  = cursor.execute('SELECT * from autodesk ORDER BY Id ASC')
#count  = cursor.execute('SELECT * from autodesk where Id=375580')#如果报错的话，找到出错时数据库对应的Id，单独测试
sp = StanParser()#初始化一次，节省内存
tk = Tokens()#初始化一次，节省内存
#----------------------------------------------------------------------
#i=0#测试用的计数变量，先检验若干个输出是否正确； 然后去掉，完整运行。

try:
##############################################################################
    #只获取第一条用fetchone()，全部获取必须用fetchall()
    results = cursor.fetchall()
    for result in results:
        if result[0] >= 375580:
#            print(result[4])
            nlist = sp.syntaxTag( result[4] )#将post_context拆分成知识属性
    
            res = [result[0],result[1],result[3]]+nlist+[result[5],
                   result[6],result[7],result[8]]#将所有字段合并到一起，方便数据库操作
            
            res[0] = str(res[0])#原autodesk表中'item_id'为int属性，现在改成str属性
            for i in range(2,7):
                #将字段中的句子分词，去除停用词和符号.并将其变为字符串
                res[i]=",".join( tk.vocab(res[i]) )
            print(res)
            
            
            cursor.execute('''
            insert into autodesk_nlp (item_id,post_id,nlp_title,nlp_cause,nlp_motivation,
            nlp_scenarios,nlp_context,post_author,post_datetime,post_degree,post_likes) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            , res)
            
            conn.commit()# 提交事务
            print('-----------------------')
            
    del(results)
##############################################################################
####如果报错的话，找到出错时数据库对应的Id，用该段代码测试StanParser，Tokens
#    count  = cursor.execute('SELECT * from autodesk where Id=309542')
#    results = cursor.fetchall()
#    sentences = results[0][4]
#    print(sentences)
#    print('------------------------------')
#    sen=re.sub(r'\\|\/|\'|\"', " ", sentences)
#    print(sen)
#    print('------------------------------')
#    pa    = sp.splitSentence(sen)
#    print(pa) 
#    print('------------------------------')
#    nlist = ['','','','']#储存最终结果
#    for sentence in pa:
#        print(sentence)
#        print('------------------------------')
#        if sentence.strip():     
#            if len(sentence.split(' '))<100:
#                syntaxes  = sp.parser.raw_parse( sentence ) 
#                for syntax in syntaxes:
#                    np = sp.notpp(syntax)#获得除介词以外的所有词汇，作为问(答)上下文
#                    nlist[3] += (",".join(np)+",")
#    print(nlist[3])
#    print('------------------------------')
#    vc=",".join( tk.vocab(nlist[3]) )
#    print(vc)
#    print('------------------------------')
#    del(results)
 ##############################################################################
   
finally:
    
    # 关闭Cursor和Connection:
    cursor.close()
    conn.close()
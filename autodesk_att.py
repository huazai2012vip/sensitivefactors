# -*- coding: utf-8 -*-
"""
Created on Tue May 15 20:21:31 2018

@author: fuhua
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:49:45 2018

@author: fuhua
"""

import pymysql # 导入pymysql驱动
import time
#----------------------------------------------------------------------
#创建数据库连接
conn   = pymysql.connect(host='localhost', port=3306, user='root',passwd='sa',
                         db='info',charset='utf8')
#创建游标
cursor = conn.cursor(cursor=pymysql.cursors.Cursor)

#----------------------------------------------------------------------
i=0 #测试用的计数变量，先检验若干个输出是否正确； 然后去掉，完整运行。

try:
##############################################################################
#    ##执行查询操作，返回符合条件的记录数
#    count  = cursor.execute('SELECT * from autodesk ORDER BY Id ASC LIMIT 30')
#
#    #只获取第一条用fetchone()，全部获取必须用fetchall()
#    results = cursor.fetchall()
#    timesort=[]
#    for result in results:
#        s=result[6][1:]#提取时间字符串，并去掉'\u200e'这一开头,使其符合time格式
#        t = time.mktime(time.strptime(s, '%m-%d-%Y %H:%M %p'))
#        timesort.append(t)
#    print(timesort)
#    print('-----------------------')
#    ts = sorted(timesort)
#    for t in ts:
#        timestruct = time.localtime(t)
#        print( time.strftime('%m-%d-%Y %H:%M %p', timestruct) )
#    print('-----------------------')
##############################################################################
#    sql="""
#    SELECT item_id,post_id,nlp_title,nlp_context,nlp_cause,nlp_motivation,nlp_scenarios,
#    min(post_datetime) 
#    from autodesk_nlp_copy GROUP BY post_id
#    """
#    count  = cursor.execute(sql)
#    results = cursor.fetchall()
#    for result in results:
#        print(result)
#        sql="""
#            INSERT INTO autodesk_att(IID,PID,EP,PC,PR,PM,PS,ST)
#            values (%s,%s,%s,%s,%s,%s,%s,%s);"""
#        count  = cursor.execute(sql,list(result))
#        conn.commit()# 提交事务
##############################################################################
    
    sql="""SELECT IID,PID FROM autodesk_att;"""
    count1  = cursor.execute(sql)
    results1 = cursor.fetchall()
    
    for result1 in results1:
        iid=result1[0]
        pid=result1[1]
        sql="""
            SELECT item_id,post_id,nlp_context,nlp_cause,nlp_motivation,nlp_scenarios,post_author 
            FROM autodesk_nlp_copy WHERE post_id="""+pid+";"
        count2  = cursor.execute(sql)
        results2 = cursor.fetchall()
#        print(results2)
        for result2 in results2:
            if result2[0] != iid:
#                print(result2)
                sql="UPDATE autodesk_att SET SC='"+result2[2]+"',SR='"+result2[3]+ \
                "',SM='"+result2[4]+"',SS='"+result2[5]+"',SI='"+result2[6]+"' WHERE PID="+pid+";"
                print(sql)
                count  = cursor.execute(sql)
                conn.commit()# 提交事务



    del(results1,results2)
finally:
    
    # 关闭Cursor和Connection:
    cursor.close()
    conn.close()



# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:41:19 2018
@author: fuhua
"""
import networkx as nx
import matplotlib.pyplot as plt

'''无向图'''
##例1
#G = nx.Graph()#建立一个空的无向图G
#G.add_node(1)#添加一个节点1
#G.add_nodes_from([2,3])#添加节点集合
#G.add_edge(2,3)#添加一条边2-3(隐含着添加了两个节点2,3)
#G.add_edge(3,2)#对于无向图，边3-2与边2-3被认为是一条边
#print('nodes:', G.nodes())#输出全部的节点：[1,2,3]
#print('edges:', G.edges())#输出全部的边  ：[(2,3)]
#print('number of edges:',G.number_of_edges())#输出边的数量：1
#nx.draw(G)
#plt.savefig('wuxiangtu-e1.jpg')
#plt.show()

'''有向图'''
##例2
#G = nx.DiGraph()
#G.add_node(1)#添加节点1
#G.add_node(2)#添加节点2
#G.add_nodes_from([3,4,5,6])#添加节点集合
#G.add_cycle([1,2,3,4])#添加环
#G.add_edge(1,3)#添加边
#G.add_edges_from([(3,5),(3,6),(6,7)])#添加边集合
#nx.draw(G, pos=nx.shell_layout(G), with_labels = True)
#plt.savefig('youxiangtu-e2.jpg')
#plt.show()

'''有向图转无向图'''
##例3
#G = nx.DiGraph()
#G.add_node(1,index='1th')
#G.add_node(2)
#G.add_nodes_from([3,4,5,6])
#G.add_cycle([1,2,3,4])
#G.add_edge(1,3)
#G.add_edges_from([(3,5),(3,6),(6,7)])
#G = G.to_undirected()
#nx.draw(G, pos=nx.circular_layout(G), with_labels = True)#在一个圆环上均匀分布
#plt.savefig('wuxiangtu-e3.jpg')
#plt.show()

'''通过指定节点名称构建有向图'''
#例4
G = nx.DiGraph()
#road_nodes = {'a': 1, 'b': 2, 'c': 3}
road_nodes = {'a':{1:1}, 'b':{2:2}, 'c':{3:3}}
road_edges = [('a', 'b'), ('b', 'c')]
G.add_nodes_from(road_nodes.items())
G.add_edges_from(road_edges)
nx.draw(G, pos=nx.shell_layout(G), with_labels = True)#在同心圆上分布
plt.savefig("youxiangtu-e4.jpg")
plt.show()

'''多中心放射状的图形'''
#例5
G = nx.random_graphs.barabasi_albert_graph(150,1)   #生成一个BA无标度网络G
nx.draw(G, pos=nx.spring_layout(G), with_labels = True) #多中心放射状                         #绘制网络G
plt.savefig("wuxiangtu-e5.jpg")           #输出方式1: 将图像存为一个png格式的图片文件
plt.show()                            #输出方式2: 在窗口中显示这幅图像

'''加权图
有向图和无向图都可以给边赋予权重，用到的方法是add_weighted_edges_from，
它接受1个或多个三元组[u,v,w]作为参数，其中u是起点，v是终点，w是权重。'''
#例6
G = nx.Graph()







# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-23 19:24:54
# @Last Modified by:   lock
# @Last Modified time: 2017-12-23 19:41:34
import math
import numpy as np
from matplotlib import pyplot
from collections import Counter
import warnings
# K最近邻算法
# 两个分组时k值取3，3个分组时k值取5...
 
# k-Nearest Neighbor算法
def k_nearest_neighbors(data, predict, k=3):
 
    if len(data) >= k:
        warnings.warn("k is too small")
 
    # 计算predict点到各点的距离
    distances = []
    for group in data:
        for features in data[group]:
            #euclidean_distance = np.sqrt(np.sum((np.array(features)-np.array(predict))**2))   # 计算欧拉距离，这个方法没有下面一行代码快
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([euclidean_distance, group])
 
    sorted_distances =[i[1]  for i in sorted(distances)]
    top_nearest = sorted_distances[:k]
 
    #print(top_nearest)  ['red','black','red'] 出现次数最多，返回一个TopN列表。如果n没有被指定，则返回所有元素。当多个元素计数值相同时，排列是无确定顺序的。
    group_res = Counter(top_nearest).most_common(1)[0][0]
    confidence = Counter(top_nearest).most_common(1)[0][1]*1.0/k
    # confidences是对本次分类的确定程度，例如(red,red,red)，(red,red,black)都分为red组，但是前者显的更自信
    return group_res, confidence
 
if __name__=='__main__':
 
    dataset = {'black':[ [1,2], [2,3], [3,1] ], 'red':[ [6,5], [7,7], [8,6] ]}
    new_features = [3.5,5.2]  # 判断这个样本属于哪个组
 
    for i in dataset:
        for ii in dataset[i]:
            pyplot.scatter(ii[0], ii[1], s=50, color=i)
 
    #两个分组时k值取3，3个分组时k值取5
    which_group,confidence = k_nearest_neighbors(dataset, new_features, k=3)
    print(which_group, confidence)
 
    #s表示点的大小
    pyplot.scatter(new_features[0], new_features[1], s=300, color=which_group)
 
    pyplot.show()
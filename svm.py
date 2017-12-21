# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-12-21 09:58:01
# @Last Modified by:   lock
# @Last Modified time: 2017-12-21 17:41:07
# 分类算法之SVM,比KNN算法更加复杂
# demo最简单的线性可分离数据
# 参考：http://blog.csdn.net/lisi1129/article/details/70209945?locationNum=8&fps=1

import numpy as np
from matplotlib import pyplot
import math
import sys
 
class SVM(object):
    def __init__(self, visual=True):
        self.visual = visual
        self.colors = {1:'r', -1:'b'}
        if self.visual:
            self.fig = pyplot.figure()
            self.ax = self.fig.add_subplot(1,1,1)
 
    def train(self, data):
        self.data = data
        opt_dict = {}
    
        transforms = [[1,1],
                      [-1,1],
                      [-1,-1],
                      [1,-1]]
                      
        # 找到数据集中最大值和最小值
        self.max_feature_value = float('-inf')   # 正无穷
        self.min_feature_value = float('inf')    # 负无穷
        for y in self.data:
            for features in self.data[y]:
                for feature in features:
                    if feature > self.max_feature_value:
                        self.max_feature_value = feature
                    if feature < self.min_feature_value:
                        self.min_feature_value = feature
        print(self.max_feature_value, self.min_feature_value)
        
        # 和梯度下降一样，定义每一步的大小；开始快，然后慢，越慢越耗时
        step_sizes = [self.max_feature_value * 0.1, self.max_feature_value * 0.01, self.max_feature_value * 0.001]
        
        b_range_multiple = 5
        b_multiple = 5
        lastest_optimum = self.max_feature_value * 10
        
        for step in step_sizes:
            w = np.array([lastest_optimum,lastest_optimum])
            optimized = False
            while not optimized:
                for b in np.arange(self.max_feature_value*b_range_multiple*-1, self.max_feature_value*b_range_multiple, step*b_multiple):
                    for transformation in transforms:
                        w_t = w * transformation
                        found_option = True
                        for i in self.data:
                            for x in self.data[i]:
                                y = i
                                if not y*(np.dot(w_t, x)+b) >= 1:
                                    found_option = False
                                #print(x,':',y*(np.dot(w_t, x)+b))  逐渐收敛
                                    
                        if found_option:
                            opt_dict[np.linalg.norm(w_t)] = [w_t,b]
 
                if w[0] < 0:
                    optimized = True
                else:
                    w = w - step
        
            norms = sorted([n for n in opt_dict])
            opt_choice = opt_dict[norms[0]]
            self.w = opt_choice[0]
            self.b = opt_choice[1]
            print(self.w, self.b)
            lastest_optimum = opt_choice[0][0] + step*2
 

    def predict(self, features):
        classification = np.sign( np.dot(features, self.w) + self.b )
        
        if classification != 0 and self.visual:
            self.ax.scatter(features[0], features[1], s=300, marker='*', c=self.colors[classification])
 
        return classification
 
 
    # 显示picture
    def visualize(self):
        for i in self.data:
            for x in self.data[i]:
                self.ax.scatter(x[0], x[1], s=50, c=self.colors[i])
 
        # 超平面
        def hyperplane(x,w,b,v):
            return (-w[0]*x-b+v) / w[1]
 
        data_range = (self.min_feature_value*0.9, self.max_feature_value*1.1)
 
        hyp_x_min = data_range[0]
        hyp_x_man = data_range[1]
 
        psv1 = hyperplane(hyp_x_min, self.w, self.b, 1)
        psv2 = hyperplane(hyp_x_man, self.w, self.b, 1)
        self.ax.plot([hyp_x_min, hyp_x_man], [psv1, psv2], c=self.colors[1])
 
        nsv1 = hyperplane(hyp_x_min, self.w, self.b, -1)
        nsv2 = hyperplane(hyp_x_man, self.w, self.b, -1)
        self.ax.plot([hyp_x_min, hyp_x_man], [nsv1, nsv2], c=self.colors[-1])
 
        db1 = hyperplane(hyp_x_min, self.w, self.b, 0)
        db2 = hyperplane(hyp_x_man, self.w, self.b, 0)
        self.ax.plot([hyp_x_min, hyp_x_man], [db1, db2], 'y--')
 
        pyplot.show()
 
if __name__ == '__main__':
    data_set = {-1:np.array([[1,7],
                             [2,8],
                             [3,8]]),
                 1:np.array([[5,1],
                             [6,-1],
                             [7,3]])}
    print(data_set)
 
    svm = SVM()
    svm.train(data_set)
 
    # 预测
    for predict_feature in [[0,10],[2,6],[1,3], [4,3], [5.5,7.5], [8,3]]:
        print(svm.predict(predict_feature))
 
    svm.visualize()


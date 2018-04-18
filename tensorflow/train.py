#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2018/3/18 14:48

import tensorflow as tf
import os, numpy as np
from datetime import datetime
from create_captcha_img import CAPTCHA_LIST, CAPTCHA_WIDTH, CAPTCHA_HEIGHT, CAPTCHA_LEN
from create_captcha_img import get_random_captcha_text_and_image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def weight_variable(shape, w_alpha=0.01):
    """
    增加噪音,随机生成权重
    :param shape:
    :param w_alpha:
    :return: Tensor , shape仍然是[batch, height, width, channels]这种形式
    """
    initial = w_alpha * tf.random_normal(shape)
    return tf.Variable(initial)


def bias_variable(shape, b_alpha=0.01):
    """
    增加噪音，随机生成偏置项
    :param shape:
    :param b_alpha:
    :return: Tensor , shape仍然是[batch, height, width, channels]这种形式
    """
    initial = b_alpha * tf.random_normal(shape)
    return tf.Variable(initial)


def conv2d(input, filter):
    """
    实现卷积的函数
    局部变量线性组合，部长为1，模式same代表卷积后图片尺寸不变，即零边距
    https://www.cnblogs.com/qggg/p/6832342.html
    :param input: 具体含义是[训练时一个batch的图片数量, 图片高度, 图片宽度, 图像通道数],Tensor
    :param filter: 具体含义是[卷积核的高度，卷积核的宽度，图像通道数，卷积核个数],Tensor
    :return: Tensor , shape仍然是[batch, height, width, channels]这种形式
    """
    # 第三个参数strides：卷积时在图像每一维的步长，这是一个一维的向量，长度4
    # http://blog.csdn.net/wuzqChom/article/details/74785643 SAME与VALID的区别
    return tf.nn.conv2d(input, filter, strides=[1, 1, 1, 1], padding='SAME')


def max_pool(val):
    """
    池化操作，max pooling是CNN当中的最大值池化操作，其实用法和卷积很类似
    http://blog.csdn.net/mao_xiao_feng/article/details/53453926
    :param val:一般池化层接在卷积层后面，所以输入通常是feature map，依然是[batch, height, width, channels]这样的shape
    :return: Tensor , shape仍然是[batch, height, width, channels]这种形式
    """
    # ksize池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]，因为我们不想在batch和channels上做池化，所以这两个维度设为了1
    # strides：和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]
    return tf.nn.max_pool(val, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def cnn_graph(x, keep_prob, size, captcha_list=CAPTCHA_LIST, captcha_len=CAPTCHA_LEN):
    """
    三层卷积神经网络计算图
    :param x:
    :param keep_prob:
    :param size:
    :param captcha_list:
    :param captcha_len:
    :return:
    """
    # 图片reshape为4维向量
    image_height, image_width = size
    # http://blog.csdn.net/lxg0807/article/details/53021859 reshape介绍
    x_image = tf.reshape(x, shape=[-1, image_height, image_width, 1])

    # 第一层 ,filter定义为3x3x1， 输出32个特征, 即32个filter
    w_conv1 = weight_variable([3, 3, 1, 32])
    b_conv1 = bias_variable([32])
    # rulu激活函数 （
    # 一种函数（例如 ReLU 或 S 型函数），用于对上一层的所有输入求加权和，然后生成一个输出值）
    # （通常为非线性值），并将其传递给下一层。
    h_conv1 = tf.nn.relu(tf.nn.bias_add(conv2d(x_image, w_conv1), b_conv1))
    # 池化
    h_pool1 = max_pool(h_conv1)
    # dropout防止过拟合
    h_drop1 = tf.nn.dropout(h_pool1, keep_prob)

    # 第二层
    w_conv2 = weight_variable([3, 3, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(tf.nn.bias_add(conv2d(h_drop1, w_conv2), b_conv2))
    h_pool2 = max_pool(h_conv2)
    h_drop2 = tf.nn.dropout(h_pool2, keep_prob)

    # 第三层
    w_conv3 = weight_variable([3, 3, 64, 64])
    b_conv3 = bias_variable([64])
    h_conv3 = tf.nn.relu(tf.nn.bias_add(conv2d(h_drop2, w_conv3), b_conv3))
    h_pool3 = max_pool(h_conv3)
    h_drop3 = tf.nn.dropout(h_pool3, keep_prob)

    # 全连接层
    image_height = int(h_drop3.shape[1])
    image_width = int(h_drop3.shape[2])
    w_fc = weight_variable([image_height * image_width * 64, 1024])
    b_fc = bias_variable([1024])
    h_drop3_re = tf.reshape(h_drop3, [-1, image_height * image_width * 64])
    h_fc = tf.nn.relu(tf.add(tf.matmul(h_drop3_re, w_fc), b_fc))
    h_drop_fc = tf.nn.dropout(h_fc, keep_prob)

    # 输出层
    w_out = weight_variable([1024, len(captcha_list) * captcha_len])
    b_out = bias_variable([len(captcha_list) * captcha_len])
    y_conv = tf.add(tf.matmul(h_drop_fc, w_out), b_out)
    return y_conv


def optimize_graph(y, y_conv):
    '''
    优化计算图
    :param y:
    :param y_conv:
    :return:
    '''
    # 交叉熵计算loss 注意logits输入是在函数内部进行sigmod操作
    # sigmod_cross适用于每个类别相互独立但不互斥，如图中可以有字母和数字
    # softmax_cross适用于每个类别独立且排斥的情况，如数字和字母不可以同时出现
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=y_conv, labels=y))
    # 最小化loss优化
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)
    return optimizer


def accuracy_graph(y, y_conv, width=len(CAPTCHA_LIST), height=CAPTCHA_LEN):
    '''
    偏差计算图
    :param y:
    :param y_conv:
    :param width:
    :param height:
    :return:
    '''
    # 这里区分了大小写 实际上验证码一般不区分大小写
    # 预测值
    predict = tf.reshape(y_conv, [-1, height, width])
    max_predict_idx = tf.argmax(predict, 2)
    # 标签
    label = tf.reshape(y, [-1, height, width])
    max_label_idx = tf.argmax(label, 2)
    correct_p = tf.equal(max_predict_idx, max_label_idx)
    # reduce_mean求tensor中平均值
    accuracy = tf.reduce_mean(tf.cast(correct_p, tf.float32))
    return accuracy


def convert2gray(img):
    '''
    图片转为黑白，3维转1维
    :param img:
    :return:
    '''
    if len(img.shape) > 2:
        img = np.mean(img, -1)
    return img


def text2vec(text, captcha_len=CAPTCHA_LEN, captcha_list=CAPTCHA_LIST):
    '''
    验证码文本转为向量
    :param text:
    :param captcha_len:
    :param captcha_list:
    :return: vector
    '''
    text_len = len(text)
    if text_len > captcha_len:
        raise ValueError('验证码最长4个字符')
    vector = np.zeros(captcha_len * len(captcha_list))
    for i in range(text_len):
        vector[captcha_list.index(text[i]) + i * len(captcha_list)] = 1
    return vector


def vec2text(vec, captcha_list=CAPTCHA_LIST, size=CAPTCHA_LEN):
    '''
    验证码向量转为文本
    :param vec:
    :param captcha_list:
    :param size:
    :return:
    '''
    # if np.size(np.shape(vec)) is not 1:
    #     raise ValueError('向量限定为1维')
    # vec = np.reshape(vec, (size, -1))
    # vec_idx = np.argmax(vec, 1)
    vec_idx = vec
    text_list = [captcha_list[v] for v in vec_idx]
    return ''.join(text_list)


def wrap_gen_captcha_text_and_image(shape=(60, 160, 3)):
    '''
    返回特定shape图片
    :param shape:
    :return:
    '''
    while True:
        t, im = get_random_captcha_text_and_image()
        if im.shape == shape:
            return t, im


def next_batch(batch_count=60, width=CAPTCHA_WIDTH, height=CAPTCHA_HEIGHT):
    '''
    获取训练图片组
    :param batch_count:
    :param width:
    :param height:
    :return:
    '''
    # np.zeros()返回来一个给定形状和类型的用0填充的数组；
    batch_x = np.zeros([batch_count, width * height])
    batch_y = np.zeros([batch_count, CAPTCHA_LEN * len(CAPTCHA_LIST)])
    for i in range(batch_count):
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2gray(image)
        # 将图片数组一维化 同时将文本也对应在两个二维组的同一行
        batch_x[i, :] = image.flatten() / 255
        batch_y[i, :] = text2vec(text)
    # 返回该训练批次
    return batch_x, batch_y


def start_train(height=CAPTCHA_HEIGHT, width=CAPTCHA_WIDTH, y_size=len(CAPTCHA_LIST) * CAPTCHA_LEN):
    """
    cnn 训练
    :param height:
    :param width:
    :param y_size:
    :return:
    """
    acc_rate = 0.95
    # 按照图片大小申请占位符
    x = tf.placeholder(tf.float32, [None, height * width])  # (这里的None表示此张量的第一个维度可以是任何长度的)
    y = tf.placeholder(tf.float32, [None, y_size])
    # 防止过拟合 训练时启用 测试时不启用 （过拟合是指为了得到一致假设而使假设变得过度严格）
    keep_prob = tf.placeholder(tf.float32)
    # cnn模型
    y_conv = cnn_graph(x, keep_prob, (height, width))
    # 最优化
    optimizer = optimize_graph(y, y_conv)
    # 偏差
    accuracy = accuracy_graph(y, y_conv)
    # 启动会话.开始训练
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    step = 0
    while 1:
        batch_x, batch_y = next_batch(64)
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: 0.75})
        # 每训练一百次测试一次
        if step % 100 == 0:
            batch_x_test, batch_y_test = next_batch(100)
            acc = sess.run(accuracy, feed_dict={x: batch_x_test, y: batch_y_test, keep_prob: 1.0})
            print(datetime.now().strftime('%c'), ' step:', step, ' accuracy:', acc)
            # 偏差满足要求，保存模型
            if acc > acc_rate:
                model_path = os.getcwd() + os.sep + str(acc_rate) + "captcha.model"
                saver.save(sess, model_path, global_step=step)
                acc_rate += 0.01
                if acc_rate > 0.99:
                    break
        step += 1
    sess.close()


if __name__ == "__main__":
    start_train()

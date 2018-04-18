#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2018/3/18 17:26

import tensorflow as tf
from train import cnn_graph
from train import get_random_captcha_text_and_image
from train import vec2text, convert2gray
from create_captcha_img import CAPTCHA_LIST, CAPTCHA_WIDTH, CAPTCHA_HEIGHT, CAPTCHA_LEN


def captcha_to_text(image_list, height=CAPTCHA_HEIGHT, width=CAPTCHA_WIDTH):
    '''
    验证码图片转化为文本
    :param image_list:
    :param height:
    :param width:
    :return:
    '''
    x = tf.placeholder(tf.float32, [None, height * width])
    keep_prob = tf.placeholder(tf.float32)
    y_conv = cnn_graph(x, keep_prob, (height, width))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint('.'))
        predict = tf.argmax(tf.reshape(y_conv, [-1, CAPTCHA_LEN, len(CAPTCHA_LIST)]), 2)
        vector_list = sess.run(predict, feed_dict={x: image_list, keep_prob: 1})
        vector_list = vector_list.tolist()
        text_list = [vec2text(vector) for vector in vector_list]
        return text_list[0]


def multi_test(height=CAPTCHA_HEIGHT, width=CAPTCHA_WIDTH):
    x = tf.placeholder(tf.float32, [None, height * width])
    keep_prob = tf.placeholder(tf.float32)
    y_conv = cnn_graph(x, keep_prob, (height, width))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint('.'))
        while 1:
            text, image = get_random_captcha_text_and_image()
            image = convert2gray(image)
            image = image.flatten() / 255
            image_list = [image]
            predict = tf.argmax(tf.reshape(y_conv, [-1, CAPTCHA_LEN, len(CAPTCHA_LIST)]), 2)
            vector_list = sess.run(predict, feed_dict={x: image_list, keep_prob: 1})
            vector_list = vector_list.tolist()
            text_list = [vec2text(vector) for vector in vector_list]
            pre_text = text_list[0]
            flag = u'错误'
            if text == pre_text:
                flag = u'正确'
            print u"实际值(actual):%s, 预测值(predict):%s, 预测结果:%s" % (text, pre_text, flag,)


if __name__ == '__main__':
    try:
        # 多个测试
        multi_test()
        exit()

        text, image = get_random_captcha_text_and_image()
        image = convert2gray(image)
        image = image.flatten() / 255
        pre_text = captcha_to_text([image])
        flag = u'错误'
        if text == pre_text:
            flag = u'正确'
        print u"实际值(actual):%s, 预测值(predict):%s, 预测结果:%s" % (text, pre_text, flag,)
    except KeyboardInterrupt as e:
        print e.message

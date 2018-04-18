#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2018/3/18 13:25

import string
import random
from captcha.image import ImageCaptcha
from PIL import Image
import numpy as np
import os

CAPTCHA_HEIGHT = 60  # 验证码高度
CAPTCHA_WIDTH = 160  # 验证码宽度
CAPTCHA_LEN = 4  # 验证码长度
# CAPTCHA_LIST = [str(i) for i in range(0, 10)] + list(string.ascii_letters)  # 验证码字符列表
CAPTCHA_LIST = [str(i) for i in range(0, 10)]  # 验证码字符列表,改小一点的访问,提高速度


def get_random_captcha_text(char_set=CAPTCHA_LIST, length=CAPTCHA_LEN):
    captcha_text = [random.choice(char_set) for _ in range(length)]
    return ''.join(captcha_text)


def get_random_captcha_text_and_image(width=CAPTCHA_WIDTH, height=CAPTCHA_HEIGHT, save=None):
    image = ImageCaptcha(width=width, height=height)
    captcha_text = get_random_captcha_text()
    captcha = image.generate(captcha_text)
    if save:
        image.write(captcha_text, 'image/' + captcha_text + '.jpg')
    captcha_image = Image.open(captcha)
    # 转化为np数组
    captcha_image_np = np.array(captcha_image)
    return captcha_text, captcha_image_np


if __name__ == "__main__":
    if os.path.exists('image') is False:
        os.mkdir('image')

    while 1:
        text, np_data = get_random_captcha_text_and_image(CAPTCHA_WIDTH, CAPTCHA_HEIGHT, 1)
        print text

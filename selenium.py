# -*- coding: utf-8 -*-
# @Author: lock
# @Date:   2017-04-04 01:40:22
# @Last Modified by:   lock
# @Last Modified time: 2017-04-04 23:38:09
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class BaiduSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_lock(self):
        driver = self.driver
        driver.get("http://www.baidu.com")
        self.assertIn(u"百度一下", driver.title)
        elem = driver.find_element_by_id("kw")
        elem.send_keys("lock")
        elem.send_keys(Keys.RETURN)
        i = 0
        while 1:
               if i>=2:
                    break
               time.sleep(1)
               i+=1
               print "not test %s , wait %s second continue ..." % ('lock',i,)

    def test_search(self):
        driver = self.driver
        driver.get("http://www.baidu.com")
        self.assertIn(u"百度一下", driver.title)
        elem = driver.find_element_by_id("kw")
        elem.send_keys("php")
        elem.send_keys(Keys.RETURN)
        i = 0
        while 1:
               if i>=2:
                    break
               time.sleep(1)
               i+=1
               print "not test %s , wait %s second continue ..." % ('php',i,)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
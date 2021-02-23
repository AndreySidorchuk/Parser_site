from selenium import webdriver
import time


url = "https://notariat.ru/ru-ru/"
driver = webdriver.Chrome(executable_path="C:\\Users\\Андрей\\PycharmProjects\\Parser_site\\chromedriver\\chromedriver.exe")

# class NalogParser(object):
#
#
#     def __init__(self,driver,lang):
#         self.driver = driver
#         self.lang = lang
#
#     def parse(self):
#         self.go_to_tests_page()
#
#     def go_to_tests_page(self):
#         self.driver.get("https://proghub.ru/tests")
#         slide_elems = self.driver.find_elements_by_class_name("test-slider-inner")
#         for elem in slide_elems:
#             print(elem.get_attribute)('href')
try:
    driver.get(url=url)
    time.sleep(5)
    elems = driver.find_elements_by_class_name("public-records__item-text")
    for elem in elems:
        print(elem.get_attribute("href"))
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

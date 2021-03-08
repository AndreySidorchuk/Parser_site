from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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
    time.sleep(2)
    window_before = driver.window_handles[0]
    # driver.find_element_by_link_text("Реестр наследственных дел").click()
    # elem = driver.find_elements_by_xpath("//span[@class='public-records__item-text']//*[contains(text(), 'Реестр наследственных дел')]")
    # elem = driver.find_element_by_css_selector('span.public-records__item-text')
    # elem = driver.find_element_by_css_selector('div.public-records__item>a[href="//notariat.ru/ru-ru/help/probate-cases/"]')
    # elem = driver.find_element_by_xpath("//a[@class=public-records__item-text']ontent'][@href='//notariat.ru/ru-ru/help/probate-cases/']")
    # elem = driver.find_element_by_xpath('//a[span="Поиск по сайту"]')
    elem = driver.find_element_by_xpath('/html/body/div/main/div[3]/div[2]')
    ActionChains(driver).move_to_element(elem).click(elem).perform()
    time.sleep(8)
    window_after = driver.window_handles[2]
    driver.switch_to.window(window_after)
    time.sleep(2)
    name = driver.find_element_by_name('name')
    ActionChains(driver).move_to_element(name).send_keys("Иванов Иван Иванович").perform()
    time.sleep(4)
    day = driver.find_element_by_xpath("//a[span='День']")
    ActionChains(driver).move_to_element(day).click(day).perform()
    time.sleep(3)
    month = driver.find_element_by_xpath('//a[span="Месяц"]')
    ActionChains(driver).move_to_element(month).click(month).perform()
    time.sleep(3)
    # select = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.select[name="b-month"]'))))
    # numbers_month = select.select_by_value("02")
    # select = Select(EC.element_to_be_clickable((By.NAME, "")))
    # numbers_month = driver.find_element_by_xpath("//input[@name='b-month']")
    # numbers_month.send_keys("Февраль")
    # driver.find_element_by_xpath('//select[@name="b-month"]/option[@value="01"]').click()
    # months = Select(driver.find_element(By.NAME("b-month")))
    months = driver.find_element_by_xpath('/html/body/div/main/div[1]/div[2]/section/section/div[1]/form/div[1]/div[1]/div[2]/div/label[2]/select/option[3]')
   # number_month = months.select_by_visible_text("Январь")
    time.sleep(2)
    driver.switch_to.active_element(months)
    print('opa')
    month.click()
    time.sleep(2)
    # select.select_by_value('01').click()
    # numbers_month = Select(driver.find_element_by_name("b-month"))
    # numbers_month.select_by_visible_text("Январь").click()
    # ActionChains(driver).move_to_element(numbers_month).click(numbers_month).perform()
    time.sleep(3)
    # d_month = driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/section/section/div[1]/form/div[1]/div[1]/div[3]/div/label[2]/div/a/span/font/font')
    # ActionChains(driver).move_to_element(d_month).click(d_month).perform()
    # time.sleep(3)
    # number_d_month = driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/section/section/div[1]/form/div[1]/div[1]/div[3]/div/label[2]/select/option[2]')
    # ActionChains(driver).move_to_element(number_d_month).click(number_d_month).perform()
    # time.sleep(3)
    # number_day = driver.find_element_by_xpath('//a[@span="01")]')
    # ActionChains(driver).move_to_element(number_day).click(number_day).perform()
    # time.sleep(4)
    b_year = driver.find_element_by_name('b-year')
    ActionChains(driver).move_to_element(b_year).click(b_year).perform()
    ActionChains(driver).move_to_element(name).send_keys("1960").perform()
    time.sleep(4)
    d_year = driver.find_element_by_name('d-year')
    ActionChains(driver).move_to_element(d_year).click(d_year).perform()
    ActionChains(driver).move_to_element(name).send_keys("2020").perform()
    search = driver.find_element_by_class_name('button__text')
    ActionChains(driver).move_to_element(search).click(search).perform()
    time.sleep(4)
    # name.send_keys("Иванов Иван Иванович")
    # time.sleep(2)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

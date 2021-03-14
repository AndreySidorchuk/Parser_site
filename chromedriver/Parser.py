from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import csv

CSV = 'cases.csv'
url = "https://notariat.ru/ru-ru/"
driver = webdriver.Chrome(executable_path="C:\\Users\\Андрей\\PycharmProjects\\Parser_site\\chromedriver\\chromedriver.exe")

class NalogParser(object):

    def parse_probate_cases_page(self, fio: str, b_date: list, d_date: list):
        """Вводит входные данные
            Arg:
                fio:
                b_date:
                d_date:

            Return:
        """
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

            #Нахождение баннера с Реестром наследственных дел
            elem = driver.find_element_by_xpath('/html/body/div/main/div[3]/div[2]')
            ActionChains(driver).move_to_element(elem).click(elem).perform()
            time.sleep(2)
            window_after = driver.window_handles[2]
            driver.switch_to.window(window_after)
            time.sleep(2)
            # Ввод ФИО человека
            name = driver.find_element_by_name('name')
            ActionChains(driver).move_to_element(name).send_keys(fio).perform()
            time.sleep(4)
            day = driver.find_element_by_xpath("//a[span='День']")
            ActionChains(driver).move_to_element(day).click(day).perform()
            time.sleep(3)
            # Клик по вкладке месяц рождения
            month = driver.find_element_by_xpath('//a[span="Месяц"]')
            # ActionChains(driver).move_to_element(month).click(month).perform()
            time.sleep(3)
            # select = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.select[name="b-month"]'))))
            # numbers_month = select.select_by_value("02")
            # select = Select(EC.element_to_be_clickable((By.NAME, "")))
            # numbers_month = driver.find_element_by_xpath("//input[@name='b-month']")
            # numbers_month.send_keys("Февраль")
            # driver.find_element_by_xpath('//select[@name="b-month"]/option[@value="01"]').click()
            # months = Select(driver.find_element(By.NAME("b-month")))
            # number_month = months.select_by_visible_text("Январь")
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

            # Ввод года рождения человека
            b_year = driver.find_element_by_name('b-year')
            ActionChains(driver).move_to_element(b_year).click(b_year).perform()
            # ActionChains(driver).move_to_element(name).send_keys(b_date[2]).perform()
            # time.sleep(4)
            # Ввод года смерти человека
            d_year = driver.find_element_by_name('d-year')
            ActionChains(driver).move_to_element(d_year).click(d_year).perform()
            ActionChains(driver).move_to_element(name).send_keys(d_date[2]).perform()
            # Нажатие кнопки поиск дел
            search = driver.find_element_by_class_name('button__text')
            ActionChains(driver).move_to_element(search).click(search).perform()
            time.sleep(4)
            HTMLPage = driver.page_source
            items = self.get_content(HTMLPage)
            self.save_info(items, CSV)
        except Exception as ex:
            print(ex)
            print('NO')
        finally:
            driver.close()
            driver.quit()


    def get_content(self, HTMLPage):
        soup = BeautifulSoup(HTMLPage, features='html.parser')

        all_cases = []
        pages = int(soup.find('h5', class_='probate-cases__result-header').find('b').get_text()) // 12 + 1
        for page in range(1, pages + 1):
            page = str(page)
            probate_cases = soup.find_all('ol', class_='probate-cases__result-list')
            if page != '1':
                number_page = driver.find_element_by_css_selector(f'li[data-page="{page}"]')
                ActionChains(driver).move_to_element(number_page).click(number_page).perform()
                time.sleep(4)
            for cases in probate_cases:
                for case in cases:
                    all_cases.append(
                        {
                            'title': case.find('h4').get_text(),
                            'date_death': case.find_all('p')[0].get_text(),
                            #'number_case': case.find_all('p')[1][0].get_text(),
                            'name_notary': case.find('a').get_text(),
                            'link_product': case.find('a').get('href')
                        }
                    )
        return all_cases

    def save_info(self, items, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['ФИО человека', 'Дата смерти', 'Номер дела', 'Нотариус', 'Ссылка на нотариус'])
            for item in items:
                writer.writerow([item['title'], item['date_death'], item['name_notary'], item['link_product']])


if __name__ == '__main__':
    fio = 'Иванов Сергей Александрович'
    b_date = ['01', '03', '1960']
    d_date = ['01', '03', '2015']
    Parser =NalogParser()
    Parser.parse_probate_cases_page(fio, b_date, d_date)
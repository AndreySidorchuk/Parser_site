from bs4 import BeautifulSoup
import requests
import re
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
url = "https://notariat.ru/ru-ru/help/probate-cases/"
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
            months = driver.find_elements_by_xpath('//span[contains(text(), "Месяц")]')
            days = driver.find_elements_by_xpath('//span[contains(text(), "День")]')
            # Ввод ФИО человека
            name = driver.find_element_by_name('name')
            ActionChains(driver).move_to_element(name).send_keys(fio).perform()
            time.sleep(2)

            # Выбор дня рождения
            b_day = days[0]
            driver.execute_script("arguments[0].scrollIntoView();", b_day)
            time.sleep(2)
            ActionChains(driver).move_to_element(b_day).click(b_day).perform()
            time.sleep(2)
            for day in range(1, int(b_date[0]) + 1):
                if day != 1:
                    ActionChains(driver).move_to_element(b_day).send_keys(Keys.ARROW_DOWN).perform()
                    time.sleep(1)
            ActionChains(driver).move_to_element(b_day).send_keys(Keys.RETURN).perform()
            time.sleep(3)

            #Выбор месяца рождения
            b_month = months[0]
            ActionChains(driver).move_to_element(b_month).click(b_month).perform()
            time.sleep(3)
            for month in range(1, int(b_date[1]) + 1):
                if month != 1:
                    ActionChains(driver).move_to_element(b_month).send_keys(Keys.ARROW_DOWN).perform()
                    time.sleep(1)
            ActionChains(driver).move_to_element(b_month).send_keys(Keys.RETURN).perform()
            time.sleep(3)

            # Ввод года рождения человека
            b_year = driver.find_element_by_name('b-year')
            ActionChains(driver).move_to_element(b_year).click(b_year).perform()
            ActionChains(driver).move_to_element(name).send_keys(b_date[2]).perform()
            time.sleep(3)

            # Выбор дня смерти
            d_day = days[1]
            driver.execute_script("arguments[0].scrollIntoView();", d_day)
            time.sleep(2)
            ActionChains(driver).move_to_element(d_day).click(d_day).perform()
            time.sleep(2)
            for day in range(1, int(d_date[0]) + 1):
                if day != 1:
                    ActionChains(driver).move_to_element(d_day).send_keys(Keys.ARROW_DOWN).perform()
                    time.sleep(1)
            ActionChains(driver).move_to_element(d_day).send_keys(Keys.RETURN).perform()
            time.sleep(3)

            # Выбор месяца смерти
            d_months = months[1]
            ActionChains(driver).move_to_element(d_months).click(d_months).perform()
            time.sleep(3)
            for month in range(1, int(d_date[1]) + 1):
                if month != 1:
                    ActionChains(driver).move_to_element(d_months).send_keys(Keys.ARROW_DOWN).perform()
                    time.sleep(1)
            ActionChains(driver).move_to_element(d_months).send_keys(Keys.RETURN).perform()
            time.sleep(3)

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
            if page != '1':
                number_page = driver.find_element_by_css_selector(f'li[data-page="{page}"]')
                ActionChains(driver).move_to_element(number_page).click(number_page).perform()
                time.sleep(4)
                html_page = driver.page_source
                soup = BeautifulSoup(html_page, features='html.parser')
            probate_cases = soup.find_all('ol', class_='probate-cases__result-list')
            for cases in probate_cases:
                for case in cases:
                    all_cases.append(
                        {
                            'title': case.find('h4').get_text().capitalize(),
                            'date_death': case.find_all('p')[0].get_text(),
                            'number_case': re.findall(r'(\d*\/\d\d*)', case.find_all('p')[1].get_text())[0],
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
                writer.writerow(
                    [item['title'], item['date_death'], item['number_case'], item['name_notary'], item['link_product']])


if __name__ == '__main__':
    fio = 'Иванов Сергей Александрович'
    b_date = ['08', '03', '1945']
    d_date = ['01', '07', '2014']
    Parser = NalogParser()
    Parser.parse_probate_cases_page(fio, b_date, d_date)
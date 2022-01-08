from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver.locators import NalogLocators
from loguru import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv


TEST_FOLDER = "C:\\Users\\79277\\PycharmProjects\\Parser_site\\chromedriver\\"
CSV = TEST_FOLDER + 'cases.csv'
URL = "https://notariat.ru/ru-ru/help/probate-cases/"
driver = webdriver.Chrome(executable_path="C:\\Users\\79277\\PycharmProjects\\chromedriver.exe")


logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")
logger.info("Info")
logger.error("Error")
logger.debug("Debug")


@logger.catch
def parse_probate_cases_page(fio: str, b_date: list, d_date: list):
    """Вводит входные данные для поиска дела

    Arg:
        fio: ФИО человека
        b_date: дата рождения
        d_date: дата смерти

    Return: информация о найденных делах
    """
    try:
        driver.get(URL)
        WebDriverWait(driver, 1)
        months = driver.find_elements(*NalogLocators.months)
        days = driver.find_elements(*NalogLocators.days)
        name = driver.find_element(*NalogLocators.name)
        ActionChains(driver).move_to_element(name).send_keys(fio).perform()
        b_day = days[0]
        input_b_or_d_day(b_day, b_date)
        b_month = months[0]
        input_b_or_d_month(b_month, b_date)
        b_year = driver.find_element(*NalogLocators.brth_day)
        input_b_or_d_year(b_year, b_date, name)
        d_day = days[1]
        input_b_or_d_day(d_day, d_date)
        d_month = months[1]
        input_b_or_d_month(d_month, d_date)
        d_year = driver.find_element(*NalogLocators.death_day)
        input_b_or_d_year(d_year, d_date, name)
        search_case()
        HTMLPage = driver.page_source
        items = get_content(HTMLPage)
        save_info(items, CSV)
    finally:
        driver.close()
        driver.quit()


def input_b_or_d_day(l_day, date):
    """Выбирает день рождения либо день смерти

    Args:
        l_day: день месяца
        date: дата смерти либо рождения
    """
    driver.execute_script("arguments[0].scrollIntoView();", l_day)
    ActionChains(driver).move_to_element(l_day).click(l_day).perform()
    for day in range(1, int(date[0]) + 1):
        if day != 1:
            ActionChains(driver).move_to_element(l_day).send_keys(Keys.ARROW_DOWN).perform()
    ActionChains(driver).move_to_element(l_day).send_keys(Keys.RETURN).perform()


def input_b_or_d_year(l_year, date, name):
    """Выбирает год рождения либо год смерти

    Args:
        l_year: год месяца
        date: дата смерти либо рождения
        name: имя человека
        """
    ActionChains(driver).move_to_element(l_year).click(l_year).perform()
    ActionChains(driver).move_to_element(name).send_keys(date[2]).perform()


def input_b_or_d_month(l_month, date):
    """Выбирает месяц рождения либо месяц смерти

    Args:
        l_month: месяц смерти либо рождения
        date: дата смерти либо рождения
    """
    ActionChains(driver).move_to_element(l_month).click(l_month).perform()
    WebDriverWait(driver, 1)
    for month in range(1, int(date[1]) + 1):
        if month != 1:
            ActionChains(driver).move_to_element(l_month).send_keys(Keys.ARROW_DOWN).perform()
    ActionChains(driver).move_to_element(l_month).send_keys(Keys.RETURN).perform()


def search_case():
    """Нажатие кнопки 'Искать дело'"""
    search = driver.find_element(*NalogLocators.search_button)
    ActionChains(driver).move_to_element(search).click(search).perform()
    time.sleep(2)

@logger.catch
def get_content(HTMLPage):
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
                        'title': case.find('h4').get_text(),
                        'date_death': case.find_all('p')[0].get_text(),
                        'number_case': re.findall(r'(\d*\/\d\d*)', case.find_all('p')[1].get_text())[0],
                        'name_notary': case.find('a').get_text(),
                        'link_product': case.find('a').get('href')
                    }
                )
    return all_cases


@logger.catch
def save_info(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['ФИО человека', 'Дата смерти', 'Номер дела', 'Нотариус', 'Ссылка на нотариус'])
        for item in items:
            writer.writerow(
                [item['title'], item['date_death'], item['number_case'], item['name_notary'], item['link_product']])


if __name__ == '__main__':
    fio = 'Иванов Сергей Александрович'
    b_date = ['02', '02', '1946']
    d_date = ['22', '09', '2011']
    parse_probate_cases_page(fio, b_date, d_date)

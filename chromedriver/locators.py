from selenium.webdriver.common.by import By


class NalogLocators(object):


    months = (By.XPATH, '//span[contains(text(), "Месяц")]')
    days = (By.XPATH, '//span[contains(text(), "День")]')
    name = (By.NAME, 'name')
    search_button = (By.CLASS_NAME, 'button__text')
    brth_day = (By.NAME, 'b-year')
    death_day = (By.NAME, 'd-year')


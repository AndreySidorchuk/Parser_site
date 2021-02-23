from selenium import webdriver
import time


url = "https://proghub.ru/tests/"
driver = webdriver.Chrome(executable_path="C:\\Users\\Андрей\\PycharmProjects\\Parser_site\\chromedriver\\chromedriver.exe")




try:
    driver.get(url=url)
    time.sleep(5)
    slide_elems = driver.find_elements_by_class_name("testCard")
    for elem in slide_elems:
        print(elem.get_attribute("href"))
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


# def main():
#     driver = webdriver.Chrome()
#     parser = ProgHubParser(driver,"python")
#     parser.parse()
#
#
# if __name__ == "__main__":
#     main()

    # url = "https://proghub.ru/tests/"
    # driver = webdriver.Chrome(
    #     executable_path="C:\\Users\\Андрей\\PycharmProjects\\Parser_site\\chromedriver\\chromedriver.exe")
    #
    # try:
    #     driver.get(url=url)
    #     time.sleep(5)
    #     driver.refresh()
    #     title4 = driver.find_element_by_tag_name("h1")
    #     print(title4.text)
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     driver.close()
    #     driver.quit()
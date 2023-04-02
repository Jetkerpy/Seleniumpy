import requests
import time
import re
from bs4 import BeautifulSoup

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select



class ValyutaConverter:
    """
    ValyutaConverter automate with seleniumpy
    """
    URL = "https://uz.moneyratestoday.com/valyuta-hisoblagichi.html"
    ALL = []
    PATTERN = r"\((\w+)\)"

    def __init__(self, money: int, from_currency = "USD", to_currency = "UZS") -> None:
        self.set_currencies_to_all()
        self.__check_money(money)
        self.__check_currency(from_currency)
        self.__check_currency(to_currency)
        self.money = money
        self.from_currency = from_currency.upper()
        self.to_currency = to_currency.upper()

    
    @classmethod
    def __check_money(cls, money):
        """
        Check money
        """
        if money == '':
            raise ValueError("You didn't put money!")
        
        if not isinstance(money, int):
            raise TypeError("Money must be number!")


    @classmethod
    def __check_currency(self, currency):
        """
        Check currency from and to
        """
        if not isinstance(currency, str) or currency == '':
            raise TypeError("You must put currency using str and not empty.")
        if currency.upper() not in self.ALL:
            raise ValueError("Your currency doesn't exists!")


    
    def close_button(self, driver):
        """
        This you know :) when you are going to the page suddenly
        show up blah blah :) :) so we'll kick his ass
        """
        close_button = driver.find_element(By.XPATH, "//input[@value='❌ Close']")
        close_button.click()



    def change_tag_to_valyuta_convertor(self, driver):
        """
        Change tag to valyuta convertor
        """
        tag_valyuta_konvertori = driver.find_element(By.XPATH, "//a[@title='Valyuta konvertori']")
        tag_valyuta_konvertori.click()



    def change_from_uz_to_usd(self, driver):
        """
        This method allow us to change example USD => UZS, UZS => USD
        """
        change = driver.find_element(By.CLASS_NAME, "reverse")
        change.click()

    

    def clear_money(self, driver):
        """
        This method remove 1 from form of this page and return object
        """
        money = driver.find_element(By.ID, "text_quantity")
        money.clear()
        return money

    

    def send_money(self, driver, value):
        """
        This method send money and clicked button
        """
        money = self.clear_money(driver)
        money.send_keys(value)
        button = driver.find_element(By.ID, "whc_btn2")
        button.click()

    

    def change_currencies(self, driver):
        """
        Change currencies is put our currency into form by selecting 
        """
        if self.from_currency == "USD" and self.to_currency == "UZS":
            self.change_from_uz_to_usd(driver)

        else:
            self.select_from_currency(driver)
            time.sleep(4)
            self.select_to_currency(driver)

    

    def select_from_currency(self, driver):
        """
        Select from currency this method helps us to select
        """
        # click_dropdown = driver.find_element(By.ID, "select_from_currency")
        # click_dropdown.click()
        # put_currency = driver.find_element(By.XPATH, f"//option[@value='{self.from_currency}']")
        # put_currency.click()
        select_element = driver.find_element(By.ID, "select_from_currency")
        select = Select(select_element)
        select.select_by_value(self.from_currency)
        select_element.click()



    def select_to_currency(self, driver):
        """
        This method select to currency
        """
        # click_dropdown = driver.find_element(By.ID, "select_to_currency")
        # click_dropdown.click()
        # put_currency = driver.find_element(By.XPATH, f"//option[@value='{self.to_currency}']")
        # put_currency.click()

        select_element = driver.find_element(By.ID, "select_to_currency")
        select = Select(select_element)
        select.select_by_value(self.to_currency)
        select_element.click()



    def convert_money(self):
        """
        return converted money by your currencies
        """
        PATH = Service("C:\Chromedriver\chromedriver.exe")
        driver = Chrome(service=PATH)
        driver.get(self.URL)
        self.close_button(driver)
        self.change_tag_to_valyuta_convertor(driver)

        self.change_currencies(driver)
        
        self.send_money(driver, str(self.money))
        result = driver.find_element(By.TAG_NAME, "b")
        time.sleep(5)

        text = result.text
        driver.close()
        return text
       


    def set_currencies_to_all(self):
        """
        This method allow us to set currency to ALL = []
        by using web scraping ok :) 
        """
        html_string = requests.get(self.URL).text
        html = BeautifulSoup(html_string, 'html.parser')
        get_tag_select_by_id = html.find("select", {"id": "select_from_currency"})
        children = get_tag_select_by_id
        for child in children:
            child_text = child.text.strip()
            if child_text != '':
                value = self.filter(child_text)
                self.ALL.append(value)

    

    def filter(self, value):
        """
        return "Zambiya Kwacha's (ZMK)" => ZMK 
        """
        text = re.search(self.PATTERN, value)
        if text:
            val = text.group(1)
            return val
        return None

# vc = ValyutaConverter(100, 'cad', 'usd')
# print(vc.convert_money())
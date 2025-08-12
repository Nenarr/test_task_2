import time
from typing import List
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from locators import WildberriesLocators

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")   
    service = Service(executable_path="/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    return driver

class WildberriesPage:

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10, poll_frequency=1.5)

    def open_page(self, url: str) -> None:
        self.driver.delete_all_cookies()
        self.driver.get(url)
        self._wait_for_page_load()

    def search_for_product(self, product_name: str) -> None:
        self._wait_and_click(WildberriesLocators.SEARCH_INPUT)
        self._wait_and_send_keys(WildberriesLocators.SEARCH_INPUT, product_name)
        self._wait_for_page_load()

    def apply_filter(self, filter_index: int = 2) -> None:
        self._wait_and_click(WildberriesLocators.DROPDOWN_FILTER)
        self.wait.until(
            EC.presence_of_all_elements_located(WildberriesLocators.FILTER_ITEMS))
        filters = self.driver.find_elements(*WildberriesLocators.FILTER_ITEMS)
        if filter_index < len(filters):
            filters[filter_index].click()
        self._wait_for_page_load()

    def get_products_info(self, count: int = 10) -> List[str]:
        self.wait.until(
            EC.presence_of_element_located(WildberriesLocators.PRODUCT_CARD_LIST))

        products_list = self.driver.find_element(*WildberriesLocators.PRODUCT_CARD_LIST)
        products = products_list.find_elements(*WildberriesLocators.PRODUCT_CARD)

        name_price_list = []
        for i in range(min(count, len(products))):
            product_text = products[i].find_element(
                *WildberriesLocators.PRODUCT_CARD_MIDDLE).text
            product_text = product_text.replace("\n", "|").replace("|с WB Кошельком", "")
            name_price_list.append(product_text)

        return name_price_list

    def _wait_for_page_load(self) -> None:
        time.sleep(2)
#        self.wait.until(
#            EC.presence_of_element_located(WildberriesLocators.PAGE_LOAD_INDICATOR))

    def _wait_and_click(self, locator: tuple) -> None:
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(locator)).click()


    def _wait_and_send_keys(self, locator: tuple, text: str) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text, Keys.ENTER)


class WildberriesScraper:

    def __init__(self):
        self.driver = create_driver()
        self.driver.implicitly_wait(20)
        self.page = WildberriesPage(self.driver)

    def scrape_products(self, url: str, product_name: str) -> List[str]:
        try:
            self.page.open_page(url)
            self.page.search_for_product(product_name)
            self.page.apply_filter()
            return self.page.get_products_info()
        finally:
            self.driver.quit()


if __name__ == "__main__":
    scraper = WildberriesScraper()
    products = scraper.scrape_products(
        url="https://www.wildberries.ru/",
        product_name="транспортир"
    )
    print(f"Цена| Полная цена | Название")
    for product in products:
        print(f"{product}")
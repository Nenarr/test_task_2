from selenium.webdriver.common.by import By

class WildberriesLocators:

    SEARCH_INPUT = (By.ID, "searchInput")
    DROPDOWN_FILTER = (By.CLASS_NAME, "dropdown-filter")
    FILTER_ITEMS = (By.XPATH, '//div[@class="filter"]//ul//li')
    PRODUCT_CARD_LIST = (By.CLASS_NAME, "product-card-list")
    PRODUCT_CARD = (By.TAG_NAME, "article")
    PRODUCT_CARD_MIDDLE = (By.CLASS_NAME, "product-card__middle-wrap")
    PAGE_LOAD_INDICATOR = (By.CLASS_NAME, "product-card__wrapper")
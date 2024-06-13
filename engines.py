import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class MaxResultsReachedException(Exception):
    pass

class DuckDuckGoScraper:
    def __init__(self, browser="Firefox", timeout=10):
        self.timeout = timeout
        self.logger = self._setup_logger()
        self.driver = self._initialize_driver(browser)
      
    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
  
    def _initialize_driver(self, browser):
        try:
            if browser.lower() == "chrome":
                return webdriver.Chrome()
            elif browser.lower() == "firefox":
                return webdriver.Firefox()
            else:
                raise ValueError("Unsupported browser. Please specify 'chrome' or 'firefox'.")
        except WebDriverException as e:
            self.logger.error(f"Error initializing WebDriver: {e}")
            exit()

    def perform_search(self, query, pages):
            self._search(query)
            for _ in range(pages-1):
                self._scroll()
                try:
                    self._load_more_results()
                except MaxResultsReachedException:
                    self.logger.error("Max results reached.")
                    break
    
    def _search(self, query):
        try:
            url = f"https://duckduckgo.com/?q={query}"
            self.driver.get(url)
        except WebDriverException as e:
            self.logger.error(f"Error navigating to search page: {e}")
            exit()

    def _scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _load_more_results(self):
        try:
            button = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, "//button[@id='more-results']")))
            button.click()
        except TimeoutException:
            self.logger.warning("Timed out waiting for 'Load More Results' button. Most probably end of results reached or you set the timeout too low")
            raise MaxResultsReachedException()
    
    def _wait_until_more_results_loaded(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, "//button[not(@disabled='')]")))
        except TimeoutException:
            self.logger.warning("Timed out waiting for more results to load. This usually happens when 'more results' button wasn't clicked or you set the timeout too low")
    
    def extract_links(self):
        try:
            self._scroll()
            link_elements = self.driver.find_elements(By.XPATH, "//a[@data-testid='result-extras-url-link']")
            extracted_links = [link_element.get_attribute("href") for link_element in link_elements]
            return extracted_links
        except WebDriverException as e:
            self.logger.error(f"Error extracting links: {e}")
            exit()

    def close(self):
        try:
            self.driver.quit()
        except WebDriverException as e:
            self.logger.error(f"Error closing WebDriver: {e}")

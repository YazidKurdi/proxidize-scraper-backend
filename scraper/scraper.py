import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from scraper.models import ScrapeResult
from scraper.serializers import ScrapeResultSerializer

class EcommerceScraper:
    def __init__(self):
        """
        Initializes an instance of the EcommerceScraper class with a Chrome WebDriver.
        The WebDriver is used to interact with a web browser and scrape data from a website.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("no-sandbox")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def scrape_website(self, request,keyword,rows):
        try:
            elements = self.get_elements_to_scrape(keyword,rows)

            scraped_data = []
            new_added_count = 0
            duplicate_count = 0

            for element in elements:
                product_title, img_element, info_texts, price_full = self.extract_product_info(element)
                data = {
                    "product_title": product_title,
                    "image": img_element,
                    "info": ", ".join(info_texts),
                    "price": price_full
                }

                if self.save_scrape_result(data,request):
                    new_added_count += 1
                else:
                    duplicate_count += 1
                scraped_data.append(data)

            total_scraped_count = len(scraped_data)

            response_data = {
                "scraped_data": scraped_data,
                "count_summary": {
                    "total_scraped_count": total_scraped_count,
                    "new_added_count": new_added_count,
                    "duplicate_count": duplicate_count
                }
            }

            return response_data

        # except Exception as e:
        #     return {"error": str(e)}

        finally:
            self.driver.quit()

    def get_elements_to_scrape(self, keyword, min_rows_to_scrape):
        """
        Scrapes and returns a list of elements containing product information based on a search keyword.
        """

        url = f'https://www.jarir.com/sa-en/catalogsearch/result?search={keyword}'
        self.driver.get(url)
        print(self.driver.page_source)
        wait = WebDriverWait(self.driver, 10)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'button__contrylangSelector')))
        #
        # self.driver.find_element(By.CLASS_NAME, 'button__contrylangSelector').click()
        # time.sleep(5)
        # self.driver.find_element(By.CLASS_NAME, 'p16').click()


        vue_carousel_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'VueCarousel')))
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            elements = self.driver.find_elements(By.CLASS_NAME, 'product-tile__item--spacer')[12:]
            if len(elements) >= min_rows_to_scrape:
                break

            # Scroll down to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get the desired number of elements to scrape
        return elements[:min(min_rows_to_scrape, len(elements))]

    def extract_product_info(self, element):
        """
        Extracts product information from a given element.
        """
        title_element = element.find_element(By.CLASS_NAME, 'product-title__title').get_attribute("textContent").strip()
        img_elements = element.find_elements(By.CSS_SELECTOR, '.image.image--contain')
        img_element = img_elements[2].get_attribute("src")

        try:
            tag_element = element.find_element(By.CLASS_NAME, 'product-title__info')
            info_texts = [info_span.text.strip() for info_span in tag_element.find_elements(By.TAG_NAME, 'span')]
        except NoSuchElementException:
            info_texts = []

        price_element = element.find_element(By.CSS_SELECTOR, '.price_alignment')
        price_currency = price_element.find_element(By.CLASS_NAME, 'price__currency').get_attribute(
            "textContent").strip()
        price_amount = price_element.find_element(By.XPATH, './span[2]').get_attribute("textContent").strip()
        price_full = f"{price_currency} {price_amount}"

        return title_element, img_element, info_texts, price_full

    def save_scrape_result(self, data,request):
        """
        Saves the scraped product data to the database if does not already exist.
        """
        product_title = data["product_title"]
        img_element = data["image"]
        info_texts = data["info"]
        price_full = data["price"]
        custom_id = f"{product_title}_{price_full}_{img_element}_{request.user.id}"

        instance_data = {
            **data,
            "custom_id": custom_id,
            "user": request.user.id,
        }

        serializer = ScrapeResultSerializer(data=instance_data)
        if serializer.is_valid():
            if not ScrapeResult.objects.filter(custom_id=custom_id).exists():
                serializer.save(custom_id=custom_id)
                return True
        return False
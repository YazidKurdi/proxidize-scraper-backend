from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Install Webdriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def extract_product_info(element):
    title_element = element.find_element(By.CLASS_NAME, 'product-title__title')
    img_element = element.find_elements(By.CSS_SELECTOR, '.image.image--contain')[2].get_attribute("src")
    tag_element = element.find_element(By.CLASS_NAME, 'product-title__info')

    info_texts = [info_span.text.strip() for info_span in tag_element.find_elements(By.TAG_NAME, 'span')]

    price_element = element.find_element(By.CSS_SELECTOR, '.price_alignment')
    price_currency = price_element.find_element(By.CLASS_NAME, 'price__currency').get_attribute("textContent").strip()
    price_amount = price_element.find_element(By.XPATH, './span[2]').get_attribute("textContent").strip()
    price_full = f"{price_currency} {price_amount}"

    product_title = title_element.text
    return product_title, img_element, info_texts, price_full


def scrape_website(keyword):

    try:
        url = f'https://www.jarir.com/sa-en/catalogsearch/result?search={keyword}'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        vue_carousel_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'VueCarousel')))
        elements = driver.find_elements(By.CLASS_NAME, 'product-tile__item--spacer')[12:]

        scraped_data = []
        for idx, element in enumerate(elements, start=1):
            product_title, img_element, info_texts, price_full = extract_product_info(element)
            scraped_data.append({
                "product_title": product_title,
                "image": img_element,
                "info": info_texts,
                "price": price_full
            })

        return scraped_data

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

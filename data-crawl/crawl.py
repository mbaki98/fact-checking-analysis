from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)

# options = Options()
# options.add_argument("start-maximized")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver = webdriver.Chrome(service=Service(r"C:\Program Files (x86)\chromedriver.exe"))

driver.get("https://www.snopes.com/fact-check/")
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "article"))
    )
    articles = driver.find_element(By.CLASS_NAME, "list-archive").find_elements(By.TAG_NAME, "article")
    i = 1
    for article in articles:
        title = article.find_element(By.CLASS_NAME, "title")
        subtitle = article.find_element(By.CLASS_NAME, "d-flex")
        label = article.find_element(By.CLASS_NAME, "media").find_element(By.TAG_NAME, "span")
        print("Article {}: \n\t Title: {}\n\t Sub: {}\n\t Label: {}\n".format(i, title.text, subtitle.text, label.text))
        i = i + 1

finally:
    driver.quit()

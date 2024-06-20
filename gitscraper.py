import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
import time

# Initialize the driver
#cdp = "/usr/bin/geckodriver"
#service = Service(executable_path=cdp)
#driver = webdriver.Firefox(service=service)

proxies = [
   # Add more proxies as needed
]

# Function to get a random proxy
def get_random_proxy():
    return random.choice(proxies)

# Function to create a new WebDriver instance with a proxy
def create_driver_with_proxy():
    proxy = get_random_proxy()
    firefox_options = Options()
    firefox_options.add_argument('--proxy-server=%s' % proxy)
    cdp = "/usr/bin/geckodriver"
    service = Service(executable_path=cdp)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def switch_proxy():
    global driver
    driver.quit()  # Close the current driver
    driver = create_driver_with_proxy()

# Initialize the driver with a proxy
driver = create_driver_with_proxy()

link = input("Enter the GitHub link you want to scrape: ")
global prompt 
prompt = input("Enter the keyword you want to search for:")
driver.get(f'{link}/?tab=repositories')

res = driver.find_elements(By.XPATH, "//a[@itemprop='name codeRepository']")

repo_list = []
repo_links = []

def going_for_raw(file_link):
    switch_proxy()
    #time.sleep(20)
    try:
        driver.get(file_link)
        raw = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-testid='raw-button']"))
        )
        time.sleep(10)
        raw.click()
        time.sleep(2)  # Wait for the raw content to load
        html = driver.page_source
        if prompt in html: 
            print(f"found keyword: {prompt}")
            print(file_link)
    except TimeoutException:
        print(f'Error in going for raw: Timeout while waiting for raw button on {file_link}')
    except StaleElementReferenceException:
        print(f'Error in going for raw: Stale element on {file_link}')
    except NoSuchElementException:
        print(f'Error in going for raw: No such element on {file_link}')
    except Exception as e:
        print(f'Error in going for raw: {e}')

def get_elements_retry(driver, by, value, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            return driver.find_elements(by, value)
        except StaleElementReferenceException:
            attempt += 1
            time.sleep(2)
    return []

def cycle3(folder_link, folder_name, repo_link):
    driver.get(folder_link)
    time.sleep(2)
    
    res = get_elements_retry(driver, By.CLASS_NAME, "react-directory-truncate")
    file_in_folder_list = [k.text for k in res if k.text != '']

    for k in file_in_folder_list:

        driver.get(folder_link)
        branch_element = driver.find_element(By.XPATH, "//span[@class='Text-sc-17v1xeu-0 bOMzPg']")
        branch = branch_element.text[1:]  # Remove the first character

        if "." in k and not k.startswith('.') and "png" not in k and "jpg" not in k and "jpeg" not in k and "gif" not in k and "pdf" not in k and "out" not in k:
            add = f'{repo_link}/blob/{branch}/{folder_name}/{k}'
            going_for_raw(add)
        elif "." not in k or k.startswith('.'):
            add = f'{folder_link}/{k}'
            cycle3(add, f'{folder_name}/{k}', repo_link)

def cycle(repo_link):
    switch_proxy()
    driver.get(repo_link)
    
    res = get_elements_retry(driver, By.CLASS_NAME, "react-directory-truncate")
    file_list = []
    for i in res:
        file = i.text
        if "png" not in file and "jpg" not in file and "jpeg" not in file and "gif" not in file and "pdf" not in file and file != 'a.out' and file != '':
            file_list.append(file)

    for i in file_list:
        try:
            driver.get(repo_link)
            branch_element = driver.find_element(By.XPATH, "//span[@class='Text-sc-17v1xeu-0 bOMzPg']")
            #print(branch_element)
            branch = branch_element.text[1:]  # Remove the first character

            if "." in i and not i.startswith('.') and "png" not in i and "jpg" not in i and "jpeg" not in i and "gif" not in i and "pdf" not in i and i != 'a.out':
                add = f'{repo_link}/blob/{branch}/{i}'
                going_for_raw(add)
            elif "." not in i or i.startswith('.'):
                add = f'{repo_link}/tree/{branch}/{i}'
                cycle3(add, i, repo_link)
        except StaleElementReferenceException:
            print(f'Encountered stale element reference, retrying for element: {i.text}')
            cycle(repo_link)  # Retry the function call if element is stale
        except Exception as e:
            print(add)
            print(f'Error processing file/folder {i}: {e}')

for i in res:
    repo_list.append(i.text)

for repo_name in repo_list:
    add = f'{link}/{repo_name}'
    repo_links.append(add)
    cycle(add)

driver.quit()

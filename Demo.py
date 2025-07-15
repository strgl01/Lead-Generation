from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import random
import time
proxies = [
    "45.127.248.127:5128",
     "173.0.9.209:5792",
     "166.88.58.10:5735"
    # Add more proxies as needed {username = "tlwiyzum" password = "qkulf63de7nh"}38.154.227.167:5868:tlwiyzum:qkulf63de7nh
]
custom_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br, zstd',
    
}
proxy=random.choice(proxies)
# Set up Selenium Wire options
seleniumwire_options = {
    # 'request_storage_base_dir': 'requests',  # Optional: to store requests
    'custom_headers': custom_headers,
    'proxy': {
                'http': f'http://tlwiyzum:qkulf63de7nh@{proxy}',
                'https': f'http://tlwiyzum:qkulf63de7nh@{proxy}',
                'no_proxy': 'localhost,127.0.0.1'  # Exclude localhost
                }
}

def scroll_within_element(element):
    total_height = 0
    distance = 1500
    scroll_pause_time = 50
    count=0

    while True:
        count=count+1
        print(count)
        # Scroll down by the distance
        driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", element, distance)
        time.sleep(scroll_pause_time)  # Wait to load new content
        
        # Calculate the new scroll height and check if more content is loaded
        new_scroll_height = driver.execute_script("return arguments[0].scrollHeight;", element)
        print(new_scroll_height,total_height)
        if new_scroll_height == total_height:
            print('scrolling complete')
            break
        total_height = new_scroll_height


service = Service(geckodriver_path = r"C:/Users/dell/Desktop/geckodriver.exe")
options = Options()
#options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
driver = webdriver.Firefox(service=service, options=options, seleniumwire_options=seleniumwire_options)
driver.get('https://www.google.com/maps/search/roofing+business+USA')
time.sleep(30)
# Call the scroll function
scrollable_div=driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
scroll_within_element(scrollable_div)

# driver.execute_script()
time.sleep(500)
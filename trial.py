from selenium import webdriver

url = 'http://www.google.com'
driver = webdriver.Chrome()
driver.get(url)

search_bar = driver.find_element_by_xpath('//*[@id="lst-ib"]')
search_bar.send_keys('John Rust')
search_bar.submit()
driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()

# Print all
def print_ten():
    for i in range(1,11):
        xpath = '//*[@id="rso"]/div/div[' + str(i) + ']/div/div/h3/a'
        print(driver.find_element_by_xpath(xpath).text)

while True:
    try:
        print_ten()
        driver.find_element_by_xpath('//*[@id="pnnext"]/span[1]').click()
    except:
        break
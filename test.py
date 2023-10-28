import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")
driver.implicitly_wait(5)

driver.find_element(By.NAME, "q").send_keys("Restaurants in Bangalore", Keys.ENTER)
boxes = driver.find_elements(By.CLASS_NAME, "hfpxzc")
action = ActionChains(driver)
while len(boxes) > 0:
    time.sleep(3)
    driver.execute_script("arguments[0].scrollIntoView();", boxes[-1])
    time.sleep(3)
    box = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    for bo in box:
        if boxes.count(bo) > 0:
            continue
        else:
            boxes.append(bo)

    if len(boxes) == 100:
        break

names = []
address = []
contact = []

for b in boxes:
    driver.execute_script("arguments[0].scrollIntoView()", b)
    b.click()
    driver.implicitly_wait(3)
    name = driver.find_element(By.XPATH, "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1")
    data = name.text
    names.append(data)
    time.sleep(3)

    try:
        add = driver.find_element(By.XPATH, "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[11]/div[3]/button/div/div[2]/div[1]")
        data1 = add.text
    except NoSuchElementException:
        data1 = 'Null'

    address.append(data1)

    try:
        phone = driver.find_element(By.XPATH, "/html/body/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[11]/div[7]/button/div/div[2]/div[1]")
        data2 = phone.text
        if data2 == "Place an order":
            data2 = 'Null'
    except NoSuchElementException:
        data2 = 'Null'

    contact.append(data2)

my_dict = []
names.pop(0)
for (a, b, c) in zip(names, address, contact):
    my_dict.append({'name': a, 'add': b, 'phone': c})

json_object = json.dumps(my_dict, indent=3)

with open("data.json", "w") as file:
    file.write(json_object)

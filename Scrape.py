from os import terminal_size
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import requests
import json


driver = webdriver.Firefox(executable_path="drivers/geckodriver")
driver.get('https://www.google.com/search?q=bmw+of+austin')

# Change Language this can be optional
driver.find_element_by_xpath("/html/body/div[7]/div/div[7]/div/div/div/div[2]/div/a[2]").click()
# sleep(3)
# View Review
driver.find_element_by_xpath("/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[3]/div/div/div/div[6]/div/div/div[2]/div/div/div[2]/span/span/a").click()
sleep(3)
# Sort by New
driver.find_element_by_xpath("/html/body/span[2]/g-lightbox/div[2]/div[3]/span/div/div/div/div[2]/div[3]/g-scrolling-carousel/div[1]/div/div[2]").click()

driver.find_element_by_class_name('gws-localreviews__google-review')
exit = False
while exit==False:    #loop until your requirement is fulfilled
    response = BeautifulSoup(driver.page_source, 'html.parser')
    rlist = response.findAll('span',{"class":'dehysf'})
    print(rlist[-1].getText())
    if rlist[-1].getText() == "a month ago": # if you need of this year then RHS is "2 years ago"
        exit=True
    else:
        scrollable_div = driver.find_element_by_class_name('review-dialog-list')
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scrollable_div)

response = BeautifulSoup(driver.page_source, 'html.parser')
rlist = response.findAll('div',{"class":'gws-localreviews__google-review'})
    
# print(rlist)

for i in rlist:
    reviewer = i.find('div', class_='TSUbDb').find('a').getText()
    rate = i.find('span', class_='Fam1ne')['aria-label'].split(' ')[1]
    review = i.find('div', class_='Jtu6Td').getText()
    date = i.find('span', class_='dehysf').getText()
    a={
        "reviewer":reviewer,
        "rate":rate,
        "review":review,
        "date":date
    }
    # a= str(a)
    a=json.dumps(a)
    a=json.loads(a)

    print(a)
    # Post data to api of flask to save in db.
    url="http://127.0.0.1:5000/add_review"
    r = requests.post(url, json=a)
    print(r.status_code)
    
    # print(i)
    # print("==================================")

driver.quit()

"""
Copyright 2018 YoongiKim

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException


def collect_links(keyword):
    browser = webdriver.Chrome()

    browser.get("https://www.google.com/search?q={}&source=lnms&tbm=isch".format(keyword))

    time.sleep(1)

    print('Scrolling down')

    elem = browser.find_element_by_tag_name("body")

    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    try:
        btn_more = browser.find_element(By.XPATH, '//input[@value="결과 더보기"]')
        btn_more.click()

        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

    except ElementNotVisibleException:
        pass

    photo_grid_boxes = browser.find_elements(By.XPATH, '//div[@class="rg_bx rg_di rg_el ivg-i"]')

    print('Scraping links')

    links = []

    for box in photo_grid_boxes:
        imgs = box.find_elements(By.TAG_NAME, 'img')

        for img in imgs:
            src = img.get_attribute("src")
            if src[0] != 'd':
                links.append(src)

    print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('google', keyword, len(links)))
    browser.close()

    return links

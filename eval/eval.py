from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import time
import os
import random
import json
from tqdm.auto import tqdm


# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-animations")  # Disable animations


def _eval(choices, result_name):
    # Set page load strategy to "none"
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://www.16personalities.com/free-personality-test")

    # # wait for the page to load
    time.sleep(0.5)

    PAGES = 10

    for page_no in tqdm(range(PAGES)):
        # # click the next button with aria-label="Go to next set of questions"
        # # for all the class="radios" element, print their id and value in label tag
        
        radios = driver.find_elements(By.CLASS_NAME, "radios")
        for r_idx, radio in enumerate(radios):
            # find all input tags and store it as (id, value) pair
            inputs = radio.find_elements(By.TAG_NAME, "input")
            opt = []
            # for input in inputs:
            #     opt.append((input.get_attribute("id"), input.get_attribute("value")))
            # print(opt)
            labels = radio.find_elements(By.TAG_NAME, "label")

            # click on label with value="1"
            # VAL = -2
            # VAL = choices[page_no][r_idx]
            VAL = choices[page_no*6 + r_idx]
            label = labels[VAL + 3]
            driver.execute_script("arguments[0].click();", label)            


        time.sleep(0.1)
        if page_no != PAGES - 1:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next set of questions']")
            driver.execute_script("arguments[0].click();", next_button)
        else:
            # click on the button type="submit"
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)

    # wait for the page to load
    time.sleep(0.2)

    # get the result, save the html page


    RESULT_PAGES = 6
    SAVE_DIR = "results"
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    result = {}

    for page_no in range(RESULT_PAGES):
        time.sleep(0.2)

        # result = driver.page_source
        # with open(f"{SAVE_DIR}/result_{page_no}.html", "w") as f:
        #     f.write(result)

        if page_no == 0:
            # title is "results__type__name" is present in class attribute
            title = driver.find_element(By.CLASS_NAME, "results__type__name").text

            # mbti type results__type__code is present in class attribute
            mbti = driver.find_element(By.CLASS_NAME, "results__type__code").text
            mbti = mbti.split("\n")[1]

            result["title"] = title
            result["mbti_subtype"] = mbti 
            if '-' in mbti:
                result["mbti"] = mbti.split("-")[0]
            else:
                result["mbti"] = mbti
            # print(result["title"], result["mbti"])

        else:
            # card_name is h3 tag with "card__title" inside class attribute
            card_name = driver.find_element(By.CLASS_NAME, "card__title").text

            # parity percentage is inside class="percentage right active"
            pairty_percentage = driver.find_element(By.CLASS_NAME, "percentage").text


            result[card_name] = {
                "pairty_percentage": pairty_percentage,
            }
            # print(card_name, pairty_percentage)


        # click button with class="sp-action sp-button button--action button--blue button--md button--pill button--auto"
        next_button = driver.find_element(By.XPATH, "//button[@class='sp-action sp-button button--action button--blue button--md button--pill button--auto']")
        driver.execute_script("arguments[0].click();", next_button)

    # save the final result in json format
    import json
    with open(f"{SAVE_DIR}/result_{result_name}.json", "w") as f:
        json.dump(result, f)

    driver.quit()
    return result

def eval(choices, result_name):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://www.16personalities.com/free-personality-test")

    PAGES = 10
    for page_no in tqdm(range(PAGES)):
        radios = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "radios")))
        for r_idx, radio in enumerate(radios):
            labels = radio.find_elements(By.TAG_NAME, "label")
            VAL = choices[page_no * 6 + r_idx]
            label = labels[VAL + 3]
            driver.execute_script("arguments[0].click();", label)

        if page_no != PAGES - 1:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Go to next set of questions']"))
            )
            driver.execute_script("arguments[0].click();", next_button)
        else:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            driver.execute_script("arguments[0].click();", submit_button)

    RESULT_PAGES = 6
    SAVE_DIR = "results"
    os.makedirs(SAVE_DIR, exist_ok=True)
    result = {}

    for page_no in range(RESULT_PAGES):
        if page_no == 0:
            title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "results__type__name"))).text
            mbti = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "results__type__code"))).text
            mbti = mbti.split("\n")[1]
            result["title"] = title
            result["mbti_subtype"] = mbti
            result["mbti"] = mbti.split("-")[0] if '-' in mbti else mbti
        else:
            card_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card__title"))).text
            parity_percentage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "percentage"))).text
            result[card_name] = {"parity_percentage": parity_percentage}

        if page_no != RESULT_PAGES - 1:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='sp-action sp-button button--action button--blue button--md button--pill button--auto']"))
            )
            driver.execute_script("arguments[0].click();", next_button)

    with open(f"{SAVE_DIR}/result_{result_name}.json", "w") as f:
        json.dump(result, f)

    driver.quit()
    return result


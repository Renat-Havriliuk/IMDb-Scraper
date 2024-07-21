from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import csv

try:

    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    with webdriver.Chrome(options=options) as driver:
        driver.get('https://www.imdb.com/chart/top/')

        wait = WebDriverWait(driver, 10)

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sc-FRqyn'))).click()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sc-eKYSwk'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     '/html/body/div[2]/nav/div[2]/div[6]/div/div/div/span/ul[2]/li[2]'
                                                     )) and
                   EC.element_to_be_clickable((By.XPATH,
                                               '/html/body/div[2]/nav/div[2]/div[6]/div/div/div/span/ul[2]/li[2]'
                                               ))).click()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sc-eKYSwk'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     '/html/body/div[2]/nav/div[2]/div[6]/div/div/div/span/ul[1]/li[3]'
                                                     )) and
                   EC.element_to_be_clickable((By.XPATH,
                                               '/html/body/div[2]/nav/div[2]/div[6]/div/div/div/span/ul[1]/li[3]'
                                               ))).click()
        driver.implicitly_wait(5)
        tree = html.fromstring(driver.page_source)

    with open('data/films.csv', 'w', newline='', encoding='utf-8') as file:
        column_names = ['Title', 'Year', 'Rating', 'URL']
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()

        movie_blocks = tree.xpath('//li[contains(@class, "ipc-metadata-list-summary-item")]')

        if len(movie_blocks) == 250:
            for movie_block in movie_blocks:
                try:
                    info_block = movie_block.find('./div[2]')
                    # print(html.tostring(info_block, pretty_print=True, encoding='unicode'))
                    try:
                        title = info_block.find('./div/div/div/a/h3').text.split('.')[1].strip()
                        print(f'title: "{title}"')
                    except Exception:
                        print('Title is missing')
                    try:
                        year = info_block.find('./div/div/div[2]/span').text.strip()
                        print(f'year: "{year}"')
                    except Exception:
                        print('Year is missing')
                    try:
                        rating = info_block.find('./div/div/span/div/span/span[1]').text.strip()
                        print(f'rating: "{rating}"')
                    except Exception:
                        print('Rating is missing')
                    try:
                        url = 'https://www.imdb.com' + str(info_block.find('./div/div/div/a').get('href')).strip()
                        print(f'url: "{url}')
                    except Exception:
                        print('URL is missing')

                    writer.writerow({'Title': title, 'Year': year, 'Rating': rating, 'URL': url})

                except Exception:
                    print("The movie doesn't have info")

        else:
            print(len(movie_blocks))
            print('We got less then 250 movies')

except Exception as ex:
    print(f"We have a problem: \n {ex}")
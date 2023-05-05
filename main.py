import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import json
from unicodedata import normalize

HOST = "https://spb.hh.ru"
VACANSY = "/search/vacancy?text=python&area=1&area=2"

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def get_text(url):
    return requests.get(url, headers=get_headers()).text

if __name__ == '__main__':
    result_json = {}
    html_data = get_text(f'{HOST}{VACANSY}')
    soup = BeautifulSoup(html_data, 'lxml')
    div_tag_main = soup.find('div', id="a11y-main-content")
    div_tag_all = div_tag_main.find_all('div', class_='serp-item')
    for div_tag in div_tag_all:
        h3_tag = div_tag.find('h3')
        span_tag = h3_tag.find('span')
        link = span_tag.find('a')['href']
        page_data = get_text(link)
        if re.findall('[D,d]jango|[F,f]lask|[Д,д]жанго|[Ф,ф]ласк', page_data):
            vacancy = span_tag.find('a').text
            print(vacancy)
            company = div_tag.find('div', class_='bloko-text').text
            print(company)
            city = div_tag.find('div', {'data-qa':'vacancy-serp__vacancy-address'}).text
            print(city)
            soup_page = BeautifulSoup(page_data, 'lxml')
            div_salary_tag = soup_page.find('div', class_="vacancy-title")
            salary = div_salary_tag.find('span').text
            print(salary)

            result_json[normalize('NFKD', vacancy)] = {
                                    'link' : normalize('NFKD', link),
                                    'salary' : normalize('NFKD', salary),
                                    'company' : normalize('NFKD',company),
                                    'city' : normalize('NFKD', city)
                                                       }

    with open('result_json.json', 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)

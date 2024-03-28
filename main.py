import requests
import bs4
import fake_headers
import json


HOST = 'https://hh.ru/search/vacancy?area=1&area=2&text=Python'

headers_gen = fake_headers.Headers(os='win', browser='chrome')


response = requests.get(HOST, headers=headers_gen.generate())
main_html_data = response.text
main_soup = bs4.BeautifulSoup(main_html_data, features='lxml')

articles_list_tag = main_soup.find('div', id='a11y-main-content')

articles_tags = articles_list_tag.find_all('div', class_='vacancy-serp-item-body__main-info')
vacancy_data = []

for article_tag in articles_tags:
    a_tag = article_tag.find('a', class_='bloko-link')
    link_absolute = a_tag['href']

    span_tag = a_tag.find('span', class_='serp-item__title')
    vacancy_name = span_tag.text.strip()

    salary_tag = article_tag.find('span', attrs={'data-qa' : 'vacancy-serp__vacancy-compensation'})
    if salary_tag != None:
        salary = salary_tag.text.strip().replace('\u202f', ' ')
    else:
        salary = ''

    company_name = article_tag.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-employer'}).text.strip().replace('\xa0', ' ')
    city = article_tag.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy-address'}).text.strip().replace('\xa0', ' ')

    response = requests.get(link_absolute, headers=headers_gen.generate())
    article_html_data = response.text
    article_soup = bs4.BeautifulSoup(article_html_data, features='lxml')

    vacancy_body = article_soup.find('div', attrs={'data-qa' : 'vacancy-description'})

    if vacancy_body.find(string='Django') != None and vacancy_body.find(string='Flask') != None:
        vacancy_data.append({
            'name': vacancy_name,
            'link': link_absolute,
            'salary': salary,
            'company': company_name,
            'city': city
        })

with open('vacancy_data.json', 'w', encoding='utf-8') as fp:
    json.dump(vacancy_data, fp, ensure_ascii=False)

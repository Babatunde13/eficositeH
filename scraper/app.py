from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scholarship')
def scholarship():
    return jsonify(
        get_details_from_html(get_content())
    )

def get_content(url='https://www.intelregion.com/scholarships'):
    response = requests.get(url)
    return response.text 

def get_details_from_html(html: str) -> list:
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='td-block-span4' or 'td-bp-span4' or 'td-block-span6' or 'td_module_wrap')
    scholarships = []
    for scholarship in divs:
        res = scholarship.find('div', class_='td-module-thumb')
        new_scholarship = {
            'url': res.a['href'],
            'title': res.a['title']
        }
        new_request = requests.get(new_scholarship['url'])
        new_soup = BeautifulSoup(new_request.text, 'lxml')
        url = new_soup.find('section', 
                class_='elementor-section \
                        elementor-top-section elementor-element \
                        elementor-element-546d233a elementor-section-boxed \
                        elementor-section-height-default elementor-section-height-default'
                ).div.div.div.find('div', 
                        class_='elementor-button-wrapper').a['href']
        new_scholarship['url'] = url
        deadline = new_soup.find(
            'section',
            class_='elementor-section elementor-top-section \
                    elementor-element elementor-element-1daf00c5 \
                    elementor-section-boxed \
                    elementor-section-height-default \
                    elementor-section-height-default'
        ).div.div.div.div.div.div.div.text[9:]
        new_scholarship['deadline'] = deadline
        scholarships.append(new_scholarship)
    return scholarships

if __name__ == "__main__":
    app.run()
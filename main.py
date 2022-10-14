'''With this code you can access data from NGO DARPAN Website. DON'T USE THIS CODE FOR COMMERCIAL USE IT'S ONLY FOR LEARNING PURPOSE.
May be you guys find some ERROR in this code so I leave it to you as a Coding Challenge. Find the solution to get data as you Wish. HAPPY CODING'''

from bs4 import BeautifulSoup
import requests
import time
import csv


def get_token(sess):
    req_csrf = sess.get('https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf')
    print(req_csrf.text)
    return req_csrf.json()['csrf_token']


search_url = "https://ngodarpan.gov.in/index.php/ajaxcontroller/search_index_new/{}"
details_url = "https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info"

sess = requests.Session()
fp = open('test.csv', 'a')
for page in range(1, 30, 10):
    print(f"Getting results from {page}")

    for retry in range(1, 5):

        data = {
            'state_search': '',
            'district_search': '',
            'sector_search': 'null',
            'ngo_type_search': 'null',
            'ngo_name_search': '',
            'unique_id_search': '',
            'view_type': 'detail_view',
            'csrf_test_name': get_token(sess),
        }

        req_search = sess.post(search_url.format(page), data=data, headers={'X-Requested-With': 'XMLHttpRequest'})
        print(req_search.text)
        soup = BeautifulSoup(req_search.content, "html.parser")
        table = soup.find('table', id='example')

        if table:
            for tr in table.find_all('tr'):
                row = [td.text for td in tr.find_all('td')]
                link = tr.find('a', onclick=True)

                try:

                    if link:
                        link_number = link['onclick'].strip("show_ngif(')")
                        print(link_number)
                        req_details = sess.post(details_url, headers={'X-Requested-With': 'XMLHttpRequest'}, data={'id': link_number, 'csrf_test_name': get_token(sess)})
                        print(req_details.text)
                        json = req_details.json()
                        details = json['infor']['0']
                        
                        csv_writer = csv.writer(fp)
                        csv_writer.writerow(details)
                except KeyError:
                    continue
        
            break
        else:
            print(f'No data returned - retry {retry}')
            time.sleep(3)

fp.close()

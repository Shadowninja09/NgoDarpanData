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
for page in range(10076, 77550, 10):    # Advance 10 at a time
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
                        # print(req_details.text)
                        # json = req_details.json()
                        # details = json['infor']['0']
        #                 Operational_District = json['infor']['operational_district_db']
        #                 operational_states = json['infor']['operational_states_db']
        #                 issues_working_db = json['infor']['issues_working_db']
        #                 registration_detail = json['registeration_info'][0]
        #                 ngo_url = json['infor']['0']['ngo_url']
        #                 uniqueid_gen_dt = json['infor']['0']['last_modified_dt']
        #                 Off_phone1 = json['infor']['0']['Off_phone1']
        #                 # members_details = json['member_info'][0]
        #                 # members_details1 = json['member_info'][1]
        #                 # members_details2 = json['member_info'][2]
        #                 # members_details3 = json['member_info'][3]
        #                 # members_details4 = json['member_info'][4]
        #                 # members_details5 = json['member_info'][5]
        #                 # members_details6 = json['member_info'][6]
        #                 # members_details7 = json['member_info'][7]
        #                 # members_details8 = json['member_info'][8]
        #                 # members_details9 = json['member_info'][9]
        #                 # members_details10 = json['member_info'][10]
        #                 print([details['Mobile'], details['Email'], row[1], row[2], details['UniqueID'],
        #                        details['last_modified_dt']])
        #                 print(details)
        #                 print(registration_detail)
        #                 x = [str(row[1]), str(details['UniqueID']), str(uniqueid_gen_dt), str(registration_detail['reg_name']),
        #                      str(registration_detail['TypeDescription']), str(registration_detail['nr_regNo']),
        #                      str(registration_detail['nr_actName']), str(registration_detail['nr_city']),
        #                      str(registration_detail['StateName']), str(registration_detail['ngo_reg_date']),
        #                      str(issues_working_db), str(Operational_District), str(operational_states)]
        #
        #                 y = [str(registration_detail['nr_isFcra']),
        #                      str(registration_detail['fcrano']),
        #                      str(registration_detail['nr_add']), str(registration_detail['nr_city']),
        #                      str(registration_detail['StateName']),
        #                      str(Off_phone1), str(details['Mobile']),
        #                      str(ngo_url), str(details['Email']),
        #                      str(details['last_modified_dt']), str(registration_detail['nr_updDocId'])]
        #                 # z = [str(members_details['FName']), str(members_details['DesigName']),
        #                 #      str(members_details1['FName']), str(members_details1['DesigName'])
        #                      # str(members_details2['FName']), str(members_details2['DesigName']),
        #                      # str(members_details3['FName']), str(members_details3['DesigName']),
        #                      # str(members_details4['FName']), str(members_details4['DesigName']),
        #                      # str(members_details5['FName']), str(members_details5['DesigName']),
        #                      # str(members_details6['FName']), str(members_details6['DesigName']),
        #                      # str(members_details7['FName']), str(members_details7['DesigName']),
        #                      # str(members_details8['FName']), str(members_details8['DesigName']),
        #                      # str(members_details9['FName']), str(members_details9['DesigName']),
        #                      # str(members_details10['FName']), str(members_details10['DesigName'])
        #                 #     ]
        #
        #                 csv_writer = csv.writer(fp)
        #                 csv_writer.writerow(x+y)
        #                     #csv_writer.writerow(details)
                except KeyError:
                    continue
        #
        #     break
        # else:
        #     print(f'No data returned - retry {retry}')
        #     time.sleep(3)

fp.close()
# RSNV FOUNDATION
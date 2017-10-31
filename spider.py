# -*- coding: utf-8 -*-

# Pre-requirement install below packages
# pip install bs4
# pip install requests

# import urllib previous used this one, BeautifulSoup has the same functionality
import requests
from bs4 import BeautifulSoup
import json
import time


def crawl_details(id):
    url = 'https://www.lagou.com/jobs/%s.html' % id
    headers = {
    'Host':'www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3218.0 Safari/537.36'
    }

    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')
    job_bt = soup.find('dd',attrs={'class':'job_bt'})
    print(job_bt.text)
    # print(req.content.decode('utf-8','ignore'))
    return job_bt.text




def main():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3218.0 Safari/537.36',
        'Host':'www.lagou.com',
        'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code':'0',
        'X-Anit-Forge-Token':'None',
        'X-Requested-With':'XMLHttpRequest'
    }

    # form_data = {
    #     'first':'true',
    #     'pn':'1',
    #     'kd':'python'
    # }

    # 由于站点使用了post请求，而爬虫使用get 最后获取的都是假数据
    # 此处要改为post，使用post需要发送表单数据给服务器获取数据
    # result = requests.post('https://www.lagou.com/jobs/positionAjax.json?'
    #                       'city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0',
                           # headers=headers, data=form_data)
    # print(result.content.decode('utf-8','ignore')) # In order to avoid hex code using decode to decode the data

    # json_result = result.json()
    # print(json_result)
    # positions = json_result['content']['positionResult']['result']

    # for position in positions:
        # print ('-'*40)
        # print(position)

    # line = json.dumps(positions, ensure_ascii=False)
    # with open('lagou.json','wb') as fp:
    #     fp.write(line.encode('utf-8'))

    positions = []
    for x in range(1,31):
        form_data = {
            'first': 'true',
            'pn': x,
            'kd': 'python'
        }

        result = requests.post('https://www.lagou.com/jobs/positionAjax.json?'
                               'city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0',
                               headers=headers, data=form_data)
        json_result = result.json()
        print('-'*50)
        print(json_result)
        print('-' * 50)
        page_positions = json_result['content']['positionResult']['result']
        for position in page_positions:
            position_dict = {
            'position_name':position['positionName'],
            'work_year':position['workYear'],
            'salary':position['salary'],
            'district':position['district'],
            'company_name':position['companyFullName']
            }
            position_id = position['positionId']
            position_detail = crawl_details(position_id)
            

        positions.extend(page_positions)
        time.sleep(3)

    line = json.dumps(positions, ensure_ascii=False)
    with open('lagou.json','wb') as fp:
        fp.write(line.encode('utf-8'))











if __name__ == '__main__':
   # main()
   crawl_details('914413')


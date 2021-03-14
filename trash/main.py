from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Host': 'www.guazi.com',
    'Connection': 'keep-alive',
    'Cookie': 'cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22c95877c1-4106-4c0e-b21c-5f2d3a0b4643%22%2C%22ca_city%22%3A%22hrb%22%2C%22sessionid%22%3A%22a5ba764a-a664-4ec2-c763-fdf802ff4110%22%7D; cityDomain=bj; sessionid=a5ba764a-a664-4ec2-c763-fdf802ff4110; Hm_lpvt_bf3ee5b290ce731c7a4ce7a617256354=1613197828; Hm_lvt_bf3ee5b290ce731c7a4ce7a617256354=1613110210,1613111180,1613197816; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A51991822010%7D; clueSourceCode=%2A%2300; lg=1; uuid=c95877c1-4106-4c0e-b21c-5f2d3a0b4643; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; close_finance_popup=2021-02-13; gps_type=1; lng_lat=126.618481_45.737069; preTime=%7B%22last%22%3A1613197815%2C%22this%22%3A1613110209%2C%22pre%22%3A1613110209%7D; user_city_id=12; ganji_uuid=7649021131000891196847; antipas=2U21Q711533O8113i7H724045r0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://www.guazi.com/bj/',
}

url_list = ['https://www.guazi.com/wh/4740cda76ff85d1cx.htm#fr_page=index&fr_pos=jiangjia&fr_no=2',
            'https://www.guazi.com/bj/db7ec5e3c1db7af7x.htm#fr_page=index&fr_pos=rec&fr_no=0',
            'https://www.guazi.com/rizhao/62c72795d880933ex.htm#fr_page=index&fr_pos=new&fr_no=6',
            'https://www.guazi.com/rizhao/24e84846ed7135c5x.htm#fr_page=index&fr_pos=new&fr_no=7',
            'https://www.guazi.com/wx/352dcabd5198cc5dx.htm#fr_page=index&fr_pos=new&fr_no=0']
outputs = dict()
for i, url in enumerate(url_list):
    response = requests.get(url,  headers=headers, timeout=30).content
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
    content = soup.html
    head = content.find_all(class_='basic-eleven clearfix')[0]
    head_json = dict()
    for index in range(len(head)):
        if head.contents[index] == '\n':
            continue
        square = head.contents[index]
        key = square.contents[-1].replace('\r\n', '')
        value = square.text.split('\r')[0].replace('\n', '')
        value = value.split(' ')[0]
        head_json[key] = value

    # 6 params table
    params = content.find_all(class_='detailcontent clearfix js-detailcontent active')[0]
    params_json = dict()
    for index in range(len(params)-2):
        if params.contents[index] == '\n':
            continue
        # table title
        value_soup = params.contents[index]
        value_dict = dict()
        key = value_soup.contents[1].text.replace('\n','')
        # search in one param table by lines
        for child_index in range(3, len(value_soup) - 1):
            child_key = value_soup.contents[child_index].contents[0].string
            child_value = value_soup.contents[child_index].contents[1].string
            value_dict[child_key] = child_value
        params_json[key] = value_dict

    outputs[i] = {'head': head_json, 'params': params_json}

with open('output.json', 'w') as f:
    f.write(json.dumps(outputs, indent=1))

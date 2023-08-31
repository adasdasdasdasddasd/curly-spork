import re
import execjs
import requests


index_url = "https://xueqiu.com/today"
news_test_url = "https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=15"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://xueqiu.com/today',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_complete_cookie():
    complete_cookie = {}
    # 第一次不带参数访问首页，获取 acw_tc 和 acw_sc__v2
    response = requests.get(url=index_url, headers=headers)
    complete_cookie.update(response.cookies.get_dict())
    arg1 = re.findall("arg1='(.*?)'", response.text)[0]
    with open('acw_sc_v2.js', 'r', encoding='utf-8') as f:
        acw_sc_v2_js = f.read()
    acw_sc__v2 = execjs.compile(acw_sc_v2_js).call('getcookie_v2', arg1)
    complete_cookie.update({"acw_sc__v2": acw_sc__v2})

    # 第二次访问首页，获取其他 cookies
    response2 = requests.get(url=index_url, headers=headers, cookies=complete_cookie)
    complete_cookie.update(response2.cookies.get_dict())
    return complete_cookie


def news_test(cookies):
    response = requests.get(url=news_test_url, headers=headers, cookies=cookies)
    print(response.json())


if __name__ == '__main__':
    complete_cookie = get_complete_cookie()
    news_test(complete_cookie)
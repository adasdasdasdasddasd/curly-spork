import execjs
import requests

news_est_url = "https://max.pedata.cn/api/q4x/newsflash/list"
login_token = "424a86714113e18879e2ddd853473aa82fcb75f59df3512c8692bc561dca3bc4"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'Hm_lvt_0d052dd2e4e34a214d13e86591990a09=1692604689; SESSION=OTE1ZDA5MTYtMWRkNi00NjcyLTk1NTEtZTFiNjI0NzQwYTkx; Hm_lpvt_0d052dd2e4e34a214d13e86591990a09=1692609377',
    'HTTP-X-TOKEN': login_token,
    'Origin': 'https://max.pedata.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://max.pedata.cn/client/news/newsflash',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'testxor': 'testxor',
}


def get_decrypted_data(encrypted_data, exor):
    with open('PEDATA.js', 'r', encoding='utf-8') as f:
        pedata_js = f.read()
    decrypted_data = execjs.compile(pedata_js).call('q', encrypted_data, exor, login_token)
    return decrypted_data


def get_encrypted_data():
    data = {
        "type": "",
        "module": "LP",
        "page":
            {
                "currentPage": 1,
                "pageSize": 10
            }
    }
    response = requests.post(url=news_est_url, headers=headers, json=data).json()
    encrypted_data, exor = response["data"], response["exor"]
    return encrypted_data, exor


def main():
    encrypted_data, exor = get_encrypted_data()
    decrypted_data = get_decrypted_data(encrypted_data, exor)
    print(decrypted_data)


if __name__ == '__main__':
    main()
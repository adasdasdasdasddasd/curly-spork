import base64
import json
import re

import execjs
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'dcode=101010100; SECKEY_ABVK=Jd/3w7xrhadxXWvdr6JW4dY5gzielZ4OdDfFyTiDThg%3D; BMAP_SECKEY=mvJo1E1jn8GgqMqlNkuO1unrVfR9onllQY66ai_orxIVzoFKz1s7IYA_d5H_XBfJCG6Ce9W3ASTCn1lFnlBHYmJgH1zzXQaeIabU3q7acEt5mVamhNHJJXQ74N3se_fYS1X3eDCTH9ry0rqM8uog5lWGqDEqJ_PpMI9lqggZGNeOckK_jS8D_8ZYWymjr2j4; dcity=%E5%8C%97%E4%BA%AC; Hm_lvt_6088e7f72f5a363447d4bafe03026db8=1692683719; Hm_lpvt_6088e7f72f5a363447d4bafe03026db8=1692686832',
    'Pragma': 'no-cache',
    'Referer': 'https://www.aqistudy.cn/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
def get_encrypted_js_url():
    url= 'https://www.aqistudy.cn/html/city_realtime.php'
    text= requests.get(url=url, headers=headers).text
    encrypted_js = re.findall(r'encrypt_(\w+)\.min\.js',text)[0]
    encrypted_js_url = f'https://www.aqistudy.cn/js/encrypt_{encrypted_js}.min.js'
    print(encrypted_js_url)


    return encrypted_js_url

def get_decrypted_js(encrypted_js_url):
    """
    :param encrypted_js_url: encrypt_xxxxxx.js 的地址
    :return: 解密后的 JS
    """
    decrypted_js = requests.get(url=encrypted_js_url, headers=headers).text
    flag = True
    while flag:
        if "eval(function" in decrypted_js:
            # 需要执行 eval
            print("需要执行 eval！")
            replace_js = decrypted_js.replace("eval(function", "(function")
            decrypted_js = execjs.eval(replace_js)
        elif "dswejwehxt(" in decrypted_js:
            # 需要 base64 解码
            base64_num = decrypted_js.count("dswejwehxt(")
            print("需要 %s 次 base64 解码！" % base64_num)
            decrypted_js = re.findall(r"\('(.*?)'\)", decrypted_js)[0]
            num = 0
            while base64_num > num:
                decrypted_js = base64.b64decode(decrypted_js).decode()
                num += 1
        else:
            # 得到明文
            flag = False
    return decrypted_js

def get_key_iv_appid(decrypted_js):
    """
    :param decrypted_js: 解密后的 encrypt_xxxxxx.js
    :return: 请求必须的一些参数
    """
    key_iv = re.findall(r'const.*?"(.*?)";', decrypted_js)
    app_id = re.findall(r"var appId.*?'(.*?)';", decrypted_js)
    request_data_name = re.findall(r"aqistudyapi.php.*?data.*?{(.*?):", decrypted_js, re.DOTALL)

    # 判断 param 是 AES 加密还是 DES 加密还是没有加密
    if "AES.encrypt(param" in decrypted_js:
        request_param_encrypt = "AES"
    elif "DES.encrypt(param" in decrypted_js:
        request_param_encrypt = "DES"
    else:
        request_param_encrypt = "NO"

    key_iv_appid = {
        # key 和 iv 的位置和原来 js 里的是一样的
        "aes_key_1": key_iv[0],
        "aes_iv_1": key_iv[1],
        "aes_key_2": key_iv[2],
        "aes_iv_2": key_iv[3],
        "des_key_1": key_iv[4],
        "des_iv_1": key_iv[5],
        "des_key_2": key_iv[6],
        "des_iv_2": key_iv[7],
        "app_id": app_id[0],
        # 发送请求的 data 的键名
        "request_data_name": request_data_name[0].strip(),
        # 发送请求的 data 值需要哪种加密
        "request_param_encrypt": request_param_encrypt
    }
    # print(key_iv_appid)
    return key_iv_appid

def get_data(key_iv_appid):
    """
    :param key_iv_appid: get_key_iv_appid() 方法返回的值
    """
    request_method = "GETDATA"
    request_city = {"city": "北京"}
    with open('KONGQI.js', 'r', encoding='utf-8') as f:
        execjs_ = execjs.compile(f.read())

    # 根据不同加密方式调用不同方法获取请求加密的 param 参数
    request_param_encrypt = key_iv_appid["request_param_encrypt"]
    if request_param_encrypt == "AES":
        param = execjs_.call(
            'getRequestAESParam', request_method, request_city,
            key_iv_appid["app_id"], key_iv_appid["aes_key_2"], key_iv_appid["aes_iv_2"]
        )
    elif request_param_encrypt == "DES":
        param = execjs_.call(
            'getRequestDESParam', request_method, request_city,
            key_iv_appid["app_id"], key_iv_appid["des_key_2"], key_iv_appid["des_iv_2"]
        )
    else:
        param = execjs_.call('getRequestParam', request_method, request_city, key_iv_appid["app_id"])
    data = {
        key_iv_appid["request_data_name"]: param
    }
    response = requests.post(url='https://www.aqistudy.cn/apinew/aqistudyapi.php', headers=headers, data=data).text
    # print(response)

    # 对获取的加密数据解密
    decrypted_data = execjs_.call(
        'getDecryptedData', response,
        key_iv_appid["aes_key_1"], key_iv_appid["aes_iv_1"],
        key_iv_appid["des_key_1"], key_iv_appid["des_iv_1"]
    )
    print(json.loads(decrypted_data))
#
if __name__ == '__main__':
    # get_encrypted_js_url()
    result = get_data(get_key_iv_appid(get_decrypted_js(get_encrypted_js_url())))
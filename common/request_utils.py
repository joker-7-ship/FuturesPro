"""
============================
Project:BtccFuturesProApiTest
Address:https://www.cryptouat.com/
Author:Binea
Time:2024/11
============================
"""
import hashlib,json
import urllib.parse
import requests
import time
from common.config import SECRET_KEY, BASE_URL

# # 获取服务器时间戳
# def get_server_time():
#     response = requests.get("url", verify=False)
#     if response.status_code == 200:
#         return response.json()["data"]
#     else:
#         raise Exception("无法获取服务器时间")
# 获取本地时间戳
def get_server_time():
    timestamp = int(time.time())
    return timestamp

# 对参数进行排序并生成 MD5 签名
def generate_signature(params):
    param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
    param_str_with_key = f'{param_str}&secret_key={SECRET_KEY}'
    sorted_param_str = '&'.join(sorted(param_str_with_key.split('&')))
    md5_signature = hashlib.md5(sorted_param_str.encode('utf-8')).hexdigest()
    return md5_signature

# headers生成
def prepare_request(params):
    signature = generate_signature(params)
    return {'authorization': signature}

# 构造 POST 请求
def post_request(endpoint, params, verify=False):
    url = f"{BASE_URL}{endpoint}"
    headers = prepare_request(params)
    response = requests.post(url, headers=headers, json=params, verify=verify)
    print(response)
    response.raise_for_status()
    return response.json()

# 构造 GET 请求
def get_request(endpoint, params=None, verify=False):
    params = params or {}
    url = f"{BASE_URL}{endpoint}?{urllib.parse.urlencode(params)}"
    headers = prepare_request(params)
    response = requests.get(url, headers=headers, verify=verify)
    response.raise_for_status()
    return response.json()
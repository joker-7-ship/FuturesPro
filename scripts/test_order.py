import requests
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FuturesPro')))
from common.request_utils import post_request, get_request, get_server_time
from data.order_data import put_limit
from common.config import Token_data



@pytest.fixture
def server_time():
    """加载时间戳"""
    return get_server_time()

@pytest.fixture(scope='session')
def token():
    """获取老合约Token"""
    response_login = requests.post(url="https://api1.cryptouat.com:9081/v1/user/login", data=Token_data)
    response_login_data = response_login.json()
    print(response_login.json)
    assert "token" in response_login_data, f"!!!Fail!!!: {response_login_data}"
    return response_login_data["token"]

def validate_response(response, expected_message='OK', request_params=None):
    """通用断言, 不通过打印请求和响应.正确断言应该是'OK',前期调试需要先让它不生效"""
    if response.get('message') != expected_message:
        print("Request!!!", request_params)
        print("Response!!!", response)
        raise AssertionError(f"Expected message '{expected_message}', but got '{response.get('message')}'")

class TestBtcc:
    # # 下限价单
    # @pytest.mark.parametrize("data", put_limit)
    # def test_putLimit(self, server_time, token, data):
    #     params = {
    #         "token": token,  # 获取token
    #         "market": data["market"],  # 市场名称，如BTCUSDT
    #         "side": data["side"],  # 1为多，2为空
    #         "amount": data["amount"],
    #         "price": data["price"],  # 限价单，后期应该要获取对手盘一档价格，前期可以开多先输比较低，开空可以输入比较高的价格
    #         "source": data["source"],  # 传空
    #         "price_way": data["price_way"],  # 止盈止损价格触发类型
    #         "sl_price": data["sl_price"],  # 止损价
    #         "tp_price": data["tp_price"],  # 止盈价
    #         "sl_type": data["sl_type"],  # 止损价格不为空就传
    #         "tp_type": data["tp_type"],  # 止盈价格不为空就传
    #         "sl_limit_price": data["sl_limit_price"],  # sl_type是2就传
    #         "tp_limit_price": data["tp_limit_price"],  # tp_type是2就传
    #         "tm": server_time
    #     }
    #     print(params)
    #     response = post_request("/btcc_perpetual/order/put_limit", params)
    #     validate_response(response, request_params=params)

    # 获取行情价格
    # def test_GetMarket(self, server_time, token):
    #     params = {
    #         "market": "BTCUSDT",
    #         "tm":server_time
    #     }
    #     response = get_request("/btcc_perpetual/market/last", params)
    #     validate_response(response, request_params=params)
    #     global price
    #     price = response['data']
    #     print(price)
    #
    # # 下市价单
    # def test_PutMarket(self, server_time, token):
    #     params = {
    #         "token": token,
    #         "leader_id":10010000021775,
    #         "market":"BTCUSDT",
    #         "side":1,
    #         "amount":"0.01",
    #         "tm":server_time
    #     }
    #     response = post_request("/btcc_perpetual/order/put_market", params)
    #     print(params)
    #     validate_response(response, request_params=params)
    #
    def test_Posion(self,server_time,token):
        params = {
            "token": token,
            "leader_id":10010000021775,
            "market":"N",
            "tm":server_time
        }
        response = get_request("/btcc_perpetual/position/pending", params)
        print(params)
        validate_response(response, request_params=params)
        print(response)

    # def test_Asset(self,server_time,token):
    #     params = {
    #         "token": token,
    #         "leader_id": 10010000021775,
    #         "asset":"USDT",
    #         "tm": server_time
    #     }
    #     response = get_request("/btcc_perpetual/asset/query_users", params)
    #     print(response)

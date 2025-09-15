import requests
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../common')))
from common.request_utils import post_request, get_request, get_server_time
from data.asset_data import History
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

def validate_response(response, expected_message='OK!', request_params=None):
    """通用断言, 不通过打印请求和响应.正确断言应该是'OK',前期调试需要先让它不生效"""
    if response.get('message') != expected_message:
        print("Request!!!", request_params)
        print("Response!!!", response)
        raise AssertionError(f"Expected message '{expected_message}', but got '{response.get('message')}'")

class TestBtcc:
    # 获取交易币种列表
    def test_assetList(self, server_time,token):
        params = {
            "token": token,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/asset/list", params)
        validate_response(response, request_params=params)

    # 获取账户余额
    def test_querybalance(self, server_time, token):
        params = {"token": token, "tm": server_time}
        response = get_request("/btcc_perpetual/asset/query", params)
        validate_response(response, request_params=params)

    # 获取用户资金流水
    @pytest.mark.parametrize("data", History)
    def test_History(self, server_time, token, data):
        params = {
            "token": token,
            "tm": server_time,
            "business": data["business"],
            "offset": data["offset"],
            "limit": data["limit"]
        }
        response = get_request("/btcc_perpetual/asset/history_all", params)
        validate_response(response, request_params=params)
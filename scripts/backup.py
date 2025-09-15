import requests
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../common')))
from common.request_utils import post_request, get_request, get_server_time
from data.asset_data import history_all,market_preference,AdjustMargin,AdjustLeverage
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
    # 获取市场列表
    def test_markelist(self, server_time):
        params = {"tm": server_time}
        response = get_request("/btcc_perpetual/market/list", params)
        validate_response(response, request_params=params)

    # 获取用户的市场仓位配置
    @pytest.mark.parametrize("data", market_preference)
    def test_get_preference(self, server_time,token,data):
        params = {
            "token": token,
            "market":data["market"],
            "side":data["side"],
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/get_preference", params)
        validate_response(response, request_params=params)

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
    @pytest.mark.parametrize("data", history_all)
    def test_history_all(self, server_time, token, data):
        params = {
            "token": token,
            "tm": server_time,
            "business": data["business"],
            "offset": data["offset"],
            "limit": data["limit"]
        }
        response = get_request("/btcc_perpetual/asset/history_all", params)
        validate_response(response, request_params=params)

    # 查询用户当前仓位列表
    @pytest.mark.parametrize("data", market_preference)
    def test_PositionPending(self, server_time,token,data):
        params = {
            "token": token,
            "market":data["market"],
            "side":data["side"],
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/position/pending", params)
        validate_response(response, request_params=params)

    # 查询用户历史仓位
    @pytest.mark.parametrize("data", market_preference)
    def test_PositionFinished(self, server_time,token,data):
        params = {
            "token": token,
            "market":data["market"],
            "start_time": 0,
            "end_time": 0,
            "side":data["side"],
            "offset": 0,
            "limit": 100,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/position/pending", params)
        global position_id
        position_id = response['records']['position_id']
        validate_response(response, request_params=params)

    # 查询仓位成交记录
    def test_PositionDeals(self, server_time,token,data):
        params = {
            "token": token,
            "position_id":position_id,
            "offset": 0,
            "limit": 100,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/position/deals", params)
        validate_response(response, request_params=params)

    # 调整用户仓位保证金
    @pytest.mark.parametrize("data", AdjustMargin)
    def test_AdjustMargin(self, server_time,token,data):
        params = {
            "token": token,
            "market":data["market"],
            "type": data["type"],
            "amount":data["amount"],
            "side":data["side"],
            "tm": server_time
        }
        response = post_request("/btcc_perpetual/position/adjust_margin", params)
        validate_response(response, request_params=params)

    # 查询用户仓位保证金调整记录
    @pytest.mark.parametrize("data", AdjustMargin)
    def test_PositionMargin(self, server_time,token,data):
        params = {
            "token": token,
            "position_id":position_id,
            "offset": 0,
            "limit": 100,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/position/margins", params)
        validate_response(response, request_params=params)

    # 查询用户仓位的历史资金费用
    @pytest.mark.parametrize("data", market_preference)
    def test_PositionFunding(self, server_time,token,data):
        params = {
            "token": token,
            "market":data["market"],
            "start_time": 0,
            "end_time": 0,
            "side":data["side"],
            "offset": 0,
            "limit": 100,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/position/funding", params)
        validate_response(response, request_params=params)

    # 调整仓位杠杆与模式
    @pytest.mark.parametrize("data", AdjustLeverage)
    def test_AdjustLeverage(self, server_time,token,data):
        params = {
            "token": token,
            "market":data["market"],
            "position_type": data["position_type"],
            "side":data["side"],
            "leverage":data["leverage"],
            "tm": server_time
        }
        response = post_request("/btcc_perpetual/market/adjust_leverage", params)
        validate_response(response, request_params=params)


    # 查询止盈止损单
    def test_querysltp(self, server_time, token):
        params = {
            "token": token,
            "tm": server_time
        }
        response = post_request("/btcc_perpetual/contract/sltp/query", params)
        validate_response(response, request_params=params)

    # 查询市场状态
    def test_marketstatus(self, server_time, token):
        params = {"market": "BTCUSDT", "tm": server_time,"period":"86400"}
        response = get_request("/btcc_perpetual/market/status", params)
        validate_response(response, request_params=params)
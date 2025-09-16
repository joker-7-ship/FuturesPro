import requests
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../common')))
from common.request_utils import post_request, get_request, get_server_time
from data.market_data import Market,AdjustLeverage
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
    # 获取阶梯维持保证金档位
    @pytest.mark.parametrize("data", Market)
    def test_LimitConfig(self, server_time,data):
        params = {
            "market":data["market"],
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/limit_config", params)
        print(response)
        validate_response(response, request_params=params)
    # 获取市场深度
    @pytest.mark.parametrize("data", Market)
    def test_depth(self,server_time,data):
        params = {
            "market": data["market"],
            "limit":3,
            "interval":"0.00001",
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/order/depth", params)
        print(response)
        validate_response(response, request_params=params)
    # 获取市场最新价
    @pytest.mark.parametrize("data", Market)
    def test_depth(self,server_time,data):
        params = {
            "market": data["market"],
            "limit":3,
            "interval":"0.00001",
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/last", params)
        print(response)
        validate_response(response, request_params=params)


    # # 获取市场最新成交列表
    @pytest.mark.parametrize("data", Market)
    def test_MarketDeals(self, server_time,data):
        params = {
            "market":data["market"],
            "limit":1000,
            "last_id":1,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/deals", params)
        print(response)
        validate_response(response, request_params=params)

    # 查询市场状态
    @pytest.mark.parametrize("data", Market)
    def test_MarketStatus(self, server_time,data):
        params = {
            "market":data["market"],
            "period":86400,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/status", params)
        validate_response(response, request_params=params)

    # 查询市场k线
    @pytest.mark.parametrize("data", Market)
    def test_MarketKline(self, server_time,data):
        params = {
            "market":"BTCUSDT_INDEXPRICE",
            "start": 86400,
            "end": 86400,
            "interval":6,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/kline", params)
        validate_response(response, request_params=params)


    # 查询市场历史资金费率
    @pytest.mark.parametrize("data", Market)
    def test_FundingHistory(self, server_time,data):
        params = {
            "market":data["market"],
            "start_time": 0,
            "end_time": 0,
            "offset": 0,
            "limit": 100,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/funding_history", params)
        validate_response(response, request_params=params)

    # 查询保险基金
    @pytest.mark.parametrize("data", Market)
    def test_MarketInsurances(self, server_time,data):
        params = {
            "market":data["market"],
        }
        response = post_request("/btcc_perpetual/market/insurances", params)
        validate_response(response, request_params=params)

    # 查询历史保险基金
    @pytest.mark.parametrize("data", Market)
    def test_HistoryInsurances(self, server_time,data):
        params = {
            "market":data["market"],
            "type":1,
            "start_time": 0,
            "end_time": 0,
            "offset": 0,
            "limit": 100,
            "tm": server_time
        }
        response = get_request("/btcc_perpetual/market/insurance_history", params)
        validate_response(response, request_params=params)





















    # # 获取市场列表
    # def test_markelist(self, server_time):
    #     params = {"tm": server_time}
    #     response = get_request("/btcc_perpetual/market/list", params)
    #     validate_response(response, request_params=params)
    #
    # # 获取用户的市场仓位配置
    # @pytest.mark.parametrize("data", Market)
    # def test_get_preference(self, server_time,token,data):
    #     params = {
    #         "token": token,
    #         "market":data["market"],
    #         "side":data["side"],
    #         "tm": server_time
    #     }
    #     response = get_request("/btcc_perpetual/market/get_preference", params)
    #     validate_response(response, request_params=params)
    #
    # # 调整仓位杠杆与模式
    # @pytest.mark.parametrize("data", AdjustLeverage)
    # def test_AdjustLeverage(self, server_time,token,data):
    #     params = {
    #         "token": token,
    #         "market":data["market"],
    #         "position_type": data["position_type"],
    #         "side":data["side"],
    #         "leverage":data["leverage"],
    #         "tm": server_time
    #     }
    #     response = post_request("/btcc_perpetual/market/adjust_leverage", params)
    #     validate_response(response, request_params=params)
    #
    # # 查询用户历史仓位
    # @pytest.mark.parametrize("data", Market)
    # def test_UserDeals(self, server_time,token,data):
    #     params = {
    #         "token": token,
    #         "market":data["market"],
    #         "start_time": 0,
    #         "end_time": 0,
    #         "side":data["side"],
    #         "offset": 0,
    #         "limit": 100,
    #         "tm": server_time
    #     }
    #     response = get_request("/btcc_perpetual/market/user_deals", params)
    #     global position_id
    #     position_id = response['records']['position_id']
    #     validate_response(response, request_params=params)
    #
    #
    #






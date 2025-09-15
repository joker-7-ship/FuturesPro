import asyncio
import websockets
import json
import ssl
import hashlib
from common.config import API_KEY,SECRET_KEY,WSS_URL

# 计算 SHA256 签名
def calculate_sign(access_key):
    return hashlib.sha256(access_key.encode()).hexdigest()

async def connect_to_websocket():
    # 忽略证书验证
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(WSS_URL, ssl=ssl_context, compression='deflate') as websocket:
        # 鉴权
        sign_data = calculate_sign(SECRET_KEY)
        auth_request = {
            "method": "server.accessid_auth",
            "params": [API_KEY, sign_data],
            "id": 1
        }
        await websocket.send(json.dumps(auth_request))
        response = await websocket.recv()
        print("鉴权响应:", response)

        # 发送 ping
        ping_request = {
            "method": "server.ping",
            "params": ["ping"],
            "id": 2
        }
        await websocket.send(json.dumps(ping_request))
        ping_response = await websocket.recv()
        print("Ping 响应:", ping_response)

        # 获取服务器时间
        time_request = {
            "method": "server.time",
            "params": [],
            "id": 3
        }
        await websocket.send(json.dumps(time_request))
        time_response = await websocket.recv()
        print("服务器时间响应:", time_response)

        # 查询K线
        kline_request = {
            "method": "kline.query",
            "params": ["BTCUSDT", 1724119234, 1724119294, 60],
            "id": 4
        }
        await websocket.send(json.dumps(kline_request))
        kline_response = await websocket.recv()
        print("K线查询响应:", kline_response)

        # 订阅 K 线
        kline_subscribe_request = {
            "method": "kline.subscribe",
            "params": ["BTCUSDT", 1],
            "id": 2
        }
        await websocket.send(json.dumps(kline_subscribe_request))
        kline_subscribe_response = await websocket.recv()
        print("K线订阅响应:", kline_subscribe_response)

        # 取消订阅 K 线
        kline_unsubscribe_request = {
            "method": "kline.unsubscribe",
            "params": [],
            "id": 7
        }
        await websocket.send(json.dumps(kline_unsubscribe_request))
        kline_unsubscribe_response = await websocket.recv()
        print("K线取消订阅响应:", kline_unsubscribe_response)

        # 查询深度
        depth_query_request = {
            "method": "depth.query",
            "params": ["BTCUSDT", 5, "0.01"],
            "id": 3
        }
        await websocket.send(json.dumps(depth_query_request))
        depth_response = await websocket.recv()
        print("深度查询响应:", depth_response)

        # 订阅深度
        depth_subscribe_request = {
            "method": "depth.subscribe",
            "params": ["BTCUSDT", 5, "0.01"],
            "id": 4
        }
        await websocket.send(json.dumps(depth_subscribe_request))
        depth_subscribe_response = await websocket.recv()
        print("深度订阅响应:", depth_subscribe_response)

        # 取消订阅深度
        depth_unsubscribe_request = {
            "method": "depth.unsubscribe",
            "params": [],
            "id": 8
        }
        await websocket.send(json.dumps(depth_unsubscribe_request))
        depth_unsubscribe_response = await websocket.recv()
        print("深度取消订阅响应:", depth_unsubscribe_response)

        # 查询市场状态
        state_query_request = {
            "method": "state.query",
            "params": ["BTCUSDT", 86400],
            "id": 5
        }
        await websocket.send(json.dumps(state_query_request))
        state_response = await websocket.recv()
        print("市场状态查询响应:", state_response)

        # 订阅市场状态
        state_subscribe_request = {
            "method": "state.subscribe",
            "params": ["BTCUSDT", 86400],
            "id": 2
        }
        await websocket.send(json.dumps(state_subscribe_request))
        state_subscribe_response = await websocket.recv()
        print("市场状态订阅响应:", state_subscribe_response)

        # 取消订阅市场状态
        state_unsubscribe_request = {
            "id": 1,
            "method": "state.unsubscribe",
            "params": []
        }
        await websocket.send(json.dumps(state_unsubscribe_request))
        state_unsubscribe_response = await websocket.recv()
        print("市场状态取消订阅响应:", state_unsubscribe_response)

        # 查询最新成交
        deals_query_request = {
            "method": "deals.query",
            "params": ["BTCUSDT", 100, 0],
            "id": 3
        }
        await websocket.send(json.dumps(deals_query_request))
        deals_response = await websocket.recv()
        print("最新成交查询响应:", deals_response)

        # 查询用户最新成交
        deals_query_user_request = {
            "method": "deals.query_user",
            "params": [0, "BTCUSDT", 0, 0, 0, 0, 10],
            "id": 2
        }
        await websocket.send(json.dumps(deals_query_user_request))
        deals_query_user_response = await websocket.recv()
        print("用户最新成交查询响应:", deals_query_user_response)

        # 订阅最新成交
        deals_subscribe_request = {
            "method": "deals.subscribe",
            "params": [
                "BTCUSDT",
                "ETHUSDT"
            ],
            "id": 4
        }
        await websocket.send(json.dumps(deals_subscribe_request))
        deals_subscribe_response = await websocket.recv()
        print("最新成交订阅响应:", deals_subscribe_response)


        # 取消订阅市场状态
        state_unsubscribe_request = {
            "method": "deals.unsubscribe",
            "params": [],
            "id": 5
        }
        await websocket.send(json.dumps(state_unsubscribe_request))
        state_unsubscribe_response = await websocket.recv()
        print("市场状态取消订阅响应:", state_unsubscribe_response)

    # 查询订单
        order_query_request = {
            "method": "order.query",
            "params": ["BTCUSDT", 1, 0, 100],
            "id": 7
        }
        await websocket.send(json.dumps(order_query_request))
        order_response = await websocket.recv()
        print("订单查询响应:", order_response)

    # 查询计划委托单
        order_stop_query_request = {
            "method": "order.query_stop",
            "params": ["BTCUSDT", 0, 0, 100],
            "id": 8
        }
        await websocket.send(json.dumps(order_stop_query_request))
        order_stop_response = await websocket.recv()
        print("计划委托单查询响应:", order_stop_response)

    # 查询用户订单
        order_account_query_request = {
            "method": "order.account_query",
            "params": [0, "BTCUSDT", 0, 0, 100],
            "id": 9
        }
        await websocket.send(json.dumps(order_account_query_request))
        order_account_response = await websocket.recv()
        print("用户订单查询响应:", order_account_response)

    # 查询用户计划委托单
        order_account_query_stop_request = {
            "method": "order.account_query_stop",
            "params": [0, "BTCUSDT", 0, 0, 100],
            "id": 2
        }
        await websocket.send(json.dumps(order_account_query_stop_request))
        order_account_query_stop_response = await websocket.recv()
        print("用户计划委托单查询响应:", order_account_query_stop_response)

    # 订阅订单
        order_subscribe_request = {
            "method": "order.subscribe",
            "params": [],
            "id": 3
        }
        await websocket.send(json.dumps(order_subscribe_request))
        order_subscribe_response = await websocket.recv()
        print("订单订阅响应:", order_subscribe_response)

    # 取消订阅订单
        order_unsubscribe_request = {
            "id": 6,
            "method": "order.unsubscribe",
            "params": []
        }
        await websocket.send(json.dumps(order_unsubscribe_request))
        order_unsubscribe_response = await websocket.recv()
        print("订单取消订阅响应:", order_unsubscribe_response)

    # 查询资产
        asset_query_request = {
            "id": 1,
            "method": "asset.query",
            "params": [16094]
        }
        await websocket.send(json.dumps(asset_query_request))
        asset_query_response = await websocket.recv()
        print("资产查询响应:", asset_query_response)

    # 订阅资产
        asset_subscribe_request = {
            "id": 5,
            "method": "asset.subscribe",
            "params": []
        }
        await websocket.send(json.dumps(asset_subscribe_request))
        asset_subscribe_response = await websocket.recv()
        print("资产订阅响应:", asset_subscribe_response)

    # 取消订阅资产
        asset_unsubscribe_request = {
            "id": 7,
            "method": "asset.unsubscribe",
            "params": []
        }
        await websocket.send(json.dumps(asset_unsubscribe_request))
        asset_unsubscribe_response = await websocket.recv()
        print("资产取消订阅响应:", asset_unsubscribe_response)

# 运行 WebSocket 客户端
asyncio.run(connect_to_websocket())
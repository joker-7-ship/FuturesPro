import asyncio
import websockets
import json
import ssl
import hashlib
from common.config import API_KEY, SECRET_KEY, WSS_URL

def calculate_sign(secret_key):
    return hashlib.sha256(secret_key.encode()).hexdigest()
async def subscribe_and_receive(websocket, subscribe_request, message_type):
    await websocket.send(json.dumps(subscribe_request))
    subscribe_response = await websocket.recv()
    print(f"{message_type} 订阅响应:", subscribe_response)
    while True:
        try:
            message = await websocket.recv()
            message_data = json.loads(message)
            if "method" in message_data:
                method = message_data["method"]
                if method == "kline.update":
                    print("K线推送消息:", json.dumps(message_data, ensure_ascii=False))
                elif method == "depth.update":
                    print("深度推送消息:", json.dumps(message_data,  ensure_ascii=False))
                elif method == "deals.update":
                    print("成交推送消息:", json.dumps(message_data, ensure_ascii=False))
                elif method == "state.update":
                    print("市场状态推送消息:", json.dumps(message_data,  ensure_ascii=False))
                elif method == "order.update":
                    print("订单推送消息:", json.dumps(message_data,  ensure_ascii=False))
                elif method == "asset.update":
                    print("资产推送消息:", json.dumps(message_data,  ensure_ascii=False))
                else:
                    print("未知消息类型:", json.dumps(message_data,  ensure_ascii=False))
        except websockets.ConnectionClosed:
            print(f"{message_type} 推送已关闭")
            break
        except Exception as e:
            print(f"{message_type} 推送发生错误: {e}")
            break
async def connect_to_websocket():
    url = WSS_URL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with websockets.connect(url, ssl=ssl_context, compression='deflate') as websocket:
        # 鉴权请求
        sign_data = calculate_sign(SECRET_KEY)
        auth_request = {
            "method": "server.accessid_auth",
            "params": [API_KEY, sign_data],
            "id": 1
        }
        await websocket.send(json.dumps(auth_request))
        auth_response = await websocket.recv()
        print("鉴权响应:", auth_response)
        # 检查鉴权是否成功
        if "auth fail" in json.loads(auth_response):
            print("鉴权失败，退出连接")
            return
        # K线推送
        kline_subscribe_request = {
            "method": "kline.subscribe",
            "params": ["BTCUSDT", 1],
            "id": 2
        }
        asyncio.create_task(subscribe_and_receive(websocket, kline_subscribe_request, "K线"))
        # 深度推送
        depth_subscribe_request = {
            "method": "depth.subscribe",
            "params": ["BTCUSDT", 5, "0.01"],
            "id": 4
        }
        asyncio.create_task(subscribe_and_receive(websocket, depth_subscribe_request, "深度"))
        # 市场状态推送
        state_subscribe_request = {
            "method": "state.subscribe",
            "params": ["BTCUSDT", 86400],
            "id": 5
        }
        asyncio.create_task(subscribe_and_receive(websocket, state_subscribe_request, "市场状态"))
        # 成交推送
        deals_subscribe_request = {
            "method": "deals.subscribe",
            "params": ["BTCUSDT", "ETHUSDT"],
            "id": 6
        }
        asyncio.create_task(subscribe_and_receive(websocket, deals_subscribe_request, "成交"))
        # 订单推送
        order_subscribe_request = {
            "method": "order.subscribe",
            "params": [],
            "id": 7
        }
        asyncio.create_task(subscribe_and_receive(websocket, order_subscribe_request, "订单"))
        # 资产推送
        asset_subscribe_request = {
            "method": "asset.subscribe",
            "params": [],
            "id": 8
        }
        asyncio.create_task(subscribe_and_receive(websocket, asset_subscribe_request, "资产"))
        await asyncio.Future()
if __name__ == "__main__":
    asyncio.run(connect_to_websocket())
History = [{
        "business": 50,
        "offset": 0.001,
        "limit": 100 # 加注释
    },
{
        "asset": "BTCUSDT",
        "business": "trade",
        "start_time": 0.001,
        "end_time": 0.001,
        "offset": 0,
        "limit": 100 # 加注释
    }
]

market_preference= [{
        "market":"BTCUSDT",
        "side": 1
},
{
        "market":"ETHUSDT",
        "side": 0
}
]

AdjustMargin=[{
        "market":"BTCUSDT",
        "type": 1,
        "amount": "100",
        "side": 1,
}
]

AdjustLeverage=[{
        "market": "BTCUSDT",
        "position_type": 1, #仓位类型 1 逐仓 2 全仓
        "side": 1,
        "leverage": 10,
}
]
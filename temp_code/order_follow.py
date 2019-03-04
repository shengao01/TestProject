import base64
import hmac
import requests
import websocket
import json
import zlib
import dateutil.parser as dp
from app.following_orders import *
from jsonpath import jsonpath


def get_server_time():
    url = "http://www.okex.com/api/general/v3/time"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['iso']
    else:
        return ""

def server_timestamp():
    server_time = get_server_time()
    parsed_t = dp.parse(server_time)
    timestamp = parsed_t.timestamp()
    return timestamp

# get mysign
def login_params(timestamp, api_key, passphrase, secret_key):
    message = timestamp + 'GET' + '/users/self/verify'
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    sign = base64.b64encode(d)
    login_param = {"op": "login", "args": [api_key, passphrase, timestamp, sign.decode("utf-8")]}
    return login_param

# unzip
def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated.decode()

def on_open(self):
    # login
    print("程序启动")
    timestamp = str(server_timestamp())
    # login_str = login_params(str(timestamp), eval(f"api_key{i}"), eval(f"passphrase{i}"), eval(f"secret_key{i}"))
    # print(login_str)
    # # subscrbe future trades for self
    # self.send(json.dumps(login_str))
    login_str = login_params(str(timestamp), api_key0, passphrase0, secret_key0)
    # subscrbe future trades for self
    self.send(json.dumps(login_str))

    time.sleep(0.2)
    sub_param = {"op": "subscribe", "args": ["futures/order:ETH-USD-190329"]}
    # sub_param = {"op": "subscribe", "args": ["futures/order:ETH-USD-190329", "futures/position:ETH-USD-190329"]}
    sub_str = json.dumps(sub_param)
    self.send(sub_str)


def on_message(self, evt):
    data = inflate(evt)  # data decompress
    data = json.loads(data)
    # print(data)


    if data.get("table") == "futures/order":
        if data["data"][0]["status"] == "2":
            orders_data = {}
            print("enter")
            leverage = data["data"][0]["leverage"]
            instrument_id = data["data"][0]["instrument_id"]
            orders_data["price"] = float(data["data"][0]["price"])
            # 订单类型(1:开多 2:开空 3:平多 4:平空)
            orders_data["type"] = data["data"][0]["type"]
            # 张数
            orders_data["size"] = data["data"][0]["size"]
            print(orders_data)

            # 跟单 开仓
            if orders_data["type"] == "1" or orders_data["type"] == "2":
                follow_result = FutureAPI.take_orders(instrument_id, [orders_data], leverage)
                print(follow_result)
                result = FutureAPI.get_specific_position(instrument_id)
                # 下单id
                order_ids = jsonpath(follow_result,"$..order")

                cancel_time = time.time() + 30
                # 没有持仓量
                while not result["holding"]:
                    time.sleep(2)
                    result = FutureAPI.get_specific_position(instrument_id)
                    # 30秒未成交 撤单
                    if cancel_time >= time.time():
                        print(FutureAPI.revoke_orders(instrument_id,order_ids))
                        break


            # 跟单 平仓
            if orders_data["type"] == "3" or orders_data["type"] == "4":
                result = FutureAPI.get_specific_position(instrument_id)
                print(result)
                # 有持仓量
                if result["holding"]:
                    if result["holding"][0]["long_qty"] != 0 or result["holding"][0]["short_qty"] != 0:
                        # 平多 获取多仓数量
                        orders_data["size"] = result["holding"][0]["long_qty"] if orders_data["type"] == "3" else result["holding"][0]["short_qty"]
                        # 下单 平仓
                        print(FutureAPI.take_orders(instrument_id, [orders_data], leverage))
                #  查持仓量
                while result["holding"]:
                    alarm_time = time.time() + 30
                    try:
                        result = FutureAPI.get_specific_position(instrument_id)
                        time.sleep(2)
                        if time.time() >= alarm_time:
                            print(f"{instrument_id}超时未平仓")
                            alarm_time += 60
                    except Exception as e:
                        print(e)

    # if data.get("table") == "futures/position":
    #     info = data["data"][0]
    #     if info:
    #         pass

    if data.get("event") == "error":
        print("订阅的频道已过期")
        ws.close()


def on_error(self, evt):
    print(evt)


def on_close(self):
    print('DISCONNECT')


if __name__ == "__main__":
    while True:
        # 手工交易账户 followed
        follower = create_app("order_following")
        url = follower.v3_url
        api_key0 = follower.api_key
        secret_key0 = follower.seceret_key
        passphrase0 = follower.passphrase

        # follower
        app = create_app("order_following")
        FutureAPI = app.FutureAPI()

        # websocket.enableTrace(True)
        websocket.enableTrace(False)
        if len(sys.argv) < 2:
            host = url
        else:
            host = sys.argv[1]
        ws = websocket.WebSocketApp(host,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close,
                                    )
        ws.on_open = on_open
        # ping
        ws.run_forever(ping_interval=10,ping_timeout=5)

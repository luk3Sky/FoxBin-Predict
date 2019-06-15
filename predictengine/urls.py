"""predictengine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

print("Data fetch begins...")
import websocket
from websocket import create_connection
import time, csv, json 

COUNT = 5000

data = {}
fh = open("train_data.csv", "w")

def on_open(ws):

    old_req = {
        'ticks_history': 'R_100',
        'end': 'latest',
        'start': 1,
        'style': 'ticks',
        'adjust_start_time': 1,
        'count': COUNT
    }

    req = {
        'ticks_history': 'R_100',
        'end': 'latest',
        'start': 1,
        'style': 'ticks',
        'subscribe': 1,
        'adjust_start_time': 1,
        'count': COUNT
    }

    json_data = json.dumps(req)
    ws.send(json_data)

def on_message(ws, message):
    y = json.loads(message)
    if (y['msg_type'] == "history"):
        prices = y['history']['prices']        
        times = y['history']['times']
        with open('train_data.csv', mode='w', newline='') as data_file:
            data_writer = csv.writer(data_file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
            data_writer.writerow(['date_time', 'price_value', 'trading_state'])
            for i in range(len(prices)):
                price_i = float(prices[i])
                time_i = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(int(times[i])))
                state_i = {True: "rise", False: "fall"} [price_i <= float(prices[i+5])]
                data[time_i] = price_i
                data_writer.writerow([time_i, price_i, state_i])
        # ws.close()
    elif(y['msg_type'] == "tick"):
        # print(data)
        print("done")
        # tick : {ask, bid, quote, epoch}
        # quote_i = y['tick']['bid']
        # epoch_i = y['tick']['epoch']
        # print(quote_i, epoch_i)
        ws.close()


apiUrl = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
ws = websocket.WebSocketApp(apiUrl, on_message = on_message, on_open = on_open)
ws.run_forever()

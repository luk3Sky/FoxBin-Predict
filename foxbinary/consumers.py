import asyncio
import pandas as pd
import tensorflow as tf
import numpy as np
import keras
from keras.models import load_model
import json
import os
import subprocess
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer

# we need to redefine our metric function in order 
# to use it when loading the model 
# def auc(y_true, y_pred):
#     auc = tf.metrics.auc(y_true, y_pred)[1]
#     keras.backend.get_session().run(tf.local_variables_initializer())
#     return auc

class BinaryConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
    	print("connected", event)
    	await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("recieved", event)
        text_key = event.get('text', None)
        print (text_key)
        if text_key is not None:
            payload = json.loads(text_key)
            # Part 3 - Making the predictions and visualising the results
            if payload['test'] == 'Prediction':
                print("true")
                predicted_result = predict()
                print(predicted_result)
                result = [1, 2, 4]
                await self.send({
                    "type": "websocket.send",
                    "array": predicted_result,
                })
        await self.send({
            "type": "websocket.send",
            "text": "recieved tick value",
           # "array": array
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

def predict():
    regressor = load_model(filepath=os.getcwd()+'\\foxbinary\model.h5', compile=False, custom_objects=None)
    # Getting the real stock price 
    dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
    real_stock_price = dataset_test.iloc[:, 1:2].values

    # Getting the predicted stock price 
    dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
    training_set = dataset_train.iloc[:, 1:2].values
    dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, 1000):
        X_test.append(inputs[i-60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    # adding the bias to the array
    predicted_stock_price = np.array(predicted_stock_price)
    predicted_stock_price = predicted_stock_price + 0.00016

    # Visualising the results
    # TODO:  get a numerical value for the accuracy
    # plt.plot(real_stock_price, color = 'red', label = 'Real Stock Price')
    # plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted  Stock Price')
    # plt.title(' Stock Price Prediction')
    # plt.xlabel('Time')
    # plt.ylabel(' Stock Price')
    # plt.legend()
    # plt.show()
    return predicted_stock_price
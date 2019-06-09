    
var WebSocket = require('websocket').w3cwebsocket;
let ws = new WebSocket('ws://localhost:8000/ml/');
      
    ws.onopen = (evt) => {
        console.log('Open');
        ws.send(JSON.stringify({test: "Prediction"}));
    }
    ws.onmessage = (msg) => {
        console.log('Message', msg);
    }
    ws.onerror = (error) => {
        console.log('Error', error);
    }
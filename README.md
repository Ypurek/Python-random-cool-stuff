# Python random cool stuff

project to keep different useful scripts on Python for QA activities also cool findings and other stuff check out also
my
| blog             | http://qamania.org/               |
|------------------|-----------------------------------|
| telegram channel | https://t.me/qamania              |
| youtube channel  | https://www.youtube.com/c/QAMania |

## Table of content
- [Websocket Server](#Websocket Server)
- [Launching playwright browsers concurrently](#Launching playwright browsers concurrently)

## Websocket Server
[websocketServer.py](websocketServer.py)  
Obviously, when I do testing with HTTP services, I can use Postman, SoapUI, curl or any other HTTP client. 
Meanwhile, I was wondering what tools I can use to work with web sockets. 
So I've found some, like [Websocket King](https://chrome.google.com/webstore/detail/websocket-king-client/cbcbkhdmedgianpaifchdaddpnmgnknn)
and decided to try it out.
Used sample from [here](https://medium.com/nuances-of-programming/как-создавать-веб-сокеты-в-python-1bc572045827)
and created simple web socket server

### Preconditions
- Python 3.8+
- 	`pip install websockets`
- free local port 4000 (set in the code)

### Description
after start server on **ws://localhost:4000**, client can connect and send text message, which will be resent to all connected clients  
also once per 10 sec server will send message to all clients  
also server will not resend messages with **ignore** word  
This is done to show there is no classic request/response sequence with websockets



## Launching playwright browsers concurrently
[async_browsers_playwright.py](async_browsers_playwright.py)    

### ref
- [playwright repo](https://github.com/microsoft/playwright-python)
- [playwright website](https://playwright.dev/)

### Preconditions
- Python 3.8+
- `pip install playwright`
- `python -m playwright install`

### Description
The code launches 10 instances of Chromium concurrently and make them to run simple "tests" in random order. Just for fun 
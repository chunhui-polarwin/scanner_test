import configparser
import socket     #导入socket模块
from fastapi import FastAPI, Request, Response, Body	
import uvicorn as u
import time
import json
import requests
import httpx
app = FastAPI(debug=True)	


def crossDomainResponse(data):
    response = Response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

def _format(result):
    if str(result).startswith('0x'):
        result = str(result)[2:-1]
    return result

@app.get(path = "/getdeviceid",summary='读取闸机扫描到的rfid')
async def getdeviceids(step:int = 10):
    s = socket.socket()						#创建套接字
    global host					            #IP
    global port								#端口
    global storeId
    s.connect((host,int(port)))				#主动初始化TCP服务器连接
    s.settimeout(step)
    res = []
    end_time = time.time() + step
    #print(time.time(),end_time)
    while end_time > time.time():
        try:
            #发送开始扫描的指令
            s.send(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            recvData = s.recv(1024)
            print(recvData)
            EPC = recvData[7:-5]
            result = hex(int.from_bytes(EPC, byteorder='big',signed=False))
            #print(sys.byteorder)
            if result in res:
                pass
            else:
                print(result)
                res.append(result)
        except Exception as e:
            #输出超时信息
            print(e)
         
    #关闭套接字
    s.close()
    res = [_format(i) for i in res]
    res_data = {
        "dataList":res,
        "storeId":int(storeId),
    }
    return {"code": 200, "data": res_data,"msg": '请求成功'}

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./conf.ini')
    url = config['web']['url']
    host = config['door']['ip']
    port = config['door']['port']
    storeId = config["door"]['storeid']
    u.run(app, host="0.0.0.0", port=8008)
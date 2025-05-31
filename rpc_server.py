import socket
import os
import math
import json

class connectSocket:
    # ソケット作成から接続要求まで
    def __init__(self):
        self.server_address = '/tmp/socket_file'
        self.sock = None

    def init(self):
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass
        
        print('Starting up on {}'.format(self.server_address))

        self.sock.bind(self.server_address)
        self.sock.listen(1)

        return self.sock



# 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
def floor(x: float) -> int:
    return math.floor(x)

# 方程式 r^n = x における、r の値を計算する。
def nroot(n: int, x: int):
    return x ** (1/n)

# 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
def reverse(s: str):
    if s.__len__() == 0:
        return ""
    else:
        return s[s.__len__()-1] + reverse(s[0:s.__len__()-1]) 

# 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
def validAnagram(s1:str,s2:str):
    s1 = s1.lower().replace(" ","")
    s2 = s2.lower().replace(" ","")
    if len(s1) != len(s2):
        return False
    
    s1Counter = {}
    s2Counter = {}

    for i in range(len(s1)):
        s1Counter[s1[i]] =  1 + s1Counter.get(s1[i],0) 
        s2Counter[s2[i]] =  1 + s2Counter.get(s2[i],0) 
        
    return s1Counter == s2Counter

def sort_strings(string_list : list[str]) -> list[str]:
    if not isinstance(string_list,list) or not all(isinstance(item,str) for item in string_list):
        raise ValueError("リスト内のすべての要素は文字列である必要があります。")
    
    # アルファベット順にソート
    sorted_list = sorted(string_list)
    return sorted_list

functions = {
    "floor" : floor,
    "nroot" : nroot,
    "reverse" : reverse,
    "validAnagram" : validAnagram,
    "sort" : sort_strings,
}

def main():
    server = connectSocket()
    sock = server.init()

    while True:
        connection,client_address = sock.accept()
        try:
            print('connection from',client_address)

            while True:
                data = connection.recv(1024).decode('utf-8')
                request_data = json.loads(data)

                method_name = request_data.get("method_name")
                arguments = request_data.get("arguments")
                param_type = request_data.get("param_type")
                request_id = request_data.get("id")

                if method_name in functions:
                    target_function = functions[method_name]
                    if method_name == "sort":
                        result = target_function(arguments)
                    else:
                        if isinstance(arguments,list):
                            result = target_function(*arguments)
                        else:
                            result = target_function(arguments)
                    responce = {
                        "results" : result,
                        "result_type": str(type(result).__name__),
                        "id":request_id
                    }
                else:
                    responce = {
                        "error": "Method not found",
                        "id":request_id
                    }
                connection.send(json.dumps(responce).encode('utf-8'))
                
        finally:
            print("Closing current connection")
            connection.close()

if __name__ == "__main__":
    main()

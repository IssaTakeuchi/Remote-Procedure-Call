import socket
import os
import math

class connectSocket:
    # ソケット作成から接続要求まで
    def init():
        sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

        server_address = '/tmp/socket_file'

        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass
        
        print('Starting up on {}'.format(server_address))

        sock.bind(server_address)
        sock.listen(1)

function_map = {
    "floor" : floor,
    "nroot" : nroot,
    "reverse" : reverse,
    "validAnagram" : validAnagram,
    "sort" : sort,
}

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




def main():
    connectSocket.init()

if __name__ == "__main__":
    main()

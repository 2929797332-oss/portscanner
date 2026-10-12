import socket
import sys

if len(sys.argv)<4:
    print("用法：python3 scan.py 需扫描的ip 端口范围1 端口范围2")
    print("如需只扫描一个端口就填同一个数")
    print("空格不能省略！！！")
    sys.exit(1)

try:
    start = int(sys.argv[2])
    end = int(sys.argv[3])
except ValueError:
    print("端口号必须是数字")
    sys.exit(1)  

target = sys.argv[1]

for port in range(start, end + 1):
    s = socket.socket()
    s.settimeout(2)
    result = s.connect_ex((target,port))
    if result == 0:
        print(f"{port} 开放")
    s.close()

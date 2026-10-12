import socket
import sys

if len(sys.argv)<2:
    print("用法：python3 scan.py 需扫描的ip") 
    sys.exit(1)

target = sys.argv[1]


for port in range(1, 1024):
    s = socket.socket()
    s.settimeout(2)
    result = s.connect_ex((target,port))
    if result == 0:
        print(f"{port} 开放")
    s.close()

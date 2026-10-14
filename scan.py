import socket
import sys

CLOSED_CODES  = {111, 10061}
TIMEOUT_CODES = {110, 10035}

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

def scan_port(target, port):
    """
    扫描单个端口
    返回字典{"port": 端口/int, "status": 状态/str, "code": 错误码/int}
    """

    s = socket.socket()
    s.settimeout(2)
    result = s.connect_ex((target, port))
    s.close()  # 必须关 —— 否则扫大量端口会耗尽资源

    if result == 0:
        status = "open"
    # Windows 的返回码和 Linux 不同，所以两组都收
    elif result in CLOSED_CODES:
        status = "closed"
    elif result in TIMEOUT_CODES:
        status = "timeout"
    else:
        status = "other"
    return {"port": port, "status": status, "code": result}


def scan_ports(target, ports):
    """
    扫描一批端口，按状态分类返回。
    ports: 任何可遍历的端口集合(range / list 都行）
    """
    buckets = {
        "open": [],
        "closed": [],
        "timeout": [],
    }

    for port in ports:
        r = scan_port(target, port)
        if r["status"] in buckets:
            buckets[r["status"]].append(r["port"])

    buckets["target"] = target
    buckets["ports"]  = list(ports)
    return buckets
        
if __name__ == '__main__':
    a = scan_ports("192.168.75.128", range(1, 101))
    print("开放：", a["open"])
    print("关闭数：", len(a["closed"]))
    print("超时数：", len(a["timeout"]))
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
source_ip = s.getsockname()[0]

ip_destino = 0x0FE4BF6D
print(type(ip_destino))
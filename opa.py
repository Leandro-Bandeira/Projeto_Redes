import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

source_ip = s.getsockname()[0]

ip_origem_str = source_ip
#transformando o octeto em bytes################################################3
octets = ip_origem_str.split('.')
# Inicialize uma lista para armazenar os bytes
bytes_list = []
# Converta cada octeto em sua representação binária de 8 bits e adicione à lista
for octet in octets:
    # Converta o octeto em inteiro
    octet_int = int(octet)
    # Converta o inteiro em um numero binário
    octet_binary = octet_int.to_bytes(1, byteorder='big')
    bytes_list.append(octet_binary)


###############################################
ip_origem_str = bytes_list[0] + bytes_list[1] + bytes_list[2] + bytes_list[3]
print(type(ip_origem_str))
ip_origem = int.from_bytes(ip_origem_str, byteorder='big')
import socket
import sys
import struct


class Client_raw:

    def __init__(self):
        try:
            # Cria um socket raw para o protocolo UDP
            self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        except socket.error as e:
            print('Erro ao criar socket: {}'.format(e))
            sys.exit()

    def send_request(self):
        # Define os detalhes do pacote UDP
        
        source_ip = self.s.getsockname()[0] #'127.0.0.1'
        dest_ip = '15.228.191.109'
        source_port = 59155
        dest_port = 50000
        data = b'Hello, UDP!'

        # Monta o cabeçalho UDP
        udp_header = struct.pack('!HHHH', source_port, dest_port, len(data) + 8, 0)  # Cabeçalho UDP: Origem Porta, Destino Porta, Comprimento, Checksum
        packet = udp_header + data

        # Envia o pacote UDP
        try:
            self.s.sendto(packet, (dest_ip, dest_port))
            print('Pacote UDP enviado com sucesso')
        except socket.error as e:
            print('Erro ao enviar pacote UDP: {}'.format(e))
            sys.exit()

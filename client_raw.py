import socket
import sys
import struct
import random

class Client_raw:

    def __init__(self):
        try:
            # Cria um socket raw para o protocolo UDP
            self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        except socket.error as e:
            print('Erro ao criar socket: {}'.format(e))
            sys.exit()

    def send_request(self, type):
        # Define os detalhes do pacote UDP
        
        source_ip = self.s.getsockname()[0] #pega o IP da máquina que está rodando para atribuir como origem 
        dest_ip = '15.228.191.109'  #IP do servidor 
        source_port = 59155     #porta da máquina 
        dest_port = 50000       #porta do servidor

        req = b'0000'      #esse é os primeiros 4 bits, que o valor especificado indica que é uma requisição 
        tipo = None
        if type == 1: 
            tipo = b'0000'
        elif type == 2:
            tipo = b'0001'
        elif type == 3:
            tipo = b'0010'

        identificador = random.randint(1, 65535)  #sorteando o numero que servirá como identificador
        identificador = format(identificador, '016b') #converte o número para sua representação binária e garante que haja pelo menos 16 dígitos na representação

        mensagem = req + tipo + identificador   #concatenando o conjunto de 4bits, 4bits e 16 bits

        # Monta o cabeçalho UDP
        comprimento_segmento = 11
        checksum = 0
        udp_header = struct.pack('!HHHH', source_port, dest_port, comprimento_segmento, checksum) 
        #!HHHH significa que o formato será big-endian e cada H significa um inteiro de 2 bytes (totalizando 8 bytes de cabeçalho)
        #os 4 H's são definidos logo em seguida: souce_port, dest 

        packet = udp_header + mensagem  #definindo o pacote com o cabeçalho e a mensagem de requisição para o servidor 

        # Envia o pacote UDP
        try:
            self.s.sendto(packet, (dest_ip, dest_port))
            print('Pacote UDP enviado com sucesso')
        except socket.error as e:
            print('Erro ao enviar pacote UDP: {}'.format(e))
            sys.exit()

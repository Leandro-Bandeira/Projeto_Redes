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
        identificador = identificador.to_bytes(2, byteorder='big') #converte o número para sua representação binária em bigendian

        mensagem = req + tipo + identificador #concatenando o conjunto de 4bits, 4bits e 16 bits

        #Pseudo cabeçalho IP 
        ip_origem = b'0xC0A80169'
        ip_destino = b'0x0FE4BF6D'
        n_protocolo = b'0x0011'
        comprimento_seg_udp = b'0x000B'


        # Cabeçalho UDP
        comprimento_segmento = 11
        checksum = 0
        
        # Calculando o checksum
        int_origin_ip = int(ip_origem, 16)
        int_dest_ip = int(ip_destino, 16)
        int_protocol = int(n_protocolo, 16)
        int_udp_length = int(comprimento_seg_udp, 16)
        int_source_port = source_port
        int_dest_port = dest_port
        int_length = comprimento_segmento
        int_checksum = checksum
        int_payload_h = (mensagem >> 8) & 0xFFFF
        int_payload_l = (mensagem << 8) & 0xFFFF

        
        sum = int_origin_ip + int_dest_ip + int_protocol + int_udp_length + int_source_port + int_dest_port + int_length + int_checksum + int_payload_h + int_payload_l
        sum_l = sum & 0xFFFF
        sum_h = (sum >> 16) & 0xFFFF
        sum_f = sum_h+sum_l
        checksum = ~sum_f & 0xFFFF
        
        #!HHHH significa que o formato será big-endian e cada H significa um inteiro de 2 bytes (totalizando 8 bytes de cabeçalho)
        #os 4 H's são definidos logo em seguida: souce_port, dest_port, comprimento, checksum 
        udp_header = struct.pack('!HHHH', source_port, dest_port, comprimento_segmento, checksum)  #junta todos os elementos do cabeçalho UDP
        udp_header = struct.pack('!HHHH', source_port, dest_port, comprimento_segmento, checksum)  #junta todos os elementos do cabeçalho UDP
        

        packet = udp_header + mensagem  #definindo o pacote com o cabeçalho e a mensagem de requisição para o servidor 

        # Envia o pacote UDP
        try:
            self.s.sendto(packet, (dest_ip, dest_port)) #enviando o pacote para o servidor
            print('Pacote UDP enviado com sucesso')
        except socket.error as e:
            print('Erro ao enviar pacote UDP: {}'.format(e))
            sys.exit()

        data, addr = self.s.recvfrom(1024)   #recebendo resposta do servidor 

        #print(data)

        # para cada valor inteiro, transforma-o em ascii a partir do primeiro byte (onde a msg começa) depois de retirar os 32 bytes (cabeçalho fake, cabecalho real e os 4 bytes da outra parte) 
        # até o final
        if type != 3:   #se for uma mensagem (tipo string)
            msg_rcv = str(data[28:-1].decode("ascii")).rstrip()
        
        else:           #se for a qtd de mensagens enviadas(tipo int)         
            msg_rcv = int.from_bytes((data[4:]), "big")
            
        print(msg_rcv)


import socket
import sys
import struct
import random
import netifaces as ni

class Client_raw:

    def __init__(self):
        try:
            # Cria um socket raw para o protocolo UDP
            self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        except socket.error as e:
            print('Erro ao criar socket: {}'.format(e))
            sys.exit()

    def send_request(self, type):
    
        # obtém o endereço IP associado à interface de rede padrão
        default_interface = ni.gateways()['default'][ni.AF_INET][1]
        source_ip = ni.ifaddresses(default_interface)[ni.AF_INET][0]['addr']
        
        dest_ip = '15.228.191.109'  #IP do servidor 
        source_port = 59155     #porta da máquina 
        dest_port = 50000       #porta do servidor

        type_request = None
        if type == 1: 
            type_request = b'\x00' 
        elif type == 2:
            type_request = b'\x01' 
        elif type == 3:
            type_request = b'\x02' 

        identificador = random.randint(1, 65535)  #sorteando o numero que servirá como identificador
        identificador = identificador.to_bytes(2, byteorder='big') #converte o número para sua representação binária em bigendian

        
        mensagem = type_request + identificador #concatenando o conjunto de 4bits, 4bits e 16 bits
        
        mensagem_int = int.from_bytes(mensagem, byteorder='big')
        
        #Pseudo cabeçalho IP

        #transformando o octeto em bytes################################################3
        octets = source_ip.split('.')
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

        
        ip_origem_by = bytes_list[0] + bytes_list[1] + bytes_list[2] + bytes_list[3]
        ip_origem = int.from_bytes(ip_origem_by, byteorder='big')
        ip_destino = 0x0FE4BF6D
        n_protocolo = 0x0011
        comprimento_seg_udp = 0x000B
        
        pseud_header = ip_origem.to_bytes(4, byteorder='big')  + ip_destino.to_bytes(4, byteorder='big') + n_protocolo.to_bytes(2, byteorder='big')  + comprimento_seg_udp.to_bytes(2, byteorder='big') 

        # Cabeçalho UDP
        #comprimento_segmento_b = b'0000000000001011'
        comprimento_segmento = 11
        checksum = 0
        
        # Calculando o checksum
        int_origin_ip_h = (ip_origem >> 16) & 0xFFFF
        int_origin_ip_l = ip_origem & 0xFFFF
        int_dest_ip_h = (ip_destino >> 16) & 0xFFFF
        int_dest_ip_l = ip_destino & 0xFFFF
        int_protocol = n_protocolo
        int_udp_length = comprimento_seg_udp
        int_source_port = source_port
        int_dest_port = dest_port
        int_length = comprimento_segmento
        int_checksum = checksum
        int_payload_h = (mensagem_int >> 8) & 0xFFFF
        int_payload_l = (mensagem_int << 8) & 0xFFFF


        sum = int_origin_ip_h + int_origin_ip_l + int_dest_ip_h + int_dest_ip_l + int_protocol + int_udp_length + int_source_port + int_dest_port + int_length + int_checksum + int_payload_h + int_payload_l
        sum_l = sum & 0xFFFF
        sum_h = (sum >> 16) & 0xFFFF
        sum_f = sum_h+sum_l
        checksum = ~sum_f & 0xFFFF
        #checksum = 0
        
        #!HHHH significa que o formato será big-endian e cada H significa um inteiro de 2 bytes (totalizando 8 bytes de cabeçalho)
        #os 4 H's são definidos logo em seguida: souce_port, dest_port, comprimento, checksum 
        udp_header = struct.pack('!HHHH', source_port, dest_port, comprimento_segmento, checksum)  #junta todos os elementos do cabeçalho UDP        


        packet = udp_header + mensagem  #definindo o pacote com o cabeçalho e a mensagem de requisição para o servidor 
        # Envia o pacote UDP
        try:
            self.s.sendto(packet, (dest_ip, dest_port)) #enviando o pacote para o servidor
        except socket.error as e:
            print('Erro ao enviar pacote UDP: {}'.format(e))
            sys.exit()

        data = None
        data, addr = self.s.recvfrom(1024)   #recebendo resposta do servidor 

        # para cada valor inteiro, transforma-o em ascii a partir do primeiro byte (onde a msg começa) depois de retirar os 32 bytes (cabeçalho fake, cabecalho real e os 4 bytes da outra parte) 
        # até o final
        if type != 3:   #se for uma mensagem (tipo string)
            msg_rcv = str(data[32:-1].decode("ascii")).rstrip()
        
        else:           #se for a qtd de mensagens enviadas(tipo int)         
            msg_rcv = int.from_bytes((data[32:]), "big")
            
        print(msg_rcv)


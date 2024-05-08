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
        source_ip = ni.ifaddresses(default_interface)[ni.AF_INET][0]['addr'] #armazena o IP da máquina em que o código está rodando 
        
        dest_ip = '15.228.191.109'  #IP do servidor 
        source_port = 59155     #porta da máquina 
        dest_port = 50000       #porta do servidor

        type_request = None    #essa variável possuirá já os 8 bytes (req + tipo)
        if type == 1: 
            type_request = b'\x00' # 00000000 (0x00)- Data e hora
        elif type == 2:
            type_request = b'\x01' # 00000001 (0x01)- Mensagem motivadora
        elif type == 3:
            type_request = b'\x02' # 00000000 (0x02)- Quantidade de mensagens enviadas pelo servidor

        identificador = random.randint(1, 65535)  #sorteando o numero que servirá como identificador
        identificador = identificador.to_bytes(2, byteorder='big') #converte o número para sua representação binária em bigendian
        mensagem = type_request + identificador #concatenando o conjunto de 8bits e 16 bits
        mensagem_int = int.from_bytes(mensagem, byteorder='big')
        
        ###################################Pseudo cabeçalho IP
        octets = source_ip.split('.')  #separa a string do ip em octetos (representados por string)
        bytes_list = []

        #esse laço transforma cada octeto em byte
        for octet in octets:
            octet_int = int(octet) #converte um octeto em inteiro
            octet_binary = octet_int.to_bytes(1, byteorder='big') #converte o inteiro em um numero binário
            bytes_list.append(octet_binary)
        
        ip_origem_by = bytes_list[0] + bytes_list[1] + bytes_list[2] + bytes_list[3]  #concatena os bytes
        ip_origem = int.from_bytes(ip_origem_by, byteorder='big')  #transforma o ip em inteiro para fazer as operacoes do checksum
        
        ip_destino = 0x0FE4BF6D  #ip do serbidor em inteiro 
        n_protocolo = 0x0011     #numero de protocolo
        comprimento_seg_udp = 0x000B
        ############################################################3 

        ########## parte do cabeçalho UDP
        comprimento_segmento = 11
        checksum = 0
        ################################
        
        # Calculando o checksum
        #todas as variaveis sao convertidas para inteiros para que seja possivel fazer as operacoes de soma
        int_origin_ip_h = (ip_origem >> 16) & 0xFFFF    #pega os 16 bits mais significativos do ip de origem
        int_origin_ip_l = ip_origem & 0xFFFF            #pega os 16 bits menos significativos do ip de origem
        int_dest_ip_h = (ip_destino >> 16) & 0xFFFF     #pega os 16 bits mais significativos do ip de destino
        int_dest_ip_l = ip_destino & 0xFFFF             #pega os 16 bits menos significativos do ip de destino            
        int_payload_h = (mensagem_int >> 8) & 0xFFFF    #pega os 16 bits mais significativos da mensagem
        int_payload_l = (mensagem_int << 8) & 0xFFFF    #pega os 16 bits menos significativos da mensagem

        #soma de todos os inteiros para calcular o checksum
        sum = int_origin_ip_h + int_origin_ip_l + int_dest_ip_h + int_dest_ip_l + n_protocolo + comprimento_seg_udp + source_port + dest_port + comprimento_segmento + checksum + int_payload_h + int_payload_l
        sum_l = sum & 0xFFFF #pega os 16 bits menos significativos da soma
        sum_h = (sum >> 16) & 0xFFFF #pega os 16 bits mais significativos da soma
        sum_f = sum_h+sum_l #soma os 16 bits mais e menos significativos para realizar wrap around
        checksum = ~sum_f & 0xFFFF  #realiza o complemento de 1 e pega os 16 bits menos significativos para o checksum
        
        #!HHHH significa que o formato será big-endian e cada H significa um inteiro de 2 bytes (totalizando 8 bytes de cabeçalho)
        #os 4 H's são definidos logo em seguida: souce_port, dest_port, comprimento, checksum 
        udp_header = struct.pack('!HHHH', source_port, dest_port, comprimento_segmento, checksum)  #junta todos os elementos do cabeçalho UDP        
        packet = udp_header + mensagem  #definindo o pacote com o cabeçalho udp e a mensagem de requisição para o servidor 

        
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
            
        print(msg_rcv)  #printando a mensagem recebida pelo servidor


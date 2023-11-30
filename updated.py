
import socket
import struct
import textwrap
from typing import Sequence
# from colorama import Fore, Back, Style
import argparse
import os

# initializing parser
parser = argparse.ArgumentParser()

# adding options
parser.add_argument("-v", "--verbose_level",
                    help="Verbose 1 shows basic info about the packets; Verbose 2 shows payload along with basic info")
parser.add_argument(
    "-o", "--output", help="Saves the Packets to the mentioned file")

# Reading args
args = parser.parse_args()

if args.verbose_level == 2:
    verbose_flag = 1
else:
    verbose_flag = 0

# Dictionary with all protocol and id's
protocol_ids = {1: 'ICMP', 2: 'IGMP', 3: 'GGP', 4: 'IP-in-IP', 5: 'ST', 6: 'TCP', 7: 'CBT', 8: 'EGP', 9: 'IGP', 10: 'BBN-RCC-MON', 11: 'NVP-II', 12: 'PUP', 13: 'ARGUS', 14: 'EMCON', 15: 'XNET', 16: 'CHAOS', 17: 'UDP', 18: 'MUX', 19: 'DCN-MEAS', 20: 'HMP', 21: 'PRM', 22: 'XNS-IDP', 23: 'TRUNK-1', 24: 'TRUNK-2', 25: 'LEAF-1', 26: 'LEAF-2', 27: 'RDP', 28: 'IRTP', 29: 'ISO-TP4', 30: 'NETBLT', 31: 'MFE-NSP', 32: 'MERIT-INP', 33: 'DCCP', 34: '3PC', 35: 'IDPR', 36: 'XTP', 37: 'DDP', 38: 'IDPR-CMTP', 39: 'TP++', 40: 'IL', 41: 'IPv6', 42: 'SDRP', 43: 'IPv6-Route', 44: 'IPv6Frag', 45: 'IDRP', 46: 'RSVP', 47: 'GRE', 48: 'DSR', 49: 'BNA', 50: 'ESP', 51: 'AH', 52: 'I-NLSP', 53: 'SwIPe', 54: 'NARP', 55: 'MOBILE', 56: 'TLSP', 57: 'SKIP', 58: 'IPv6-ICMP', 59: 'IPv6NoNxt', 60: 'IPv6-Opts', 61: 'Any', 62: 'CFTP', 63: 'Any', 64: 'SAT-EXPAK', 65: 'KRYPTOLAN', 66: 'RVD', 67: 'IPPC', 68: 'Any', 69: 'SAT-MON', 70: 'VISA', 71: 'IPCU', 72: 'CPNX', 73: 'CPHB', 74: 'WSN',
                75: 'PVP', 76: 'BR-SAT-MON', 77: 'SUN-ND', 78: 'WB-MON', 79: 'WB-EXPAK', 80: 'ISO-IP', 81: 'VMTP', 82: 'SECURE-VMTP', 83: 'VINES', 84: 'TTP', 84: 'IPTM', 85: 'NSFNET-IGP', 86: 'DGP', 87: 'TCF', 88: 'EIGRP', 89: 'OSPF', 90: 'Sprite-RPC', 91: 'LARP', 92: 'MTP', 93: 'AX.25', 94: 'OS', 95: 'MICP', 96: 'SCC-SP', 97: 'ETHERIP', 98: 'ENCAP', 99: 'Any', 100: 'GMTP', 101: 'IFMP', 102: 'PNNI', 103: 'PIM', 104: 'ARIS', 105: 'SCPS', 106: 'QNX', 107: 'A/N', 108: 'IPComp', 109: 'SNP', 110: 'Compaq-Peer', 111: 'IPX-in-IP', 112: 'VRRP', 113: 'PGM', 114: 'Any', 115: 'L2TP', 116: 'DDX', 117: 'IATP', 118: 'STP', 119: 'SRP', 120: 'UTI', 121: 'SMP', 122: 'SM', 123: 'PTP', 124: 'IS-IS', 125: 'FIRE', 126: 'CRTP', 127: 'CRUDP', 128: 'SSCOPMCE', 129: 'IPLT', 130: 'SPS', 131: 'PIPE', 132: 'SCTP', 133: 'FC', 134: 'RSVP-E2E-IGNORE', 135: 'Mobility', 136: 'UDPLite', 137: 'MPLS-in-IP', 138: 'manet', 139: 'HIP', 140: 'Shim6', 141: 'WESP', 142: 'ROHC', 1544: 'BROADCASTING/QoS'}

# Dictionary with all Target IP's and whois
whois_dict = {}

# pre-defined tabs
TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '

# main function


def main():

    
    # counter to notify no.of packets captured
    packet_counter = 0

    # creating an instance of socket
    connection = socket.socket(
        socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    # main loop which is used to display all the data we capture
    while True:
        # receiving data
        raw_data, source_address = connection.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)

        packet_counter = packet_counter + 1

        # printing the data
        #print('\033[1mETHERNET FRAMES CAPTURED: ' + str(packet_counter) + '\033[0m')

        print('ETHERNET FRAMES CAPTURED: '+ str(packet_counter)+'\n\n')

        print('Destination_MAC: ' + str(dest_mac) +'\n' + 'Source_MAC: ' + str(src_mac)+'\n')
        # print(('\tPROTOCOL:'+ str(eth_proto) + str(protocol_ids[eth_proto]) ))
        if eth_proto in protocol_ids:
            print('PROTOCOL:' + str(eth_proto) +
                  str(protocol_ids[eth_proto]))
        else:
            print('PROTOCOL:' + str(eth_proto) + ' (unknown)')

        if eth_proto == 8:
            (version, header_length, ttl, proto,
             src, target, data) = ipv4_packet(data)
            print('IPv4 Packet: ', end="")
            print(' Version: [{}] \n Header Length: [{}] \n TTL: [{}]\n'.format(
                version, header_length, ttl), end="")
            if target in whois_dict.keys():
                target_name = whois_dict[target]
            else:
                whois_cmd = "whois " + \
                    str(target) + " | " + "grep -i orgname" + \
                    " | " + "awk " + "'{" + "print " + "$2" + "}'"
                target_name = os.popen(whois_cmd).read()
                if len(str(target_name)) == 0:
                    whois_cmd = "whois " + str(target) + " | " + "grep -i netname" + " | " + \
                        "awk " + "'{" + "print " + "$2" + "}'" + \
                        "| awk '{if(NR==1) print $2}'"
                    target_name = os.popen(whois_cmd).read()
                compare = "Interneta"
                same_flag = 0
                if len(str(compare)) == len(str(target_name)):
                    same_flag = 0
                else:
                    same_flag = 1
                print("Same_Flag === " + str(same_flag)+'\n')
                if same_flag == 0:
                    target_name = " PRIVATE_ADDRESS"
                    target_name = target_name.replace("\n", "")
                    whois_dict[target] = target_name
                    target_name = whois_dict[target]
                else:
                    target_name = target_name.replace("\n", "")
                    whois_dict[target] = target_name
                    target_name = whois_dict[target]

            print(' Protocol_value: [' + str(proto) + ' - '+ str(protocol_ids[proto]) + ']' 
                  ' \nSource_IP: [' + src + ']  Target_IP: [' + str(target) + ']  ' + str(target_name))

            # ICMP
            if proto == 1:
                icmp_type, code, checksum, data = icmp_packet(data)
                print('ICMP Packet: ', end="" )
                # print(TAB_1 +'ICMP Packet' + end ="")
                print(' Type:[{}] \n Code:[{}] \n Checksum:[{}],'.format(
                    icmp_type, code, checksum))
                print(' ICMP Data: ')
                if verbose_flag == 1:
                    print(format_multi_line(DATA_TAB_3, data))

            # TCP
            elif proto == 6:
                (src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack,
                 flag_psh, flag_rst, flag_syn, flag_fin, data) = tcp_segment(data)
                print('TCP Segment: ', end="")
                print(' Source Port: [{}]  Destination Port: [{}]'.format(
                    src_port, dest_port), end="")
                print(' Sequence:[{}]  Acknowledgement:[{}]'.format(
                    sequence, acknowledgement))
                print('Flags: ', end="")
                print(' URG: {}, ACK: {}, PSH: {}, RST: {}, SYN:{}, FIN: {}'.format(
                    flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                if verbose_flag == 1:
                    print(TAB_2 + 'Data:')
                    print(format_multi_line(DATA_TAB_3, data))

            # UDP
            elif proto == 17:
                src_port, dest_port, length, data = udp_segment(data)
                print('UDP Segment: ', end="")
                print(' Source Port: [{}]  Destination Port: [{}]  Length: [{}]'.format(
                    src_port, dest_port, length))

            # Other
            else:
                if verbose_flag == 1:
                    print(TAB_1 + 'Data:')
                    print(TAB_2 + format_multi_line(DATA_TAB_2, data))

        else:
            if verbose_flag == 1:
                print('Data:')
                print(format_multi_line(DATA_TAB_1, data))

        print("====================================================================")

# capturing the frame and unpacking


def ethernet_frame(data):
    # extracting the fields
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_address(dest_mac), get_mac_address(src_mac), socket.htons(proto), data[14:]

# formatting the mac address to its original format


def get_mac_address(bytes_order):
    bytes_str = map('{:02x}'.format, bytes_order)
    return ':'.join(bytes_str).upper()

# if the ethernet protocol is 8 (0x0800), which means it contains a ipv4 packet then dismantle with this function


def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

# formatting the ipv4 address to its original format


def ipv4(addr):
    return '.'.join(map(str, addr))

# dismantling a icmp packet


def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]

# dismantling a tcp packet


def tcp_segment(data):
    (src_port, dst_port, sequence, acknowledgement,
     offset_reversed_flags) = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reversed_flags >> 12) * 4
    flag_urg = (offset_reversed_flags & 32) >> 5
    flag_ack = (offset_reversed_flags & 16) >> 4
    flag_psh = (offset_reversed_flags & 8) >> 3
    flag_rst = (offset_reversed_flags & 4) >> 2
    flag_syn = (offset_reversed_flags & 2) >> 1
    flag_fin = offset_reversed_flags & 1
    return src_port, dst_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

# dismantling a UDP packet


def udp_segment(data):
    src_port, dst_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dst_port, size, data[8:]

# the remaining data is too long to print in a single line, so we are creating a function to convert it into a multi-line readable format


def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


main()

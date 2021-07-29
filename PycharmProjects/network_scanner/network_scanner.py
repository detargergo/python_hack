import scapy.all as scapy
import argparse


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='target network to discover')
    options = parser.parse_args()
    if options.target:
        return options.target
    else:
        parser.error('specify a target network')
        return


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #   scapy.ls(scapy.ARP())
    #   print(arp_request.summary())

    clients_list = []
    for element in answered_list:
        clients_list.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
#       print(element[1].psrc + '\t\t' + element[1].hwsrc)
#       print(element[1].show())
    return clients_list


def print_result(clients_list):
    print('IP\t\t\tMAC Address\n-----------------------------------------')
    for client in clients_list:
        print(client['ip'] + '\t\t' + client['mac'])

target = get_argument()
scanning = scan(target)
print_result(scanning)

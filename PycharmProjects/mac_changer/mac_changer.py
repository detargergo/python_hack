import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface',dest='interface', help='interface to change its mac address')
    parser.add_option('-m', '--mac',dest='new_mac', help='new mac address')
    options = parser.parse_args()[0]
    if not options.interface:
        parser.error('please specify an interface')
    if not options.new_mac:
        parser.error('please specify a new mac')
    return options


def change_mac(interface, new_mac):
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('could not read mac address')
options = get_arguments()
current_mac = get_current_mac(options.interface)
print('current mac = ' + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print('the mac address was successfully changed to ' + current_mac)
else:
    print('the process is failed')

#!/usr/bin/python

#from k5contractsettingsV8 import *

from k5APIwrappersV14 import *

import os

# get OS_ environment vars

OS_USERNAME = os.environ.get('OS_USERNAME', None)
OS_PASSWORD = os.environ.get('OS_PASSWORD', None)
OS_REGION_NAME = os.environ.get('OS_REGION_NAME', None)
OS_PROJECT_ID = os.environ.get('OS_PROJECT_ID', None)
OS_USER_DOMAIN_NAME = os.environ.get('OS_USER_DOMAIN_NAME', None)
demoProjectid = os.environ.get('OS_PROJECT_ID')
region = os.environ.get('OS_REGION', 'uk-1')


k5token = get_scoped_token(OS_USERNAME, OS_PASSWORD, OS_USER_DOMAIN_NAME, OS_PROJECT_ID, OS_REGION_NAME).headers['X-Subject-Token']
print "Token:", k5token

print "- snapshots"
k5json = list_snapshots(k5token, demoProjectid, region).json()
if 'snapshots' in k5json:
  snapshots = k5json['snapshots']
  for snapshot in snapshots:
    print "\t",snapshot.get('name'),"\t",snapshot.get('id')
#    print delete_snapshot(k5token, snapshot.get('id'), demoProjectid, region)

print "- servers"
k5json = list_servers(k5token, demoProjectid, region).json()
if 'servers' in k5json:
  for server in k5json['servers']:
    print"\t", server.get('name'),"\t",server.get('id')
 #   print delete_server(k5token, server.get('id'), demoProjectid, region)

print "- volumes"
k5json = list_volumes(k5token, demoProjectid, region).json()
if 'volume' in k5json:
  for volume in k5json['volumes']:
    print "\t",volume.get('name'),"\t",volume.get('id')
 #   print delete_volume(k5token, volume.get('id'), demoProjectid, region)

print "- security_groups"
k5json = list_security_groups(k5token, region).json()
if 'security_groups' in k5json:
  for sg in k5json['security_groups']:
    print "\t",sg.get('name'),"\t",sg.get('id')
 #   print delete_security_group(k5token, sg.get('id'), region)

print "- global_ips"
for global_ip in list_global_ips(k5token, region).json()['floatingips']:
    print "\t",global_ip
  #  print delete_global_ip(k5token, global_ip.get('id'), region)

# remove vpn and network and router ports...later

print "- routers"
for router in list_routers(k5token, region).json()['routers']:
  print "\t",router.get('name'),"\t",router.get('id')
  for interface in show_router_interfaces(k5token, router.get('id'), region).json()['ports']:
        print "\t\t" , interface.get('name'),"\t".interface.get('id')
#      print remove_interface_from_router(k5token, router.get('id'), interface.get('id'), region)
#    print delete_router(k5token, router.get('id'), region )

print "- ports"
for port in list_ports(k5token, region).json()['ports']:
     print "\t",port.get('name'), "\t", port.get('id')
#     print delete_port(k5token, port.get('id'), region)

print "- subnets"
for subnet in list_subnets(k5token, region).json()['subnets']:
     if "inf" not in subnet.get('name'):
         print "\t",subnet.get('name'),"\t",subnet.get('id')
#         print delete_subnet(k5token, subnet.get('id'), region)

print "- networks"
for network in list_networks(k5token, region).json()['networks']:
    if "ext-net" not in network.get('name'):
        print "\t",network.get('name'),"\t",network.get('id')    
#        print delete_network(k5token, network.get('id'), region)

# TODO floating IPs

print "done "

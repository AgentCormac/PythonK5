#!/usr/bin/python

#from k5contractsettingsV8 import *

from k5APIwrappersV14 import *

import os, sys, getopt



def get_os_envs():
  #define global variables. 
  global k5token
  global OS_PROJECT_ID
  global OS_REGION  
  # get OS_ environment vars
  OS_USERNAME = os.environ.get('OS_USERNAME', None)
  OS_PASSWORD = os.environ.get('OS_PASSWORD', None)
  OS_REGION_NAME = os.environ.get('OS_REGION_NAME', None)
  OS_PROJECT_ID = os.environ.get('OS_PROJECT_ID', None)
  OS_USER_DOMAIN_NAME = os.environ.get('OS_USER_DOMAIN_NAME', None)
  OS_REGION = os.environ.get('OS_REGION', 'uk-1')
  
  if DEBUG == True:
    print "OS_USERNAME", OS_USERNAME
    print "OS_PASSWORD", OS_PASSWORD
    print "OS_OS_REGION_NAME", OS_REGION_NAME
    print "OS_PROJECT_ID", OS_PROJECT_ID
    print "OS_USER_DOMAIN_NAME", OS_USER_DOMAIN_NAME
    print "OS_REGION", OS_REGION
  
  try:
    if OS_USERNAME is not None \
    and OS_PASSWORD is not None \
    and OS_REGION_NAME is not None \
    and OS_PROJECT_ID is not None \
    and OS_USER_DOMAIN_NAME is not None \
    and OS_REGION is not None:
      print("K5 environment variable retrieved from OS")
      k5token = get_scoped_token(OS_USERNAME, OS_PASSWORD, OS_USER_DOMAIN_NAME, OS_PROJECT_ID, OS_REGION_NAME).headers['X-Subject-Token']
      print "Token:", k5token
  except NameError:
      print("OS_USERNAME, OS_PASSWORD, OS_OS_REGION_NAME, OS_PROJECT_ID, OS_USER_DOMAIN_NAME, OS_PROJECT_ID, OS_REGION must be set as OS env variables and exported [see openrc]")
      sys.exit(2)
      
  if k5token == "":
      print "Could not retrieve K% authorisation token"
      sys.exit(2)

  return          

def purge_snapshots():
  print "- snapshots"
  k5json = list_snapshots(k5token, OS_PROJECT_ID, OS_REGION).json()
  if 'snapshots' in k5json:
    snapshots = k5json['snapshots']
    for snapshot in snapshots:
      print snapshot
      print delete_snapshot(k5token, snapshot.get('id'), OS_PROJECT_ID, OS_REGION)
  return

def purge_servers():
  print "- servers"
  k5json = list_servers(k5token, OS_PROJECT_ID, OS_REGION).json()
  if 'servers' in k5json:
    for server in k5json['servers']:
      print server
      print delete_server(k5token, server.get('id'), OS_PROJECT_ID, OS_REGION)
  return

def purge_volumes():
  print "- volumes"
  k5json = list_volumes(k5token, OS_PROJECT_ID, OS_REGION).json()
  if 'volume' in k5json:
    for volume in k5json['volumes']:
      print volume
      print delete_volume(k5token, volume.get('id'), OS_PROJECT_ID, OS_REGION)
  return

def purge_security_groups():
  print "- security_groups"
  k5json = list_security_groups(k5token, OS_REGION).json()
  if 'security_groups' in k5json:
    for sg in k5json['security_groups']:
      print sg
      print delete_security_group(k5token, sg.get('id'), OS_REGION)
  return

def purge_global_ips():
  print "- global_ips"
  for global_ip in list_global_ips(k5token, OS_REGION).json()['floatingips']:
    print global_ip
    print delete_global_ip(k5token, global_ip.get('id'), OS_REGION)
  return

def purge_routers():
  print "- routers"
  for router in list_routers(k5token, OS_REGION).json()['routers']:
    for interface in show_router_interfaces(k5token, router.get('id'), OS_REGION).json()['ports']:
      print remove_interface_from_router(k5token, router.get('id'), interface.get('id'), OS_REGION)
      print delete_router(k5token, router.get('id'), OS_REGION )
  return

def purge_ports():
  print "- ports"
  for port in list_ports(k5token, OS_REGION).json()['ports']:
     print port.get('name'), "\t", port.get('id')
     print delete_port(k5token, port.get('id'), OS_REGION)
  return

def purge_subnets():
  print "- subnets"
  for subnet in list_subnets(k5token, OS_REGION).json()['subnets']:
    if "inf" not in subnet.get('name'):
      print subnet
      print delete_subnet(k5token, subnet.get('id'), OS_REGION)
  return

def purge_networks():
  print "- networks"
  for network in list_networks(k5token, OS_REGION).json()['networks']:
    if "ext-net" not in network.get('name'):
      print delete_network(k5token, network.get('id'), OS_REGION)
  return

def main(argv):
  global DEBUG
  DEBUG = False
  try:
    opts, args = getopt.getopt(argv,"hd")
  except getopt.GetoptError:
    print 'purge_project.py <-d> <-h> <option option ...>'
    sys.exit(2)
  
  if len(sys.argv) == 1:
    print "ERROR: no options specified:"
    print 'purge_project.py <-d> <-h> <option option ...>'
    sys.exit(2)
  
  for opt, arg in opts:
      
    if opt == '-h':
      print 'purge_project.py <-d> <-h> <option option ...>'
      print "-d = debug"
      print "-h = help. This message"
      print "options = snapshots, servers, volumes, security_groups, global_ips, routers, ports, subnets, networks, all"
      sys.exit()
    elif opt == '-d':
       DEBUG = True
    elif opt in ("snapshots", "servers", "volumes", "security_groups", "global_ips", "routers", "ports", "subnets", "networks", "all"):
      if DEBUG == True:
        print "Purging", args
    
    
  if "snapshots" not in args \
  and "servers" not in args \
  and "volumes" not in args \
  and "security_groups" not in args \
  and "global_ips" not in args \
  and "routers" not in args \
  and "ports" not in args \
  and "subnets" not in args \
  and "networks" not in args \
  and "all" not in args:
    print "ERROR: No options specified"
    print "options = snapshots, servers, volumes, security_groups, global_ips, routers, ports, subnets, networks, all"
    sys.exit(2)
            
  get_os_envs()  
    
  if "snapshots" or "all" in args: 
    purge_snapshots()
  if "servers" or "all" in args: 
    purge_servers()
  if "volumes" or "all" in args: 
    purge_volumes()
  if "security_groups" or "all" in args: 
    purge_security_groups()
  if "global_ips" or "all" in args: 
    purge_global_ips()
  if "routers" or "all" in args: 
    purge_routers()
  if "ports" or "all" in args: 
    purge_ports()
  if "subnets" or "all" in args: 
    purge_subnets()
  if "networks" or "all" in args: 
    purge_networks()        

  print "done - wait a while, to allow the commands to complete within k5"

if __name__ == "__main__":
  main(sys.argv[1:])


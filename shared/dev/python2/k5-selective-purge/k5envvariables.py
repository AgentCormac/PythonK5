#!/usr/bin/python

import os

debug = os.environ.get('K5_DEBUG')
#    adminUser = 'landg'
#    adminPassword = 'password'
projectUser = os.environ.get('OS_USERNAME')
projectPassword = os.environ.get('OS_PASSWORD')
contract = os.environ.get('OS_USER_DOMAIN_NAME')
#contractid = '3256d41b17014d5c99727993d6fca821'
defaultid = os.environ.get('OS_DEFAULT_DOMAIN')
project = os.environ.get('OS_PROJECT_ID')
region = os.environ.get('OS_REGION', 'uk-1')
az1 = os.environ.get('OS_AZ1','uk-1a')
az2 = os.environ.get('OS_AZ2', 'uk-1b')
demoProject = os.environ.get('OS_PROJECT_NAME')

if debug:
    print "projectUser=%s" % projectUser
    print "projectPassword=%s" % projectPassword
    print "contract=%s" % contract
    print "defaultid=%s" % defaultid
    print "project=%s" % project
    print "region=%s" % region
    print "az1=%s" % az1
    print "az2=%s" % az2
    print "demoProject=%s" % demoProject

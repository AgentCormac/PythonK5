Python
============

This is a Vagrant environment for testing/learning about Python and the [Fujtisu K5 IaaS](https://s-portal.cloud.global.fujitsu.com) API when you are handicapped by having a Windows machine. ;0)

K5 guides and documentation can be found [here](http://www.fujitsu.com/global/solutions/cloud/k5/guides/).

**Note:** K5 portal is IE only as at 20/01/2017.

The Vagrant script will spin up a CentOS 7 gui machine and install Python 2.7, Robot Framework WebDemo and all the dependencies needed to develop in Python to drive the Fujitsu K5 IaaS APIs:

**NOTE:** This is not the way to write an Ansible Playbook. It is just a quick and dirty script to get up and running quickly.

Instructions
------------

Vagrant up
* Wait for provisioning to complete
* Use GUI to login - vagrant/vagrant
* Open a terminal window

OR

* vagrant ssh python

Your development project should be placed in ~vagrant/shared/dev. This will share access to the code base from your favourite windows IDE or use/install tools on the VM (Atom editor).

Robotframework web demo is also included (as a hangover from a previous box).

```
cd webdemo
python demoapp/server.py &
robot login-tests/
```
**NOTE:** Tests can be disrupted by Firefox setup dialogues, which can happen after an update/install.
**NOTE:** Running a gui in a vm is not a good idea. May need to increase the wait time and/or memory allocated to the VM for the vm to enable the browser to respond in time for the framework.
```
${DELAY}          0 in login_tests/resource.robot
```

Pre-requisites
--------------

* Virtual Box
* Cygwin
* Vagrant (1.8.5)
* Vagrant plugin vagrant-vbguest

The Vagrantfile will spin up the VMs and install Ansible, ssh-keys etc. Ansible will the provision the VM. The ansible script can be found in the **shared** directory.

K5 API development
==================
This box was created to take advantage of the great work carried out by Nick Cross over at [mohclips](https://github.com/mohclips/k5-ansible-infra) (20/01/2017). Be sure to recusively clone the repository into shared/dev
```
git clone --recursive https://github.com/mohclips/k5-ansible-infra.git
```

Dependencies
------------

K5 API python (pip) development dependencies:


* requests
* cryptography
* shade

Linux dependencies:


* python-devel
* python-crypto
* libffi-devel
* python-netifaces
* openssl-devel

Create your own openrc credentials file and run
```
. openrc
```
See [mohclips](https://github.com/mohclips/k5-ansible-infra) for further details.

K5 API Ansible
==============

get repo from mohclips (as described above).
```
cd k5-ansible-infra
. openrc
ansible-paybook provision_infra.yml
```

openrc should be modified to contain your personal K5 credentials. The ansible scripts will use this nformation to authenticate against K5.

Additional scripts
------------------
In the shared/ansible folder there are the following scripts which may be useful:

* x11support.yml - Adds Xll packages
* liclipse.yml - Adds Liclipse IDE

To use x11 windows on your windows box install and run Cygwin X11 server or XMing.
**NOTE:** XMing is easier to set up and run. Cygwin X11 server will need configuring correctly to use. **Initial** X11 window onto the client VM will have to be through a console that supports X11 e.g Putty. **Subsequent** windows can be started  from a normal cli by ssh'ing into the vm with the X11 switch:
On vm:
```
ansible-playbook ~/shared/ansible/x11support.yml
```
Log onto vm with Putty (making sure X11 settings are correct in the Putty connection profile Connection -> ssh > X11):
```
xeyes &
```
Connect to VM from normal vm with X11 switch
```
vagrant ssh python -- -Y
ansible-playbook ~/shared/ansible/liclipse.yml
liclipse &
```


Enjoy!

################################################################
#
# Author: 	Mark Higginbottom
#
# Date:		27/09/2016
#
# Vagrant PROJECT file to create Ansible provisioned VM for Robot Framework testing
#
# Dependencies:
#     vagrant plugin install vagrant-triggers
#     vagrant plugin install vagrant-vbguest
#################################################################
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'


Vagrant.configure("2") do |config|
  config.ssh.insert_key = false

  ##python VM
  config.vm.define "python" do |python|
#    python.vm.box = "bento/centos-7.2"
#    python.vm.box = "pbarriscale/centos7-gui"
    python.vm.box = "centos/7"
    python.vm.hostname = 'python'

    python.vm.network :private_network, ip: "192.168.100.101"
    python.vm.network :forwarded_port, guest: 22, host: 10122, id: "ssh"
    python.vm.network :forwarded_port, guest: 7272, host: 7272, id: "pythontestport"


    python.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 2018]
      v.customize ["modifyvm", :id, "--name", "python"]
# Show VM?
#	  v.gui = true
    end

	#map shared directory
	python.vm.synced_folder "shared", "/home/vagrant/shared"

	python.vm.provision "shell", inline: <<-SHELL
		#Basic vanilla installation to bootstrap Ansible.
		#set ownership of shared directory to vagrant
		sudo chown -R vagrant:vagrant /home/vagrant/shared
		##Install Ansible on python node
		#sudo apt-get update -y
		sudo yum update -y
		sudo yum install vim -y
		sudo yum install epel-release -y
		sudo yum install ansible -y
		sudo yum install yum-utils
		##Install Git
		sudo yum install git -y
		##Turn off ansible key checking
		export ANSIBLE_HOST_KEY_CHECKING=false
	SHELL

	##run info script
    python.vm.provision "info", type: "shell", path: "scripts/vminfo.sh"

	##Ansible provisioning from playbook that is on the Guest VM
	python.vm.provision "ansible_local" do |ansible|
		ansible.verbose = "true"
		ansible.extra_vars = {servers: "python"} #inject the name of the server we want to apply this ansible config to.
		ansible.playbook = "shared/ansible/site.yml"
    end

  end

  # clean up files on the host after the guest is destroyed
  config.trigger.after :destroy do
    run "scripts\\reset_known_hosts.bat"
  end

end

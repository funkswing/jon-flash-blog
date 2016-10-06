# Automate the Boring Stuff with...Ansible, created in Python
>  The first rule of any technology used in a business is that automation applied to an efficient operation will magnify the efficiency. The second is that automation applied to an inefficient operation will magnify the inefficiency - _Bill Gates_

Ansible is an “agentless” platform for managing and configuring computers/servers/VMs remotely using OpenSSH (Powershell for managing Windows). Ansible can manage the local machine it is running on as well if needed. SSH authentication is handled with SSH keys by default, although passwords are allowed. Likewise, if a “sudo” password is required it can also be passed to the remote machine.

This post will go over installing Ansible on RHEL7 and configuring a remote VM, also running RHEL7, from its base install to running a NGNIX web server using Docker containerization.

### Note about Windows:
Windows support at this time is limited to configuring machines only. The control machine must be Unix-based, but Ansible (as of version 1.7) can manage a remote Windows machine with no additional software needing to be installed. This post will not cover managing Windows machines using Ansible. Here are are the [official docs](http://docs.ansible.com/ansible/intro_windows.html) regarding Ansible and Windows.

1.  Step 1 - Installing Ansible on RHEL7


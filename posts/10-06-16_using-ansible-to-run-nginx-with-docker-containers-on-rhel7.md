# Automate the Boring Stuff with...Ansible, created in Python
>  The first rule of any technology used in a business is that automation applied to an efficient operation will magnify the efficiency. The second is that automation applied to an inefficient operation will magnify the inefficiency - _Bill Gates_

Ansible is an “agentless” platform for managing and configuring computers/servers/VMs remotely using OpenSSH (Powershell for managing Windows). Similar in operation to Puppet and Chef, yet from a developer’s (let alone a Python developer’s) point of view Ansible is simpler to use and easier to setup and start using to solve real issues. Ansible is written in Python, but for general use cases you work with YAML (there’s no Python code in this post!). Ansible may have been written Python, but you can write custom modules in whatever language fits your fancy (although you will be [giving up a lot of shortcut goodies](http://docs.ansible.com/ansible/developing_modules.html)). Let’s dive into automation with a simple example familiar to many devs: get Docker running on a fresh VM install of RHEL7 serving up a NGINX web server, all without ever opening a terminal on the new VM.

### Additional Notes:
Ansible can manage the local machine it is running on as well, if needed. SSH authentication is handled with SSH keys by default, although passwords are allowed. Likewise, if a “sudo” password is required it can also be passed to the remote machine.

### Note about Windows:
Windows support at this time is limited to configuring machines only - the control machine must be Unix-based. Ansible (as of version 1.7) can manage a remote Windows machine with no additional software needing to be installed, maintaining its “agentless” billing. This post will not cover managing Windows machines, however. Here are are the official docs regarding Ansible and Windows: [http://docs.ansible.com/ansible/intro_windows.html](http://docs.ansible.com/ansible/intro_windows.html)

1.  Step 1 - Installing Ansible on RHEL7


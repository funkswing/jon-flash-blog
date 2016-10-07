# Automate the Boring Stuff with...Ansible, created in Python
>  The first rule of any technology used in a business is that automation applied to an efficient operation will magnify the efficiency. The second is that automation applied to an inefficient operation will magnify the inefficiency - _Bill Gates_

Ansible is an “agentless” platform for managing and configuring computers/servers/VMs remotely using OpenSSH (Powershell for managing Windows). Similar in operation to Puppet and Chef, yet from a developer’s (let alone a Python developer’s) point of view Ansible is simpler to use and easier to setup and start using to solve real issues. Ansible is written in Python, but for general use cases you work with YAML (there’s no Python code in this post!). Ansible may have been written Python, but you can write custom modules in whatever language fits your fancy (although you will be [giving up a lot of shortcut goodies](http://docs.ansible.com/ansible/developing_modules.html)). Let’s dive into automation with a simple example familiar to many devs: get Docker running on a fresh VM install of RHEL7 serving up a NGINX web server, all without ever opening a terminal on the new VM.

### Additional Notes:
This tutorial assumes two machines (VMs, instances, etc…) that can communicate to each other over HTTP port 80. The sample scenario detailed here was performed on two VirtualBox VMs with CentOS7 (I know...I lied about RHEL7 in the title, but in production that’s what we use!).  SSH authentication is handled with SSH keys by default, although passwords are allowed. I’ll show the way with passwords since it is more likely in a “trying out Ansible” scenario. Likewise, if a “sudo” password is required it can also be passed to the remote machine. Lastly, Ansible can manage the local machine it is running on, if needed, but that is not explicitly covered here.

### Note about Windows:
Windows support at this time is limited to configuring machines only - the control machine must be Unix-based. Ansible (as of version 1.7) can manage a remote Windows machine with no additional software needing to be installed, maintaining its “agentless” billing. This post will not cover managing Windows machines, however. Here are are the official docs regarding Ansible and Windows: [http://docs.ansible.com/ansible/intro_windows.html](http://docs.ansible.com/ansible/intro_windows.html)

## Installing Ansible on RHEL7

Installing Ansible on RHEL7 is as simple as a ```yum install ansible```, yet this tutorial will make the assumption that you are using a fresh install of RHEL7. So, first things first, do your ```yum update``` and ```systemctl reboot``` before moving on to adding the additional repos Red Hat does not enable out of the box.

### Enable new RHEL 7 Extras and Optional repos
Using the new subscription manager, enable the “extras” and “options” repos:

```sudo subscription-manager repos --enable rhel-7-server-optional-rpms```
```sudo subscription-manager repos --enable rhel-7-server-extras-rpms```

### Add the EPEL repository
```
mkdir ~/tmp && cd ~/tmp
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum install -y epel-release-latest-7.noarch.rpm
```

### Finally, install Ansible
```
sudo yum install -y ansible
```

Now we are ready to start using Ansible to manage and configure another machine remotely.

## Managing Another VM with Ansible

Ansible creates a template file to configure which machines it manages:
```
/etc/ansible/hosts
```

Add the remote IP/host of the machine you wish to manage to this file:

```
echo -e "192.168.56.102\nserver.example.com" >> /etc/ansible/hosts
```

Now test the connection using Ansible. By default, Ansible will authenticate using SSH public keys. You can also use private keys with the ```--private-key``` flag to specify a pem file.

First, setup SSH-agent to use the proper credentials within your shell:
```
ssh-agent bash
ssh-add ~/.ssh/id_rsa
```

Then, ping the remote host(s):

```
ansible all -m ping -u <username>
```

    -u <username> = username you wish to log in with via SSH (e.g. ssh <username>@host)

If you do not have SSH keys setup or you just want to test out Ansible quick and dirty, you can force the use of username and password.

```
ansible all -m ping -k -u <username>
```

    -k = prompt for password instead of using SSH key
    -u <username> = username to log in with (default is whatever user the current shell is)

If successful you will see the response, which is formatted as JSON:
```
192.168.56.102 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

If you need to connect and manage something that requires root privileges, such as a system service, you can use the “become” flag (```-b```) to become root on the remote machine. If you are not using SSH keys, you can pass the -K (uppercase) flag to be prompted for sudo password:

```
ansible all -m ping -k -u student -b -K
```

If you need to switch to a specific user, say apache, add ```--become-user <username>```

```
ansible all -m ping -k -u student -b --become-user apache -K
```

## Ad-Hoc Commands

Now that you have Ansible working, let's play with some more Ad-Hoc commands before getting into Playbooks - Ansible’s configuration language.

First, let's give our host a name, if you haven’t already, to allow for specific hosts to be operated on. Edit the ```/etc/ansible/hosts``` file to label the hosts in square brackets above their entry:

```
[remote1]
192.168.56.102
```

OK, lets control the remote machine! Try some Ad-hoc commands:

Yum update:

```ansible remote1 -m shell -a "yum update -y" -u <username> -b -K```

Reboot remote:

```ansible remote1 -m shell -a "reboot" -u <username> -b -K```

The JSON response says this failed, but it rebooted the remote machine, disconnecting the SSH and triggered the failed response. Nothing is perfect...

## Modules

This isn’t much different than a shell script, you say? With Ad-hoc commands this is true, but the real power from Ansible comes from Modules and their ability to have context when issuing its commands. Modules strive to make Ansible idempotent. Idempotence means Ansible will always result in the same outcome, regardless how many times it is run. Essentially, you are specifying the desired final state with Ansible, and Ansible determines what it needs to do (and not do) to get there. Running the same Ansible module twice would result in the same final state...something that is not always true with shell scripts.

Install Docker on remote:

```
ansible remote1 -m yum -a name=docker -u <username> -b -K
```

Notice the return JSON. The “changed” value is set to “true”, and the “results” value is the STDOUT. If you repeat the same module command again, the “changed” value would be “false”, indicating the final state was not changed, as docker is already installed on the system.

Ansible has many modules pre-baked into it. These range from yum to apt to docker and pip. Look at the list of all available modules to see if the task you want to perform is already a module:
[http://docs.ansible.com/ansible/list_of_all_modules.html](http://docs.ansible.com/ansible/list_of_all_modules.html)

## Playbooks

Playbooks are sequence of modules to run written in YAML. They are very powerful and allow for synchronous and asynchronous execution, as well as jumping around plays to accomplish the desired state(s) of the remote machines. Here I will show a simple playbook that installs Docker and starts running a NGINX web server container on Port 80.

### Playbook to install Docker and Run NGINX on port 80 in a container

    ---
    # This Playbook will install Docker and run a NGINX image on port 80
    
    - hosts: all  # Executes play on all hosts, this can explicitly name specific hosts if needed
      remote_user: <username>  # User you wish to SSH into remote with
      become: yes  # Become root user
      tasks:
      - name: update system packages
        yum: name=* state=latest
      - name: install docker  # Human readable description of task
        yum: name=docker state=latest  # yum install docker, ensuring its the latest version
      - name: install pip  # Install pip, this is a fresh RHEL7 install, so pip could not be available
        yum: name=python-pip
      - name: pip install docker-py  # Needed for Ansible to execute Docker commands
        pip: name=docker-py
      - name: Create NGINX docker container
        docker_container:
          name: nginx_80
          image: nginx
          ports:
          - "80:80"  # Bind host port to container port ("host:container")

### Run Playbook:

```ansible-playbook docker_nginx.yml```

    Add -i <hosts_file> if you want to specify a hosts file (default is /etc/ansible/hosts)
    Add -K flag if you need to authenticate for sudo

More Playbook examples can be found:
[http://docs.ansible.com/ansible/playbooks_intro.html](http://docs.ansible.com/ansible/playbooks_intro.html)

Now you can visit the hosts IP in a browser (or curl) to see the NGINX welcome page:

```
curl http://192.168.56.102/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

That’s it! Obviously there are many more “plays” we could/should add to this Playbook to increase its robustness, but presented here is just enough of the iceberg to hit the ground running.

More Playbook examples can be found:
[http://docs.ansible.com/ansible/playbooks_intro.html](http://docs.ansible.com/ansible/playbooks_intro.html)


## Ansible Official Docs: 

Install - [http://docs.ansible.com/ansible/intro_installation.html](http://docs.ansible.com/ansible/intro_installation.html)

Tutorial - [http://docs.ansible.com/ansible/intro_getting_started.html](http://docs.ansible.com/ansible/intro_getting_started.html)

Become - [http://docs.ansible.com/ansible/become.html](http://docs.ansible.com/ansible/become.html)


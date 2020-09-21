# remote-ssh-tunnel-controller-service

## Dependencies:

*  python3
*  python-daemon
*  pid
*  asingleton
*  PyDispatcher
*  Dependencies of [remote-ssh-tunnel-controller-lib](https://github.com/guallo/remote-ssh-tunnel-controller-lib/tree/de08ad50c11f131ae7601e77c0688861463898cf#dependencies)
*  Dependencies of [fusionpbx-client-lib](https://github.com/guallo/fusionpbx-client-lib/tree/ae774a7316f6783c97c0a25294eb0804647f5a12#dependencies)

## Installation

### Manual

#### Debian 10

```bash
sudo apt-get install python3 python3-pip firefox-esr git
sudo pip3 install python-daemon pid asingleton PyDispatcher paramiko selenium

sudo adduser --system --group rssht-controller-service
sudo su -s /bin/bash - rssht-controller-service

git clone https://github.com/guallo/remote-ssh-tunnel-controller-service.git
cd remote-ssh-tunnel-controller-service
git submodule update --init -- lib/rssht_controller_lib/
git submodule update --init -- lib/fpbx_client_lib/

wget -q https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar xzf geckodriver-v0.26.0-linux64.tar.gz

mkdir -p $HOME/.ssh
ssh-keygen -C rssht-controller-service -N "" -f id_rsa
ssh-copy-id -i id_rsa.pub rssht-server@<SSH-SERVER> -p 443

sed -i 's!\(RSSHT_SERVER_ADDR = \).*$!\1"<SSH-SERVER>"!' lib/rssht_controller_lib/config.py
sed -i 's!\(KEY_FILENAME = \).*$!\1os.path.join(LIB_DIR, os.pardir, os.pardir, "id_rsa")!' lib/rssht_controller_lib/config.py

sed -i 's!\(CHECK_INTERVAL = \).*$!\1<CHECK-INTERVAL>!' rssht_controller_service/config.py
sed -i 's!\(MAX_THREADS = \).*$!\1<MAX-THREADS>!' rssht_controller_service/config.py

sed -i 's!\(GECKODRIVER_LOG_FILENAME = \).*$!\1os.devnull!' configd/p??_fpbx_failover.py

nano configd/p??_fpbx_failover.py  # Search for AGENT_CLIENT_MAP and edit as needed.

nano configd/p??_fpbx_failover_notifier.py  # Edit as needed.

chmod 600 lib/rssht_controller_lib/config.py
chmod 600 rssht_controller_service/config.py
chmod 600 configd/p??_*.py
chmod u+x __main__.py
exit

sudo cp /home/rssht-controller-service/remote-ssh-tunnel-controller-service/rssht-controller.service /lib/systemd/system/
sudo systemctl enable rssht-controller.service
sudo systemctl start rssht-controller.service
```

## Installation upgrade

### Manually

#### Debian 10

**NOTICE:** This method currently do not deploy (if upgraded) the *systemd unit* file [`rssht-controller.service`](https://github.com/guallo/remote-ssh-tunnel-controller-service/blob/master/rssht-controller.service).

```bash
sudo systemctl stop rssht-controller.service

sudo su -s /bin/bash - rssht-controller-service
cd remote-ssh-tunnel-controller-service

git config user.name temp
git config user.email temp
git add -A
git commit -m 'temp'
git pull --rebase
# Resolve any conflicts (if any) that could arise from previous command.
git reset HEAD~1
chmod 600 rssht_controller_service/config.py
chmod 600 configd/p??_*.py
chmod 600 id_rsa
chmod 744 __main__.py
git config --unset user.name
git config --unset user.email

cd lib/rssht_controller_lib/
git config user.name temp
git config user.email temp
git stash push -a
cd ../../
git submodule update --checkout -- lib/rssht_controller_lib/
cd lib/rssht_controller_lib/
git stash apply
# Resolve any conflicts (if any) that could arise from previous command.
git stash drop
chmod 600 config.py
git config --unset user.name
git config --unset user.email
cd ../../

cd lib/fpbx_client_lib/
git config user.name temp
git config user.email temp
git stash push -a
cd ../../
git submodule update --checkout -- lib/fpbx_client_lib/
cd lib/fpbx_client_lib/
git stash apply
# Resolve any conflicts (if any) that could arise from previous command.
git stash drop
git config --unset user.name
git config --unset user.email
cd ../../

exit

sudo systemctl start rssht-controller.service
```

## Uninstallation

### Manually

#### Debian 10

```bash
sudo systemctl stop rssht-controller.service
sudo systemctl disable rssht-controller.service
sudo rm /lib/systemd/system/rssht-controller.service

# Remove the public key entry (about "/home/rssht-controller-service/remote-ssh-tunnel-controller-service/id_rsa.pub")
# from the "/home/rssht-server/.ssh/authorized_keys" file in the "Intermediate SSH Server" and then restart the "sshd" service.

sudo deluser --system --force --remove-home rssht-controller-service
```

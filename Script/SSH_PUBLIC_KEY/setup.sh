#!/bin/bash
scp -p ~/.ssh/id_rsa.pub root@raspberrypi3b.local:/root/.ssh/a.pub
ssh root@raspberrypi3b.local ./newuser.sh
cat SSH_PUBLIC_KEY/raspberrypi_id_rsa.pub>>~/.ssh/authorized_keys

mkdir tmp
name=$(whoami)
host=$(hostname)
tmp_path=$(pwd)
echo 'Please enter where u want the image vector to be saved'
read save_path

touch run.sh
echo "ssh root@raspberrypi3b.local python2.7 test_scp.py $name@$host $tmp_path/tmp
python2.7 piRetina.py $save_path" > run.sh
chmod +x run.sh


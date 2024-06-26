#!/usr/bin/env bash

set -e

# Generate SSH Keys
mkdir -p ./.ssh
if [ ! -f ./.ssh/id_rsa ]; 
then
    ssh-keygen -t rsa -f ./.ssh/id_rsa -N ""
else
    echo "SSH Key already exists"
fi
echo "NOTICE: MAKE SURE TO GIVE THE GENERATED **PUBLIC** KEY GITHUB READ ACCESS TO JVOY!"

echo "
Host github.com
    HostName github.com
    IdentityFile /etc/ssh/id_rsa
" > ./.ssh/ssh_config


#!/usr/bin/env bash

set -e

# Init environment 
if [ ! -f .env ]; 
then
    cp .env.example .env
else
    echo ".env file already exists"


# Init submodules
git submodule status | grep '^-' > /dev/null &&  git submodule init && git submodule update --recursive;

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

# Build Analyst UI
cd analyst-ui
make beaker_kernel/server/ui/index.html
cd ..

# Build docker compose
docker compose build
#!/bin/bash

git submodule status | grep '^-' > /dev/null &&  git submodule init;
[[ -f beaker-kernel-link/package.json ]] || git submodule update --recursive;

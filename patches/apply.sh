#!/bin/bash

# LibreSSL OpenBSD codebase branch fix
#echo libressl-v4.0.0 >workspace/libressl/OPENBSD_BRANCH
sed -i '/LIBRESSL_GIT_OPTIONS="\${LIBRESSL_GIT_OPTIONS:- --depth=8}"/d' ./workspace/libressl/update.sh

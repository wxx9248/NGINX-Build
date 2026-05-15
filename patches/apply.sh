#!/bin/bash
set -euo pipefail

LIBRESSL_VERSION=$(jq -r '.libressl.version' versions.json)

# LibreSSL OpenBSD codebase branch fix
echo "libressl-${LIBRESSL_VERSION}" >workspace/libressl/OPENBSD_BRANCH
sed -i '/LIBRESSL_GIT_OPTIONS="\${LIBRESSL_GIT_OPTIONS:- --depth=8}"/d' ./workspace/libressl/update.sh

#!/bin/bash
set -euo pipefail

LIBRESSL_VERSION=$(jq -r '.libressl.version' versions.json)
UPDATE_SH=./workspace/libressl/update.sh

# LibreSSL OpenBSD codebase branch fix
echo "libressl-${LIBRESSL_VERSION}" >workspace/libressl/OPENBSD_BRANCH

# The build container sees workspace/libressl without its .git, so update.sh never detects
# that it is on a tag and takes its "Not on a tag" path: it checks out OPENBSD_BRANCH (a tag
# name, so HEAD ends up detached) and then runs `git pull`, which fails on a detached HEAD.
# The `rev-list origin/$openbsd_branch` lookup before it fails as well, since only a tag of
# that name exists. Through v4.3.3 upstream ran this whole block under `set +e`; v4.4.0
# re-enables `set -e` before the lookup, which turns both of those expected failures fatal.
# Put the `set +e` window back around the block. On older versions this is a no-op.
sed -i \
    -e '/^commit=`git -C openbsd rev-list /i set +e' \
    -e '/^# setup source paths$/i set -e' \
    "$UPDATE_SH"

# A sed that matches nothing exits 0, so check that the edit landed. Upstream reworded this
# script before and the patch silently stopped applying.
if ! grep -B1 -q '^commit=`git -C openbsd rev-list ' "$UPDATE_SH" ||
    [ "$(grep -B1 '^commit=`git -C openbsd rev-list ' "$UPDATE_SH" | head -1)" != "set +e" ] ||
    [ "$(grep -B1 '^# setup source paths$' "$UPDATE_SH" | head -1)" != "set -e" ]; then
    echo "patches/apply.sh: could not re-open the set +e window in $UPDATE_SH; upstream changed it" >&2
    exit 1
fi

# portable v4.4.0 ships patches/cert.pem.patch, which takes cert.pem from rev 1.36 to 1.37 (the
# eMudhra intermediate revocation). OpenBSD's libressl-v4.4.0 tag already carries that change as
# stable-branch rev 1.36.2.1, so both hunks fail and update.sh aborts. Patched 1.37 and 1.36.2.1
# are identical apart from the RCS id line (126 certificates each). Drop the redundant patch for
# this exact version only, so a later version that ships it again still gets applied, and fails
# loudly if it does not fit.
if [ "$LIBRESSL_VERSION" = "v4.4.0" ]; then
    rm -f ./workspace/libressl/patches/cert.pem.patch
fi

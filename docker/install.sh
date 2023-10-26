#!/bin/sh
set -e -x
target_arch=$1
target_variant=$2

target_platform=$target_arch
if [ "$target_variant" != "" ]
then
    target_platform="$target_arch/$target_variant"
fi

case "$target_platform" in
    "amd64")
        cp "/build/nginx-alpine-amd64/nginx" /usr/sbin/
        ;;
    "arm/v6")
        cp "/build/nginx-alpine-arm32@v6/nginx" /usr/sbin/
        ;;
    "arm/v7")
        cp "/build/nginx-alpine-arm32@v7/nginx" /usr/sbin/
        ;;
    "arm64")
        cp "/build/nginx-alpine-arm64@v8/nginx" /usr/sbin/
        ;;
    "386")
        cp "/build/nginx-alpine-i386/nginx" /usr/sbin/
        ;;
    "ppc64le")
        cp "/build/nginx-alpine-ppc64le/nginx" /usr/sbin/
        ;;
    *)
        echo Unknown platform: "$target_platform"
        exit 1
        ;;
esac

chown root:root /usr/sbin/nginx
chmod 755 /usr/sbin/nginx

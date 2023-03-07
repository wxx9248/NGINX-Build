# -*- coding: utf-8 -*-
import typing

from package_manager.impl import *

DISTRO_PM_GENERATOR_DICT = {
    "focal": AptCommandGenerator,
    "jammy": AptCommandGenerator,
    "archlinux": PacmanCommandGenerator,
    "alpine": ApkCommandGenerator
}

UBUNTU_PACKAGE_NAME_DICT = {
    "build-essential": "build-essential",
    "coreutils": "coreutils",
    "binutils": "binutils",
    "diffutils": "diffutils",
    "libtool": "libtool",
    "perl": "perl",
    "git": "git",
    "libgd": "libgd-dev",
    "libgeoip": "libgeoip-dev",
    "libxml2": "libxml2-dev",
    "libxslt": "libxslt-dev",
    "bash": "bash",
    "autoconf": "autoconf",
    "automake": "automake"
}

DISTRO_PACKAGE_NAME_DICT = {
    "focal": UBUNTU_PACKAGE_NAME_DICT,
    "jammy": UBUNTU_PACKAGE_NAME_DICT,
    "archlinux": {
        "build-essential": "base-devel",
        "coreutils": "coreutils",
        "binutils": "binutils",
        "diffutils": "diffutils",
        "libtool": "libtool",
        "perl": "perl",
        "git": "git",
        "libgd": "gd",
        "libgeoip": "geoip",
        "libxml2": "libxml2",
        "libxslt": "libxslt",
        "bash": "bash",
        "autoconf": "autoconf",
        "automake": "automake"
    },
    "alpine": {
        "build-essential": "alpine-sdk",
        "coreutils": "coreutils",
        "binutils": "binutils",
        "diffutils": "diffutils",
        "libtool": "libtool",
        "perl": "perl",
        "git": "git",
        "libgd": "gd-dev",
        "libgeoip": "geoip-dev",
        "libxml2": "libxml2-dev",
        "libxslt": "libxslt-dev",
        "bash": "bash",
        "autoconf": "autoconf",
        "automake": "automake"
    }
}


def get_distro_pm_command_generator(distro: str):
    return DISTRO_PM_GENERATOR_DICT.get(distro)()


def get_distro_package_name_dict(distro: str) -> typing.Dict[str, str]:
    return DISTRO_PACKAGE_NAME_DICT.get(distro)

# -*- coding: utf-8 -*-
import typing

from package_manager.impl import *
from .common import DistroType

DISTRO_PM_GENERATOR_DICT = {
    ("ubuntu", "jammy"): AptCommandGenerator(),
    ("archlinux", ""): PacmanCommandGenerator(),
    ("alpine", ""): ApkCommandGenerator()
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
    "automake": "automake",
    "linux-headers": "linux-headers-generic"
}

DISTRO_PACKAGE_NAME_DICT = {
    ("ubuntu", "jammy"): UBUNTU_PACKAGE_NAME_DICT,
    ("archlinux", ""): {
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
        "automake": "automake",
        "linux-headers": "linux-headers"
    },
    ("alpine", ""): {
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
        "automake": "automake",
        "linux-headers": "linux-headers"
    }
}


def get_distro_pm_command_generator(distro: DistroType):
    return DISTRO_PM_GENERATOR_DICT.get(distro)


def get_distro_package_name_dict(distro: DistroType) -> typing.Dict[str, str]:
    return DISTRO_PACKAGE_NAME_DICT.get(distro)

# -*- coding: utf-8 -*-
import typing

from package_manager.impl import *
from .common import DistroType

DISTRO_PM_GENERATOR_DICT = {
    ("alpine", ""): ApkCommandGenerator()
}

DISTRO_PACKAGE_NAME_DICT = {
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
        "linux-headers": "linux-headers",
        "libzstd": "zstd-dev"
    }
}


def get_distro_pm_command_generator(distro: DistroType):
    return DISTRO_PM_GENERATOR_DICT.get(distro)


def get_distro_package_name_dict(distro: DistroType) -> typing.Dict[str, str]:
    return DISTRO_PACKAGE_NAME_DICT.get(distro)

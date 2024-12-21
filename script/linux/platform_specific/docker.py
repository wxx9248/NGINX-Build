# -*- coding: utf-8 -*-
import typing

from .common import DistroType, ArchType

OVERRIDE_DICT: typing.Dict[typing.Tuple[DistroType, ArchType], str] = {
    (("archlinux", ""), ("arm64", "v8")): "agners/archlinuxarm-arm64v8"
}


def get_docker_image_repository(distro: DistroType, arch: ArchType) -> str:
    if (distro, arch) in OVERRIDE_DICT:
        return OVERRIDE_DICT[(distro, arch)]

    builder = []

    builder.append(distro[0])

    if distro[1] != "":
        builder.append(":")
        builder.append(distro[1])

    return "".join(builder)


def get_docker_image_platform(arch: ArchType) -> str:
    builder = ["linux"]
    
    if arch[0] == "":
        return "".join(builder)

    builder.append("/")
    builder.append(arch[0])

    if arch[1] == "":
        return "".join(builder)
    
    builder.append("/")
    builder.append(arch[1])

    return "".join(builder)

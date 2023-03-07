# -*- coding: utf-8 -*-
import typing

ArchTagType: typing.TypeAlias = typing.Optional[str]
DistroTagType: typing.TypeAlias = str

ARCH_DICT: typing.Dict[str, ArchTagType] = {
    "amd64": None,
    "aarch64": "arm64v8"
}

DISTRO_DICT: typing.Dict[str, DistroTagType] = {
    "focal": "ubuntu:focal",
    "jammy": "ubuntu:jammy",
    "archlinux": "archlinux",
    "alpine": "alpine"
}

TAG_OVERRIDE_DICT: typing.Dict[typing.Tuple[str, str], str] = {
    ("archlinux", "aarch64"): "agners/archlinuxarm-arm64v8"
}


def get_docker_image_tag(distro: str, arch: str) -> str:
    if distro not in DISTRO_DICT:
        raise NotImplementedError(f"Unsupported distro: {distro}")

    if arch not in ARCH_DICT:
        raise NotImplementedError(f"Unsupported arch: {arch}")

    if (distro, arch) in TAG_OVERRIDE_DICT:
        return TAG_OVERRIDE_DICT[(distro, arch)]

    tag = ""

    arch_tag: ArchTagType = ARCH_DICT.get(arch)
    if arch_tag is not None:
        tag = arch_tag + "/"

    distro_tag: DistroTagType = DISTRO_DICT.get(distro)
    tag += distro_tag

    return tag

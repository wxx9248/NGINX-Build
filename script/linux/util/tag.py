# -*- coding: utf-8 -*-
import typing

# Distro(distro, version)
DistroType: typing.TypeAlias = typing.Tuple[str, typing.Optional[str]]
# Arch(arch, variant)
ArchType: typing.TypeAlias = typing.Tuple[typing.Optional[str], typing.Optional[str]]

DISTRO_DICT: typing.Dict[str, DistroType] = {
    "ubuntu/jammy": ("ubuntu", "jammy"),
    "archlinux": ("archlinux", None),
    "alpine": ("alpine", None)
}

ARCH_DICT: typing.Dict[str, ArchType] = {
    "amd64": ("amd64", None),
    "arm64/v8": ("arm64", "v8"),
    "arm32/v6": ("arm32", "v6"),
    "arm32/v7": ("arm32", "v7"),
    "i386": ("i386", None),
    "ppc64le": ("ppc64le", None),
    "s390x": ("s390x", None)
}

OVERRIDE_DICT: typing.Dict[typing.Tuple[DistroType, ArchType], str] = {
    (("archlinux", None), ("arm64", "v8")): "agners/archlinuxarm-arm64v8"
}


def get_docker_image_tag(distro_version: str, arch_variant: str) -> str:
    if distro_version not in DISTRO_DICT:
        raise NotImplementedError(f"Unsupported distro version: {distro_version}")

    if arch_variant not in ARCH_DICT:
        raise NotImplementedError(f"Unsupported arch variant: {arch_variant}")

    distro = DISTRO_DICT.get(distro_version)
    arch = ARCH_DICT.get(arch_variant)

    if (distro, arch) in OVERRIDE_DICT:
        return OVERRIDE_DICT[(distro, arch)]

    tag_builder = []

    if arch[0] is not None:
        tag_builder.append(arch[0])

    if arch[1] is not None:
        tag_builder.append(arch[1])

    if len(tag_builder) != 0:
        tag_builder.append("/")

    tag_builder.append(distro[0])

    if distro[1] is not None:
        tag_builder.append(":")
        tag_builder.append(distro[1])

    return "".join(tag_builder)

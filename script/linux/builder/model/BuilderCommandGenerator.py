# -*- coding: utf-8 -*-
import typing

from platform_specific import DistroType, ArchType


class BuilderCommandGenerator:
    def __init__(self, distro: DistroType, arch: ArchType):
        self.__distro = distro
        self.__arch = arch

    @property
    def distro(self):
        return self.__distro

    @property
    def arch(self):
        return self.__arch

    def configure(self) -> typing.List[str]:
        return []

    def build(self) -> typing.List[str]:
        return []

    def install(self) -> typing.List[str]:
        return []

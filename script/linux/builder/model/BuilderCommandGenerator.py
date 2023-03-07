# -*- coding: utf-8 -*-
import typing


class BuilderCommandGenerator:
    def __init__(self, distro: str, arch: str):
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

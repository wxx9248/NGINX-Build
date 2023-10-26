# -*- coding: utf-8 -*-
import typing

from builder.model import BuilderCommandGenerator
from platform_specific import DistroType, ArchType


class LibreSSLBuilderCommandGenerator(BuilderCommandGenerator):
    def __init__(self, distro: DistroType, arch: ArchType):
        super().__init__(distro, arch)

    def configure(self) -> typing.List[str]:
        return [
            "cd libressl",
            "./autogen.sh",
            "cd .."
        ]

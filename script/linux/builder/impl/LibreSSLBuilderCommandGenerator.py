# -*- coding: utf-8 -*-
import typing

from builder.model import BuilderCommandGenerator


class LibreSSLBuilderCommandGenerator(BuilderCommandGenerator):
    def __init__(self, distro: str, arch: str):
        super().__init__(distro, arch)

    def configure(self) -> typing.List[str]:
        return [
            "cd libressl",
            "./autogen.sh",
            "cd .."
        ]

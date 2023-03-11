# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import typing

from builder.model import BuilderCommandGenerator


class PCRE2BuilderCommandGenerator(BuilderCommandGenerator):
    def __init__(self, distro: str, arch: str):
        super().__init__(distro, arch)

    def configure(self) -> typing.List[str]:
        return [
            "cd pcre2",
            "./autogen.sh",
            "cd .."
        ]

# -*- coding: utf-8 -*-
from package_manager.model import PackageManagerCommandGenerator, PackageManagerVerb


class AptCommandGenerator(PackageManagerCommandGenerator):
    def __init__(self):
        super().__init__("apt", {
            PackageManagerVerb.UPDATE: "update",
            PackageManagerVerb.UPGRADE: "upgrade -y",
            PackageManagerVerb.INSTALL: "install -y",
            PackageManagerVerb.REMOVE: "remove -y"
        })

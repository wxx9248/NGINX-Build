# -*- coding: utf-8 -*-

from package_manager.model import PackageManagerCommandGenerator, PackageManagerVerb


class ApkCommandGenerator(PackageManagerCommandGenerator):
    def __init__(self):
        super().__init__("apk", {
            PackageManagerVerb.UPDATE: "update",
            PackageManagerVerb.UPGRADE: "upgrade",
            PackageManagerVerb.INSTALL: "add",
            PackageManagerVerb.REMOVE: "del"
        })

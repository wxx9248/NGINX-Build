#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
import typing

import docker
from docker.models.containers import Container

import builder.impl
import platform_specific

WORKSPACE_PATH_HOST = "workspace"
WORKSPACE_PATH_CONTAINER = "/workspace"
BUILD_SCRIPT_NAME = "build.sh"
BUILD_SCRIPT_PATH_HOST = f"{WORKSPACE_PATH_HOST}/{BUILD_SCRIPT_NAME}"
BUILD_SCRIPT_PATH_CONTAINER = f"{WORKSPACE_PATH_CONTAINER}/{BUILD_SCRIPT_NAME}"


def main(argc: int, argv: typing.List[str]):
    logger = logging.getLogger()

    logger.debug(f"Current working directory: {os.getcwd()}")

    distro_string = os.environ.get("BUILD_DISTRO")
    arch_string = os.environ.get("BUILD_ARCH")

    logger.debug(f"Build on distro: {distro_string}")
    logger.debug(f"Build on architecture: {arch_string}")

    distro = platform_specific.get_distro_from_string(distro_string)
    arch = platform_specific.get_arch_from_string(arch_string)

    logger.debug("Initializing command generators")
    pm_command_generator = platform_specific.get_distro_pm_command_generator(distro)
    dependencies = platform_specific.get_distro_package_name_dict(distro).values()

    nginx_builder_command_generator = builder.impl.NginxBuilderCommandGenerator(distro, arch)
    pcre2_builder_command_generator = builder.impl.PCRE2BuilderCommandGenerator(distro, arch)
    libressl_builder_command_generator = builder.impl.LibreSSLBuilderCommandGenerator(distro, arch)

    logger.debug("Generating build script")
    command_list = [
        "#!/bin/sh",

        pm_command_generator.update(),
        pm_command_generator.upgrade(),
        pm_command_generator.install(*dependencies),

        # Resolve "dubious ownership" error thrown by git
        "git config --global --add safe.directory '*'"
    ]
    command_list.extend(nginx_builder_command_generator.configure())
    command_list.extend(pcre2_builder_command_generator.configure())
    command_list.extend(libressl_builder_command_generator.configure())
    command_list.extend(nginx_builder_command_generator.build())

    logger.debug(f"Writing build script to file: {BUILD_SCRIPT_PATH_HOST}")
    with open(BUILD_SCRIPT_PATH_HOST, "w") as file:
        file.write("\n".join(command_list))
        file.write('\n')

    tag = platform_specific.get_docker_image_tag(distro, arch)
    logger.info(f"Using docker image: {tag}")

    logger.debug(f"Initializing docker client")
    client = docker.from_env()
    container: Container = client.containers.run(
        distro[0],
        f"sh -e -x ./{BUILD_SCRIPT_NAME}",
        auto_remove=True,
        environment={
            "DEBIAN_FRONTEND": "noninteractive",
            "TZ": "Etc/UTC"
        },
        privileged=True,
        volumes={
            f"{os.getcwd()}/{WORKSPACE_PATH_HOST}": {
                "bind": WORKSPACE_PATH_CONTAINER,
                "mode": "rw"
            }
        },
        working_dir=WORKSPACE_PATH_CONTAINER,
        detach=True,
        platform=f"linux/{arch[0]}" + (f"/{arch[1]}" if arch[1] != "" else "")
    )
    console = container.attach(stdout=True, stderr=True, stream=True, logs=True)
    line: bytes
    for line in console:
        logging.info(line.decode(errors="backslashreplace")[:-1])

    exit_code = container.wait()['StatusCode']
    if exit_code != 0:
        logger.fatal(f"Container exited with non-zero code {exit_code}")
        exit(exit_code)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    main(len(sys.argv), sys.argv)

# -*- coding: utf-8 -*-
import re
import typing

from builder.model import BuilderCommandGenerator

CONFIGURE_COMMAND = "./auto/configure"

CONFIGURE_FLAGS_COMMON = [
    "--with-threads",
    "--with-file-aio",

    "--with-http_ssl_module",
    "--with-http_v2_module",
    "--with-http_realip_module",
    "--with-http_addition_module",
    "--with-http_xslt_module",
    "--with-http_image_filter_module",
    "--with-http_geoip_module",
    "--with-http_sub_module",
    "--with-http_dav_module",
    "--with-http_flv_module",
    "--with-http_mp4_module",
    "--with-http_gunzip_module",
    "--with-http_gzip_static_module",
    "--with-http_auth_request_module",
    "--with-http_random_index_module",
    "--with-http_secure_link_module",
    "--with-http_degradation_module",
    "--with-http_slice_module",
    "--with-http_stub_status_module",

    "--with-mail",
    "--with-mail_ssl_module",

    "--with-stream",
    "--with-stream_ssl_module",
    "--with-stream_realip_module",
    "--with-stream_geoip_module",
    "--with-stream_ssl_preread_module",

    "--add-module=../nginx-http-auth-digest",
    "--add-module=../ngx_brotli",
    "--add-module=../njs/nginx",

    "--with-compat",

    "--with-pcre",
    "--with-pcre=../pcre2",
    "--with-pcre-jit",

    "--with-zlib=../zlib",

    "--with-openssl=../libressl"
]

CONFIGURE_FLAGS_EXTRA = {
    (r"focal|jammy", r".*"): [
        "--prefix=/etc/nginx",
        "--sbin-path=/usr/sbin/nginx",
        "--modules-path=/usr/lib/nginx/modules",
        "--conf-path=/etc/nginx/nginx.conf",
        "--error-log-path=/var/log/nginx/error.log",
        "--pid-path=/var/run/nginx.pid",
        "--lock-path=/var/run/nginx.lock",

        "--user=nginx",
        "--group=nginx",

        "--http-log-path=/var/log/nginx/access.log",
        "--http-client-body-temp-path=/var/cache/nginx/client_temp",
        "--http-proxy-temp-path=/var/cache/nginx/proxy_temp",
        "--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp",
        "--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp",
        "--http-scgi-temp-path=/var/cache/nginx/scgi_temp",

        "--with-cc-opt='-g -O2 -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC'",
        "--with-ld-opt='-Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'"
    ],
    (r"archlinux", r".*"): [
        "--prefix=/etc/nginx",
        "--sbin-path=/usr/bin/nginx",
        "--modules-path=/usr/lib/nginx/modules",
        "--conf-path=/etc/nginx/nginx.conf",
        "--error-log-path=stderr",
        "--pid-path=/run/nginx.pid",
        "--lock-path=/run/lock/nginx.lock",

        "--user=http",
        "--group=http",

        "--http-log-path=/var/log/nginx/access.log",
        "--http-client-body-temp-path=/var/lib/nginx/client_body",
        "--http-proxy-temp-path=/var/lib/nginx/proxy",
        "--http-fastcgi-temp-path=/var/lib/nginx/fastcgi",
        "--http-uwsgi-temp-path=/var/lib/nginx/uwsgi",
        "--http-scgi-temp-path=/var/lib/nginx/scgi",

        # "--with-cc-opt=",
        # "--with-ld-opt="
    ],
    (r"archlinux", r"amd64"): [
        "--with-cc-opt='-march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -flto'",
        "--with-ld-opt='-Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now -flto'"
    ],
    (r"archlinux", r"aarch64"): [
        "--with-cc-opt='-march=armv8-a -O2 -pipe -fstack-protector-strong -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection'",
        "--with-ld-opt='-Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now'"
    ],
    (r"alpine", r".*"): [
        "--prefix=/var/lib/nginx",
        "--sbin-path=/usr/sbin/nginx",
        "--modules-path=/usr/lib/nginx/modules",
        "--conf-path=/etc/nginx/nginx.conf",
        # "--error-log-path=",
        "--pid-path=/run/nginx/nginx.pid",
        "--lock-path=/run/nginx/nginx.lock",

        "--user=nginx",
        "--group=nginx",

        # "--http-log-path=",
        "--http-client-body-temp-path=/var/lib/nginx/tmp/client_body",
        "--http-proxy-temp-path=/var/lib/nginx/tmp/proxy",
        "--http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi",
        "--http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi",
        "--http-scgi-temp-path=/var/lib/nginx/tmp/scgi",

        # "--with-cc-opt=",
        # "--with-ld-opt="
    ],
}


class NginxBuilderCommandGenerator(BuilderCommandGenerator):
    def __init__(self, distro: str, arch: str):
        super().__init__(distro, arch)

    def configure(self) -> typing.List[str]:
        matched_extra = [
            value
            for (regex_distro, regex_arch), value in CONFIGURE_FLAGS_EXTRA.items()
            if re.match(regex_distro, self.distro) and re.match(regex_arch, self.arch)
        ]

        configure_command_list = [CONFIGURE_COMMAND]
        configure_command_list.extend(CONFIGURE_FLAGS_COMMON)
        configure_command_list.extend([item for sublist in matched_extra for item in sublist])

        return [
            "cd nginx",
            " ".join(configure_command_list),
            "cd .."
        ]

    def build(self) -> typing.List[str]:
        return [
            "cd nginx",
            "make -j$(nproc)",
            "strip --strip-unneeded objs/nginx",
            "cd .."
        ]

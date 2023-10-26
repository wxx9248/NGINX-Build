import functools


def main():
    compare_all()
    #compare_archlinux()


def compare_archlinux():
    common = functools.reduce(lambda a, b: a.intersection(b), split_parameter_dict.values())
    amd64 = split_parameter_dict["archlinux-amd64"] - common
    aarch64 = split_parameter_dict["archlinux-aarch64"] - common

    common = amd64.intersection(aarch64)
    common_list = list(common)
    common_list.sort()
    print("common.py")
    [print(f"\"{item}\",") for item in common_list]
    print()

    for (key, value) in {"amd64": amd64, "aarch64": aarch64}.items():
        value_list = list(value - common)
        value_list.sort()
        print(key)
        [print(f"\"{item}\",") for item in value_list]
        print()


def compare_all():
    common = functools.reduce(lambda a, b: a.intersection(b), split_parameter_dict.values())
    common_list = list(common)
    common_list.sort()
    print("common.py")
    [print(f"\"{item}\",") for item in common_list]
    print()

    for (key, value) in split_parameter_dict.items():
        value_list = list(value - common)
        value_list.sort()
        print(key)
        [print(f"\"{item}\",") for item in value_list]
        print()


def split_option(s: str):
    l = s.split(" ")

    pos = 0
    start_quote = None
    combine = []
    combine_start_pos = 0
    combine_end_pos = 0
    while pos < len(l):
        if "'" in l[pos]:
            quote = "'"
        elif '"' in l[pos]:
            quote = '"'
        else:
            quote = None

        if start_quote is None:
            combine_start_pos = pos
            start_quote = quote
        elif start_quote == quote:
            combine_end_pos = pos + 1
            combine.append((combine_start_pos, combine_end_pos))
            start_quote = None

        pos += 1

    combined = []
    pos = 0
    for (start, end) in combine:
        if pos < start:
            combined.extend(l[:start])
            pos = start

        if pos == start:
            combined.append(" ".join(l[start:end]))
            pos = end
    combined.extend(l[pos:])

    return combined


parameter_dict = {
    "ubuntu-focal-amd64": r"--prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-pcre-jit --with-http_geoip_module --with-http_flv_module --with-http_image_filter_module --with-http_mp4_module --with-stream_geoip_module --add-module=../ngx_brotli --add-module=../ngx-fancyindex --add-module=../nginx-http-auth-digest --add-module=../njs/nginx --add-module=../nginx-rtmp-module --with-openssl=../libressl --with-pcre=../pcre2 --with-zlib=../zlib --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'",
    "ubuntu-focal-aarch64": r"--prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-pcre-jit --with-http_geoip_module --with-http_flv_module --with-http_image_filter_module --with-http_mp4_module --with-stream_geoip_module --add-module=../ngx_brotli --add-module=../ngx-fancyindex --add-module=../nginx-http-auth-digest --add-module=../njs/nginx --add-module=../nginx-rtmp-module --with-openssl=../libressl --with-pcre=../pcre2 --with-zlib=../zlib --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'",
    "ubuntu-jammy-amd64": r"--prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-pcre-jit --with-http_geoip_module --with-http_flv_module --with-http_image_filter_module --with-http_mp4_module --with-stream_geoip_module --add-module=../ngx_brotli --add-module=../ngx-fancyindex --add-module=../nginx-http-auth-digest --add-module=../njs/nginx --add-module=../nginx-rtmp-module --with-openssl=../libressl --with-pcre=../pcre2 --with-zlib=../zlib --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'",
    "ubuntu-jammy-aarch64": r"--prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-pcre-jit --with-http_geoip_module --with-http_flv_module --with-http_image_filter_module --with-http_mp4_module --with-stream_geoip_module --add-module=../ngx_brotli --add-module=../ngx-fancyindex --add-module=../nginx-http-auth-digest --add-module=../njs/nginx --add-module=../nginx-rtmp-module --with-openssl=../libressl --with-pcre=../pcre2 --with-zlib=../zlib --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'",
    "archlinux-amd64": r"--prefix=/etc/nginx --conf-path=/etc/nginx/nginx.conf --sbin-path=/usr/bin/nginx --pid-path=/run/nginx.pid --lock-path=/run/lock/nginx.lock --user=http --group=http --http-log-path=/var/log/nginx/access.log --error-log-path=stderr --http-client-body-temp-path=/var/lib/nginx/client_body --http-proxy-temp-path=/var/lib/nginx/proxy --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-cc-opt='-march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -flto' --with-ld-opt='-Wl,-O1,--sort-common.py,--as-needed,-z,relro,-z,now -flto' --with-compat --with-debug --with-file-aio --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_degradation_module --with-http_flv_module --with-http_geoip_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-pcre-jit --with-stream --with-stream_geoip_module --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-threads --modules-path=/usr/lib/nginx/modules --with-http_image_filter_module --with-http_random_index_module --add-module=../ngx_brotli --add-module=../ngx-fancyindex --add-module=../nginx-http-auth-digest --add-module=../njs/nginx --add-module=../nginx-rtmp-module --with-openssl=../libressl --with-pcre=../pcre2 --with-zlib=../zlib",
    "archlinux-aarch64": r"--prefix=/etc/nginx --conf-path=/etc/nginx/nginx.conf --sbin-path=/usr/bin/nginx --pid-path=/run/nginx.pid --lock-path=/run/lock/nginx.lock --user=http --group=http --http-log-path=/var/log/nginx/access.log --error-log-path=stderr --http-client-body-temp-path=/var/lib/nginx/client_body --http-proxy-temp-path=/var/lib/nginx/proxy --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-cc-opt='-march=armv8-a -O2 -pipe -fstack-protector-strong -fno-plt -D_FORTIFY_SOURCE=2' --with-ld-opt=-Wl,-O1,--sort-common.py,--as-needed,-z,relro,-z,now --with-compat --with-debug --with-file-aio --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_degradation_module --with-http_flv_module --with-http_geoip_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-pcre-jit --with-stream --with-stream_geoip_module --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-threads --modules-path=/usr/lib/nginx/modules --with-http_image_filter_module --with-http_random_index_module --add-module=../ngx_brotli --add-module=../ngx-fancyindex --add-module=../nginx-http-auth-digest --add-module=../njs/nginx --add-module=../nginx-rtmp-module --with-openssl=../libressl --with-pcre=../pcre2 --with-zlib=../zlib",
}

split_parameter_dict = {
    key: set(split_option(value))
    for key, value in parameter_dict.items()
}

if __name__ == "__main__":
    main()

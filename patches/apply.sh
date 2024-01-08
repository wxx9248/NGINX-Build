# LibreSSL OpenBSD codebase branch fix
echo libressl-v3.8.2 >workspace/libressl/OPENBSD_BRANCH

# https://github.com/nginx/njs/issues/684
patch workspace/njs/external/njs_xml_module.c patches/njs.issue.684.patch

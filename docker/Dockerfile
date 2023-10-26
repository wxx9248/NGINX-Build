FROM nginx:1.25.3-alpine
LABEL maintainer="wxx9248 <wxx9248@wxx9248.top>"
ARG TARGETARCH
ARG TARGETVARIANT

RUN apk add --update --no-cache gd geoip libxml2 libxslt
RUN --mount=type=bind,target=/build /build/install.sh $TARGETARCH $TARGETVARIANT
RUN mkdir -p /var/lib/nginx/logs /var/lib/nginx/tmp /run/nginx

FROM golang:latest as go_compiler

RUN mkdir /app
WORKDIR /app
ADD https://raw.githubusercontent.com/kubernetes/kubernetes/master/test/images/apparmor-loader/loader.go loader.go
RUN go mod init loader
RUN go get k8s.io/klog/v2
RUN GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -a -installsuffix cgo --ldflags '-w' -o loader .

FROM alpine:latest

RUN apk add apparmor libapparmor --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ --allow-untrusted && \
    apk add --no-cache musl\>1.1.20 --repository http://dl-cdn.alpinelinux.org/alpine/edge/main/

COPY --from=go_compiler /app/loader /usr/bin/loader

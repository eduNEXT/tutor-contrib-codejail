FROM golang:latest AS go_compiler

RUN mkdir /app
WORKDIR /app
ADD https://raw.githubusercontent.com/kubernetes/kubernetes/master/test/images/apparmor-loader/loader.go loader.go
RUN go mod init loader
RUN go get k8s.io/klog/v2
RUN GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -a -installsuffix cgo --ldflags '-w' -o loader .

FROM alpine:3.20

RUN apk add apparmor libapparmor --update-cache

COPY --from=go_compiler /app/loader /usr/bin/loader

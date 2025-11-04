FROM golang:1.25.4 AS go_compiler

RUN mkdir /app
WORKDIR /app
ADD https://raw.githubusercontent.com/kubernetes/kubernetes/a9593d634c6a053848413e600dadbf974627515f/test/images/apparmor-loader/loader.go loader.go
RUN go mod init loader
RUN go get k8s.io/klog/v2
RUN GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -a -installsuffix cgo --ldflags '-w' -o loader .

FROM alpine:3.22

RUN apk add apparmor libapparmor --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main
COPY --from=go_compiler /app/loader /usr/bin/loader


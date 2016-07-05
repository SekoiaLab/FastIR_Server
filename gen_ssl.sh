#!/bin/bash

openssl req \
       -newkey rsa:2048 -nodes -keyout ./certificate/server.key \
       -x509 -days 365 -out ./certificate/server.crt
#openssl x509 -noout -modulus -in server.crt | sed "s/Modulus=//g" > server.pub
openssl asn1parse -dump -in ./certificate/server.crt > ./certificate/server.pub



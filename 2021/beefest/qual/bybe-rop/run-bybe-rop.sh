#!/bin/bash

gcc bybe-rop.c -fno-stack-protector -no-pie -o bybe-rop
socat TCP-LISTEN:7778,reuseaddr,fork EXEC:"./bybe-rop"

#!/bin/bash

gcc map_me.c -fstack-protector -o map_me
socat TCP-LISTEN:7777,reuseaddr,fork EXEC:"./map_me"

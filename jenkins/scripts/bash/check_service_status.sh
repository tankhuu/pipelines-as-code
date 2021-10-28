#!/bin/bash -xe

sudo systemctl is-active $(cat /tmp/service_list.txt)
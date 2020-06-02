#!/bin/bash

sudo docker rm -f "tv-controller"

sudo docker run -dit --restart='always' \
--name 'tv-controller' \
--network host \
tv-controller
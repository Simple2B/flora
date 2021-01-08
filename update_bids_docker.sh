#!/bin/bash

FULL_PATH=$(realpath $0)
# echo $FULL_PATH
DIR_PATH=$(dirname $FULL_PATH)
# echo $DIR_PATH
cd $DIR_PATH

flask update-bids 2>> /usr/src/app/update-bids.log

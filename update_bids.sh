#!/bin/bash
# echo $0

FULL_PATH=$(realpath $0)
# echo $FULL_PATH
DIR_PATH=$(dirname $FULL_PATH)
# echo $DIR_PATH
cd $DIR_PATH
source .venv/bin/activate
flask update-bids 2>> /tmp/update-bids.log

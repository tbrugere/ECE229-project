#!/bin/bash

: "${SERVER:=ec2-34-222-231-189.us-west-2.compute.amazonaws.com}" 
#note that my ssh/config takes care of the rest

: "${REPO:=https://github.com/nephanth/ECE229-project.git}"
#note that to clone with ssh, you got to have 

: "${DEPLOYBRANCH:=deploy}"

DIRNAME=ECE229

ssh "$SERVER" << EOF
    set -x
    if [ ! -d "$DIRNAME" ]; then
        git clone "$REPO" --depth 1 -b "$DEPLOYBRANCH" --single-branch "$DIRNAME"
    fi

    cd "$DIRNAME"
    git fetch $REPO $DEPLOYBRANCH
    git reset --hard FETCH_HEAD
    git clean -df

    make local-deploy
    
    sudo make install-unit
    sudo systemctl daemon-reload
    sudo systemctl restart carsreco

    set +x
EOF


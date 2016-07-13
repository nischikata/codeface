#!/bin/bash
# Copyright Matthias Dittrich <matthi.d@gmail.com>
# SPDX-License-Identifier:	Apache-2.0 BSD-2-Clause GPL-2.0+ MIT WTFPL

CFCONF="/mnt/codeface-data/configurations/codeface_testing_ext.conf"

cd "id_service"
nodejs id_service.js ${CFCONF} 2>&1 > cluster.log &
node_job=$!
cd ..

codeface test -c ${CFCONF}
codeface_exit=$?
kill $node_job
exit $codeface_exit

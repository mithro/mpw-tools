#!/usr/bin/env python3
# Copyright 2020-2023 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import csv
import os
import subprocess
import argparse
import sys

def usage():
    print('check_manifest.py')


if __name__ == '__main__':
    debug = False

#manifest_file = "{0}/{1}/foundry/manifest-{1}.csv".format(os.environ["TAPEOUT_ROOT"], os.environ["SHUTTLE"])
manifest_file = sys.argv[1]

with open( manifest_file, "r" ) as f:
    reader = csv.reader(f, delimiter=",", skipinitialspace=True)
    for i, line in enumerate(reader):
        if i != 0 and line[2] != 'TEST':
            if os.path.splitext(line[10].split('>')[1])[1] == '.gz':
                # p3 = subprocess.Popen( "gunzip -c", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True  )
                p2 = subprocess.Popen( "gunzip -c | shasum", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True  )
                p1 = subprocess.Popen( line[10].split('>')[0], stdout=p2.stdin, stderr=subprocess.PIPE, shell=True )
            else:
                p2 = subprocess.Popen( "shasum", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True  )
                p1 = subprocess.Popen( line[10].split('>')[0], stdout=p2.stdin, stderr=subprocess.PIPE, shell=True )
            stdout, stderr = p2.communicate()
            output = stdout.decode('utf-8')
            if output:
                hash = output.split(' ')[0]
            if hash == line[9]:
                check = '-- Matched-- '
            else:
                check = '** Error **'

            print("{:02}:  slot = {}, project = {:<15}, id = {}, shasum = {} | {}".format(i, line[1], line[2][:15], line[3][1:], line[9], check))







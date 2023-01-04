#!/usr/bin/env python3
# Copyright 2022-2023 SkyWater PDK Authors
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

import base64
import json
import os
import pprint
import urllib.request
import yaml


def download(url, out):
    fn, headers = urllib.request.urlretrieve(url)
    with open(out, 'wb') as f:
        f.write(base64.b64decode(open(fn, 'rb').read()))
    os.unlink(fn)


URL = 'https://foss-eda-tools.googlesource.com/third_party/shuttle/sky130/mpw-%03i/slot-%03i/+/refs/heads/main/info.yaml?format=TEXT'
OUT = 'mpw-%03i_slot-%03i_info.yml'

def mpw_and_slots():
    for mpw in range(1, 8):
        for slot in range(1, 40+1):
            yield mpw, slot


def main(args):
    data = {}
    for mpw, slot in mpw_and_slots():
        if mpw not in data:
            data[mpw] = {}

        o = OUT % (mpw, slot)
        if os.path.exists(o):
            data[mpw][slot] = yaml.safe_load(open(o, 'r'))
            continue
        if os.path.exists('.'+o):
            continue
        u = URL % (mpw, slot)
        print('Downloading', u, 'to', o)
        try:
            download(u, o)
        except urllib.error.HTTPError as e:
            print(e)
            with open('.'+o, 'w') as f:
                f.write(str(e))
            continue
        data[mpw][slot] = yaml.safe_load(open(o, 'r'))

    pprint.pprint(data)

    with open('summary.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent='  ')


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))

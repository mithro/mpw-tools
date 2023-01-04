#!/bin/bash
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

#echo SHUTTLE=$SHUTTLE
#echo SHUTTLE_ROOT=$SHUTTLE_ROOT
#echo TAPEOUT_ROOT=$TAPEOUT_ROOT
#echo SHUTTLE_PREFIX=$SHUTTLE_PREFIX

set -a
usage() { echo "Usage: $0 [ -n ] <start> <end> <projects.csv>" 1>&2; exit 1; }

preview=false
use_master=false
while getopts "mns:" o; do
    case "${o}" in
        n)
            preview=true
            ;;
        m)
            use_master=true
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [[ -z "$1" || -z "$2" || -z "$3" ]]; then usage; fi
start=$1
stop=$2
user_projects=$3

home_dir="$SHUTTLE_ROOT"
echo; echo "##### Getting layout images for projects $1 to $2...  SHUTTLE_PREFIX=$SHUTTLE_PREFIX #####"; echo
cd $home_dir || exit
#for i in `seq -f "%03g" $1 $2`;
while IFS=, read -r i user_id project stuff
do
  if [[ $i -lt $start ]] || [[ $i -gt $stop ]] || [[ -z ${user_id} ]] || [[ ${user_id} == 'N' ]]; then continue; fi

#  target_path=${TAPEOUT_ROOT}/shuttle/${SHUTTLE}/$slot/$project
  echo "Getting project image $user_id | $project ..."

  get_layout_image_user.sh $user_id $project

	cd $home_dir || exit

done < $user_projects

echo "Done."

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

user_id=${1};
#project=${2}; project=$( find /mnt/uffs/user/${user_id}/design/${project}* -maxdepth 0 -type d); project=$(basename $project)
project=${2};

cd ${SHUTTLE_ROOT}/${user_id}/${project}/

source ${SAK}/set_open_mpw.sh

#project=`basename $(pwd)`
#parent_dir=`dirname $(pwd)`
#slot=`basename $parent_dir`
#slot_value=${slot:5}
#user_id=$(expr $slot_value + 65536)
#user_id_hex=`printf "%08x" $user_id`
#user_id_hex=$(python3 /mnt/share/open_mpw/sak/get_user_id.py)

#[ -f "./info.yaml" ] || { echo "** error: info.yaml not found" ; exit 2 ; }
#export USER_ID=$(get_user_id.py)
#proj_type=$(get_project_type.py)
#if [ -f ${project_path}/gds/user_project_wrapper.gds.gz ] || [ -f ${project_path}/gds/user_project_wrapper.gds.gz.00.split ] || [ -f ${project_path}/gds/user_project_wrapper.gds ] ; then
#  proj_type="digital"
#elif [ -f ${project_path}/gds/user_analog_project_wrapper.gds.gz ] || [ -f ${project_path}/gds/user_analog_project_wrapper.gds.gz.00.split ] || [ -f ${project_path}/gds/user_analog_project_wrapper.gds ]; then
#  proj_type="analog"
#fi

#    if [ ! -f ./gds/${final_gds} ] && [ ! -f ./gds/${final_gz} ] ; then
#      final_gz="caravel_${user_id_hex}.gds.gz.00.split"
#      final_cnt=$( ls ./gds/caravel_${user_id_hex}.gds.gz.??.split 2> /dev/null | wc -l )
#      if [ $final_cnt -eq 0 ]; then
#        final_gz=""
#      fi
#    fi


#if [ $proj_type == "analog" ]; then
#  gds_file="./gds/caravan.gds"
#  png_file="./signoff/caravan.png"
#  [ -f "$gds_file" ] || { [ -f "./gds/caravan.gds.gz" ] && gds_file="./gds/caravan.gds.gz" ; } \
#    || { [ -f "./gds/caravan.gds.xy" ] && gds_file="./gds/caravan.gds.xz" ; }
#else
#  gds_file="./gds/caravel.gds"
#  png_file="./signoff/caravel.png"
#  [ -f "$gds_file" ] || { [ -f "./gds/caravel.gds.gz" ] && gds_file="./gds/caravel.gds.gz" ; } \
#    || { [ -f "./gds/caravel.gds.xy" ] && gds_file="./gds/caravel.gds.xz" ; }
#fi

if [ $PDK == "gf180mcuC" ]; then
  input_file="tapeout/outputs/gds/$( basename $(find tapeout/outputs/gds/* -maxdepth 0 -type f ) )"
else
  input_file="tapeout/outputs/oas/$( basename $(find tapeout/outputs/oas/* -maxdepth 0 -type f ) )"
fi

png_file="./signoff/caravel_layout.png"
assigned_slot=$(cat "signoff/assigned_slot" )

echo $input_file

xvfb-run -e /dev/stderr klayout -z -rd input_layout=$input_file \
          -rd output_image=${png_file} \
          -rm $SAK/scrotLayout.py

#          -rd tech_file=$SAK/../klayout/tech/sky130A/sky130A.lyt \
#          -nn $SAK/get_image_sky130A.lyt \
#          -l $SAK/get_image_sky130A.lyp \
#          -rm $SAK/scrotLayout.py \
#          -c $SAK/get_image_klayoutrc

#          -nn $SAK/../klayout/tech/sky130A/sky130A.lyt \
#          -l $SAK/../klayout/tech/sky130A/sky130A-user_review.lyp \

#          -c $SAK/get_image_klayoutrc

#          -c $SAK/../klayout/tech/sky130A/sky130A.krc
#          -nn $SAK/../klayout/tech/sky130A/sky130A.lyt
#          -l $SAK/../klayout/tech/sky130A/sky130A.lyp

#python3 ${SAK}/set_info.py layout_image ${png_file}

post_file_to_slack.sh -m "Layout for ${SHUTTLE}, slot $assigned_slot -- $user_id : $project" ${png_file}


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

import pya

WIDTH = 2048
HEIGHT = 2048

app = pya.Application.instance()
win = app.main_window()


# Load def file in the main window
cell_view = win.load_layout(input_layout, 0)
layout_view = cell_view.view()
layout_view.grid_visible = False

layout_view.max_hier()

# Choose layers with these purposes
visible_purposes = [20]
visible_layers = [ 68, 69, 70, 71, 72 ]

li = layout_view.begin_layers()
while not li.at_end():
    lp = li.current()
    new_lp = lp.dup()
    if (lp.source_datatype in visible_purposes) and (lp.source_layer in visible_layers):
        print("layer {} / {} : on".format(lp.source_layer, lp.source_datatype))
        new_lp.visible = True
    else:
        print("layer {} / {} : off".format(lp.source_layer, lp.source_datatype))
        new_lp.visible = False
    layout_view.set_layer_properties(li, new_lp)

    li.next()

layout_view.save_image(output_image, WIDTH, HEIGHT)
app.exit(0)

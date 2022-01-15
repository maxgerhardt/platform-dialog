# Copyright 2022 Maximlian Gerhardt <maximilian.gerhardt@rub.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import os
import string
from os.path import join, isdir

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
mcu = board.get("build.mcu", "")
cmsis_series = board.get("build.cmsis_series", "")

CMSIS_DIR = platform.get_package_dir("framework-cmsis-dialog")
CMSIS_DEVICE_DIR = join(CMSIS_DIR, "dialog", cmsis_series)
LDSCRIPTS_DIR = join(CMSIS_DIR, "platformio", "ldscripts")
assert all(isdir(d) for d in (CMSIS_DIR, CMSIS_DEVICE_DIR, LDSCRIPTS_DIR))

def get_linker_script():
    default_ldscript = os.path.join(LDSCRIPTS_DIR, "%s.ld" % cmsis_series)

    if not os.path.isfile(default_ldscript):
        print("Warning! Cannot find a linker script for the required board!")
        env.Exit(-1)
    return default_ldscript

#
# Allow using custom linker scripts
#

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=get_linker_script())

env.Append(
    CPPPATH=[
        #os.path.join(CMSIS_DIR, "CMSIS", "Include"),
        os.path.join(CMSIS_DEVICE_DIR, "inc")
    ],
    LINKFLAGS=[
        "--specs=nano.specs",
        "--specs=nosys.specs"
    ]
)

sources_path = os.path.join(CMSIS_DEVICE_DIR, "src")

env.BuildSources(
    os.path.join("$BUILD_DIR", "FrameworkCMSIS"), 
    sources_path,
    #src_filter=[]
)
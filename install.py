#!/usr/bin/env python

# Beware:
#  - this script is executed using the system's python, so with not easy control on which
#    packages are available. Same, we cannot directly install new ones using pip.
#  - the role of the first stage of this installer is just to install a fresh new virtualenv
#    with a *controled* version of python, pip and virtualenv, and launch the second part of
#    the installer, 'install-stage2.py', which will run in the virtualenv.

# Note:
#  - This script should execute transparently in an Python > 2.7 or Python > 3.4 without any
#    additional packages

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import imp
import os
import shutil

g_prefix = None
g_src_dir = os.path.abspath(os.path.dirname(__file__))

# Injecting available targets from installer stage 2
lib = imp.load_source('install-lib.py',
                      os.path.join(os.path.dirname(__file__), "install-lib.py"))


def copyFile(relativeSrcPath, relativeDestPath):
    lib.printInfo("Copying {} to {}".format(relativeSrcPath, relativeDestPath))
    src_full_path = os.path.join(g_src_dir, relativeSrcPath)
    src_file_name = os.path.basename(relativeSrcPath)
    dst_full_path = os.path.join(g_prefix, relativeDestPath)
    lib.printDebug("Src full path: {}".format(src_full_path))
    lib.printDebug("Src file path: {}".format(src_file_name))
    lib.printDebug("Dst full path: {}".format(dst_full_path))
    dst_dir = os.path.dirname(dst_full_path)
    lib.makedirs(dst_dir)
    shutil.copy(src_full_path, dst_full_path)
    lib.printDebug("{} -> {}".format(relativeSrcPath, dst_full_path))


parser = lib.addArgumentParser(description="Install Guake on your system")
parser.add_option("--dev", action="store_true", help="install virtualenv")
(options, args) = lib.parse(parser)

lib.printSeparator("=")
lib.printInfo("Guake Installation")
lib.printSeparator("=")
lib.printDebug("Options: options: {!r}".format(options))
lib.printDebug("Args: args: {!r}".format(args))

dest_path = options.prefix
virtualenv_dest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "workdir"))
if os.environ.get("VIRTUAL_ENV"):
    lib.printInfo("Already in a virtual env, installing it inside this virtualenv")
    lib.printInfo("Installation in: {}".format(virtualenv_dest_path))
    dest_path = virtualenv_dest_path
elif options.dev:
    dest_path = virtualenv_dest_path
    lib.run(["virtualenv", "workdir"])
    if lib.isMacOsX or lib.isLinux:
        lib.run(["ln", "-s", os.path.join("workdir", "bin", "activate")])
else:
    lib.printInfo("Installation in: {}".format(dest_path))

dataFolder = "data"

lib.execute("pip install --upgrade pip")
lib.execute("pip install -r requirements.txt")
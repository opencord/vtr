#!/usr/bin/env python

# This imports and runs ../../xos-observer.py

import importlib
import os
import sys

from xosconfig import Config
Config.init('/opt/xos/synchronizers/vtr/vtr_config.yaml', 'synchronizer-config-schema.yaml')

observer_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"../../synchronizers/new_base")
sys.path.append(observer_path)
mod = importlib.import_module("xos-synchronizer")
mod.main()

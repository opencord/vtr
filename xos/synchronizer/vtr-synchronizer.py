#!/usr/bin/env python

# This imports and runs ../../xos-observer.py

import importlib
import os
import sys

from xosconfig import Config
config_file = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/vtr_config.yaml')

Config.init(config_file, 'synchronizer-config-schema.yaml')
observer_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../synchronizers/new_base")

# observer_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../xos/xos/synchronizers/new_base")
# sys.path.append('/Users/teone/Sites/opencord/orchestration/xos/xos')

sys.path.append(observer_path)
mod = importlib.import_module("xos-synchronizer")
mod.main()

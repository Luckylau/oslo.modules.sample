#!/usr/bin/env python
#
# Copyright 2016 luckylau <laujunbupt0913@163.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from oslo_config import cfg
from oslo_log import log as logging

def logname(name):
    return logging.getLogger(name)

def rpc_log_prepare(DOMAIN):
    logging.register_options(cfg.CONF)
    extra_log_level_defaults=[
        'dogpile=INFO',
        'routes=INFO'
    ]
    logging.set_defaults(default_log_levels=logging.get_default_log_levels()+extra_log_level_defaults)
    logging.setup(cfg.CONF,DOMAIN)
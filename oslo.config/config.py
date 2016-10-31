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


def configExample():
    CONF = None
    # option 1: A single configuration mode
    enable_api = cfg.ListOpt('enable_api',
                             default=['neutron_api'],
                             help='List of APIs to enable by default .')
    # option 2:A pattern contains multiple configuration items
    common_opts = [
        cfg.StrOpt('bind_host', default='0.0.0.0',
                   help='IP address to listen on'),
        cfg.IntOpt('bind_port',
                   default=22,
                   help='Port to listen on.')
    ]
    # option 3: Configuration group
    rabbit_group = cfg.OptGroup(
        name='Rabbit',
        title="RabbitMQ options"
    )
    rabbit_ssl_opt = cfg.BoolOpt('ssl_opt', default=False,
                                 help='use ssl to connection')
    rabbit_opts = [
        cfg.StrOpt('host',
                   default='localhost',
                   help='IP/hostname to listen on.'),
        cfg.IntOpt('port',
                   default=5672,
                   help='Port number to listen on.')
    ]
    rabbit_users = [

        cfg.StrOpt('user_name',
                   default=' ',
                   help='user name .'),
        cfg.StrOpt('password',
                   default=' ',
                   help='password .')
    ]

    CONF = cfg.CONF
    CONF.register_opt(enable_api)

    CONF.register_opts(common_opts)

    CONF.register_group(rabbit_group)
    CONF.register_opts(rabbit_opts, rabbit_group)
    CONF.register_opt(rabbit_ssl_opt, rabbit_group)
    CONF.register_opts(rabbit_users, rabbit_group)
    return CONF


def getargs():
    print ("Tips:\n press '1' means do not load my.conf \n"
           " press '2' means load my.conf")
    options = raw_input("Options: ")
    if str(options) is not "1" and options is not "2":
        print ("Input error ,please choose 1 or 2")
        exit()
    return options


def printInfo(config):
    print ("enabled_api: ")
    for i in config.enable_api:
        print (" " + i)

    print("bind_host: " + config.bind_host)
    print ("bind_port: " + str(config.bind_port))
    print("rabbit.ssl_opt: " + str(config.Rabbit.ssl_opt))
    print("rabbit.host: " + config.Rabbit.host)
    print("rabbit.port: " + str(config.Rabbit.port))
    print("rabbit.user_name: " + config.Rabbit.user_name)
    print("rabbit.password: " + str(config.Rabbit.password))


def main():
    options = getargs()
    config = configExample()
    if options == "1":
        config()
        printInfo(config)

    else:
        config(default_config_files=['my.conf'])
        printInfo(config)

if __name__ == '__main__':
    main()

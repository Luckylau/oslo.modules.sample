#!/usr/bin/env python
#
# Copyright 2016 zhangtonghao <nickcooper-zhangtonghao@opencloud.tech>
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
import optparse
import sys
import time

from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging as messaging

LOG = logging.getLogger(__name__)

class TestEndpoint(object):
    def __init__(self, server, target=None):
        self.server = server
        self.target = target

    def sink(self, ctx, **args):
        LOG.info("%s::TestEndpoint:sink(ctxt=%s arg=%s) called"
                % (self.server, str(ctx),str(args)))

    def echo(self, ctx, **args):
        LOG.info("%s::TestEndpoint::echo(ctxt=%s arg=%s) called"
                % (self.server, str(ctx),str(args)))
        return {"method":"echo", "context":ctx, "args":args}

    def sleep(self, ctx, **args):
        LON.info("%s::TestEndpoint::sleeps(ctxt=%s arg=%s) called. sleeping..."
                % (self.server, str(ctx),str(args)))
        time.sleep(float(args.get("timeout", 10.0)))
        LON.info("awake!")

def rpc_log_init():
    logging.register_options(cfg.CONF)
    extra_log_level_defaults = [
            'dogpile=INFO',
            'routes=INFO']
    logging.set_defaults(
            default_log_levels=logging.get_default_log_levels() +
            extra_log_level_defaults)
    logging.setup(cfg.CONF, "rpc-server")

def main(argv=None):
    _usage = """Usage: %prog [options] <server name>"""
    parser = optparse.OptionParser(usage=_usage)
    parser.add_option("--topic", action="store", default="my-topic",
                      help="target topic, default 'my-topic'")
    parser.add_option("--exchange", action="store", default="my-exchange",
                      help="target exchange, default 'my-exchange'")
    parser.add_option("--namespace", action="store", default="my-namespace",
                      help="target namespace, default 'my-namespace'")
    parser.add_option("--version", action="store", default="1.1",
                      help="target version, default '1.1'")
    parser.add_option("--url", action="store", default="rabbit://localhost",
                      help="transport address, default 'rabbit://localhost'")
    parser.add_option("--executor", action="store", default="blocking",
                      help="defaults to 'blocking'")
    parser.add_option("--oslo-config", type="string",
                      help="the oslo.messaging configuration file.")

    opts, extra = parser.parse_args(args=argv)
    if not extra:
        print("<server-name> not supplied!")
        return False

    server_name = extra[0]
    rpc_log_init()
    LOG.info("Running server, name=%s exchange=%s topic=%s namespace=%s"
          % (server_name, opts.exchange, opts.topic, opts.namespace))

    if opts.oslo_config:
        LOG.info("Loading config file %s" % opts.oslo_config)
        cfg.CONF(["--config-file", opts.oslo_config])

    transport = messaging.get_transport(cfg.CONF, url=opts.url)

    target = messaging.Target(exchange=opts.exchange,
            topic=opts.topic,
            namespace=opts.namespace,
            server=server_name,
            version=opts.version)

    server = messaging.get_rpc_server(transport, target,
            [TestEndpoint(server_name, target)],
            executor=opts.executor)

    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info("Stopping..")
        server.stop()
    return True

if __name__ == "__main__":
    sys.exit(main())

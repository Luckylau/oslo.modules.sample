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
    _usage = """Usage: %prog [options] <method> [<arg-name=arg-value>]*"""
    parser = optparse.OptionParser(usage=_usage)
    parser.add_option("--topic", action="store", default="my-topic",
                      help="target topic, default 'my-topic'")
    parser.add_option("--exchange", action="store", default="my-exchange",
                      help="target exchange, default 'my-exchange'")
    parser.add_option("--namespace", action="store", default="my-namespace",
                      help="target namespace, default 'my-namespace'")
    parser.add_option("--server", action="store",
                      help="Send only to the named server")
    parser.add_option("--fanout", action="store_true",
                      help="Fanout target")
    parser.add_option("--timeout", action="store", type="int", default=10,
                      help="timeout RPC request in seconds, default 10")
    parser.add_option("--cast", action="store_true",
                      help="cast the RPC call")
    parser.add_option("--version", action="store", default="1.1")
    parser.add_option("--url", action="store", default="rabbit://localhost",
                      help="transport address, default 'rabbit://localhost'")
    parser.add_option("--oslo-config", type="string",
                      help="the oslo.messaging configuration file.")
    parser.add_option("--payload", type="string",
                      help="Path to a data file to use as message body.")

    opts, extra = parser.parse_args(args=argv)
    if not extra:
        print("Error: <method> not supplied!!")
        return False

    rpc_log_init()
    method = extra[0]
    extra = extra[1:]
    args = {}
    args = dict([(x.split('=')[0], x.split('=')[1] if len(x) > 1 else None)
                 for x in extra])

    LOG.info("Calling %s (%s) on server=%s exchange=%s topic=%s namespace=%s"
            " fanout=%s cast=%s"
            % (method, extra, opts.server, opts.exchange, opts.topic,
                opts.namespace, str(opts.fanout), str(opts.cast)))

    if opts.oslo_config:
        LOG.info("Loading config file %s" % opts.oslo_config)
        cfg.CONF(["--config-file", opts.oslo_config])

    transport = messaging.get_transport(cfg.CONF, url=opts.url)

    target = messaging.Target(exchange=opts.exchange,
            topic=opts.topic,
            namespace=opts.namespace,
            server=opts.server,
            fanout=opts.fanout,
            version=opts.version)

    client = messaging.RPCClient(transport, target,
            timeout=opts.timeout,
            version_cap=opts.version).prepare()

    try:
        test_context = {"application": "rpc-client", "time": time.ctime()}
        if opts.cast or opts.fanout:
            client.cast(test_context, method, **args)
        else:
            rc = client.call(test_context, method, **args)
            LOG.info("RPC return value=%s" % str(rc))
    except KeyboardInterrupt:
        raise
    except Exception as e:
        LOG.error("Unexpected exception occured: %s" % str(e))
        raise

    LOG.info("RPC complete!  Cleaning up transport...")
    transport.cleanup()
    return True

if __name__ == "__main__":
    sys.exit(main())

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
import rpc_logging
import oslo_messaging as messaging
from oslo_config import cfg
import time
import sys

Domain="client"
rpc_logging.rpc_log_prepare(Domain)
LOG=rpc_logging.logname(__name__)

class Parameters(object):
    def __init__(self,exchange,topic,namespace,server,timeout,fanout,version,retry,url):
        self.exchange=exchange
        self.topic=topic
        self.namespace=namespace
        self.server=server
        self.timeout=timeout
        self.fanout=fanout
        self.version=version
        self.retry=retry
        self.url=url

def main():

    parm = Parameters("my-exchange", "my-topic", "my-namespace", "myserver", 10,None,"1.1",None,"rabbit://10.0.36.176")
    LOG.info("Client Running , Call Server name=%s , Configuration:exchange=%s , topic=%s , namespace=%s ," % (parm.server, parm.exchange, parm.topic, parm.namespace))

    transport=messaging.get_transport(cfg.CONF,url=parm.url)
    target=messaging.Target(exchange=parm.exchange,
                            topic=parm.topic,
                            namespace=parm.namespace,
                            server=parm.server,
                            version=parm.version
                            )
    client=messaging.RPCClient(transport,target,timeout=parm.timeout).prepare()
    args={"1":"fa:16:3e:a4:26:33","2":"fa:16:3e:57:d0:0f"}
    try:
        test_context={"application": "client", "time": time.ctime()}
        rc=client.call(test_context,"querydb",**args)
        LOG.info("Return from Server %s" %(str(rc)))
    except KeyboardInterrupt:
        raise
    except Exception as e:
        LOG.error("Unexpected exception occured: %s" % str(e))
        raise
    LOG.info("RPC complete!  Cleaning up transport...")
    transport.cleanup()
    return True

if __name__ == '__main__':
    sys.exit(main())

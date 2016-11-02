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
from Query_db import Connection
import time
import sys

Domain="server"
rpc_logging.rpc_log_prepare(Domain)
LOG=rpc_logging.logname(__name__)


class Parameters(object):
    def __init__(self,exchange,topic,namespace,server,version,legacy_namespaces,url,executor):
        self.exchange=exchange
        self.topic=topic
        self.namespace=namespace
        self.server=server
        self.version=version
        self.legacy_namespaces=legacy_namespaces
        self.url=url
        self.executor=executor

class ServerEndpoint(object):
    def __init__(self,server,target=None):
        self.server=server
        self.target=target

    def querydb(self,ctx,**args):
        LOG.info("%s::ServerEndpoint::querydb(ctxt=%s arg=%s) called"
                 % (self.server, str(ctx), str(args)))
        portids={}
        for (num,mac_address) in args.items():
            connection = Connection()
            port_detail = connection.get_port(str(mac_address))
            port_id=port_detail.id
            LOG.info("port_id=%s" %(port_id))
            portids[mac_address]=port_id
            LOG.info("portids=%s" % str(portids))
        args=portids
        return {"method": "querydb", "context": ctx, "args": args}

def main():

    parm=Parameters("my-exchange","my-topic","my-namespace","myserver","1.1",None,"rabbit://10.0.36.176","blocking")
    LOG.info("Server Runing ,Configuration : name=%s ,exchange=%s , topic=%s , namespace=%s" %(parm.server , parm.exchange ,parm.topic, parm.namespace))



    transport=messaging.get_transport(cfg.CONF,url=parm.url)

    target=messaging.Target(exchange=parm.exchange,
                            topic=parm.topic,
                            namespace=parm.namespace,
                            server=parm.server,
                            version=parm.version)
    server=messaging.get_rpc_server(transport,target,[ServerEndpoint(parm.server,target)],executor=parm.executor)

    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print ("Stopping server")
        server.stop()
    return True

if __name__ == '__main__':
    sys.exit(main())
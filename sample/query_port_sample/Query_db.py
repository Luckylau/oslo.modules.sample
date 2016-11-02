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
import sys

import sqlalchemy.orm
from neutron.db import models_v2
from sqlalchemy import create_engine
from sqlalchemy.orm import exc

import rpc_logging

Domain="sqlalchemy"
rpc_logging.rpc_log_prepare(Domain)
LOG= rpc_logging.logname(__name__)

_ENGINE=None
_SESSION_MAKER=None
port_details=None
'''Get the engine and session from sqlalchemy'''
def  get_engine():
    global  _ENGINE
    if _ENGINE is not None:
        return _ENGINE
    _ENGINE=create_engine("mysql+mysqldb://root:rootdb@10.0.36.176:3306/neutron",echo=True)
    return _ENGINE

def get_session_maker(engine):
    global _SESSION_MAKER
    if _SESSION_MAKER is not None:
        return _SESSION_MAKER
    _SESSION_MAKER = sqlalchemy.orm.sessionmaker(bind=engine)
    return _SESSION_MAKER


'''Get the session'''


def get_session():
    engine = get_engine()
    maker = get_session_maker(engine)
    session = maker()
    return session


class Connection(object):
    global port_details
    def __init__(self):
        pass

    def get_port(self, mac_address):
        query = get_session().query(models_v2.Port).filter_by(mac_address=mac_address)
        try:
            port_details = query.one()
        except exc.NoResultFound:
            LOG.error("error.....")
        return port_details

def main():
    LOG.info("========main=========")
    mac_address = "fa:16:3e:20:37:2e"
    connection = Connection()
    port_details = connection.get_port(mac_address)
    LOG.info("port_details %s" % (port_details))

if __name__ == '__main__':
    sys.exit(main())


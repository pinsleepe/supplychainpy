# Copyright (c) 2015-2016, Kevin Fasusi
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import select, and_
from supplychainpy.helpers.pickle_config import deserialise_config


def database_connection_uri():
    config = deserialise_config()
    db_uri = ''
    if os.name in ['posix', 'mac']:
        db_uri = 'sqlite:///{}/reporting.db'.format(config['database_path'])

    elif os.name == 'nt':
        db_uri = 'sqlite:///{}\\reporting.db'.format(config['database_path'])

    return db_uri


def connection(uri):
    engine = create_engine(uri)
    return engine

def master_sku_list(uri:str):
    """Uses connection and reflects database object from table to execute query for all skus in master_sku table"""
    meta = MetaData()
    engine = connection(uri)
    msk_table = Table('master_sku_list', meta, autoload=True, autoload_with=engine)
    skus = select([msk_table.columns.id, msk_table.columns.sku_id])
    rp = engine.execute(skus)
    result = []
    for i in rp:
        result.append((i['id'],i['sku_id']))
    rp.close()

    return result




    #master_sku_list = select()

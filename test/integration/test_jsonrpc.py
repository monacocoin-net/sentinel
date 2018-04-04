import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from monoecid import MonoeciDaemon
from monoeci_config import MonoeciConfig


def test_monoecid():
    config_text = MonoeciConfig.slurp_config_file(config.monoeci_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000005be1eb05b05fb45ae38ee9c1441514a65343cd146100a574de4278f1a3'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000008f18ad6913eed878632efbb83909272d493e5c065789330eb23ab65b5cf'

    creds = MonoeciConfig.get_rpc_creds(config_text, network)
    monoecid = MonoeciDaemon(**creds)
    assert monoecid.rpc_command is not None

    assert hasattr(monoecid, 'rpc_connection')

    # Monoeci testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = monoecid.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert monoecid.rpc_command('getblockhash', 0) == genesis_hash

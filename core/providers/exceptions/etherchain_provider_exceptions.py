#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class EtherchainProviderError(Exception):
    def __init__(self, _provider_name, _network, _err, _trace, *args):
        pass


class EtherchainProviderFatalException(Exception):
    def __init__(self, _provider_name, _network, _err, _trace, *args):
        pass

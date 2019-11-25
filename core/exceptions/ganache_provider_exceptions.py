#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GanacheProviderError(Exception):
    def __init__(self, _provider_name, _network, _err, _trace, *args):
        pass


class GanacheProviderFatalException(Exception):
    def __init__(self, _provider_name, _network, _err, _trace, *args):
        pass

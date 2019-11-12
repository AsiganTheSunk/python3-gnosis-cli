#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class NetworkAgentSocketError(Exception):
    """ NetworkAgentSocketError

    Raised when the Network Agent is unable to establish a connection to a host
    """
    def __init__(self, webscraper_name, err, trace, *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in  {1} Unable to establish a connection to the EndPoint: [ {2} ]'.format(self.name, webscraper_name, err)
        super(NetworkAgentSocketError, self).__init__(self.message, err, webscraper_name, *args)


class NetworkAgentFatalException(Exception):
    """ NetworkAgentSocketError

    Raised when the Network Agent is unable to establish a connection to a host
    """
    def __init__(self, webscraper_name, err, trace, *args):
        self.name = self.__class__.__name__
        self.trace = trace
        self.webscraper_name = webscraper_name
        self.err = err
        self.message = '{0}, in  {1} Unable to establish a connection to the EndPoint: [ {2} ]'.format(self.name, webscraper_name, err)
        super(NetworkAgentFatalException, self).__init__(self.message, err, webscraper_name, *args)


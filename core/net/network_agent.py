#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Socket Exceptions
from core.net.exceptions.network_exceptions import NetworkAgentFatalException

# Import Socket Module
import socket

class NetworkAgent:
    """ Network Agent

    Code Reference: https://stackoverflow.com/questions/3764291/checking-network-connection
    This class will establish the current state of the connectivity to internet for the system in case it's needed.
    """
    def __init__(self):
        self.name = self.__class__.__name__
        self.address = '8.8.8.8'
        self.port = 53
        self.timeout = 3

    def network_status(self):
        """ Network Status

        This Function will check the availability of the network connection
            :return True if there is internet connectivity otherwise False
        """
        try:
            socket.setdefaulttimeout(self.timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.address, self.port))
            return True
        except socket.error:
            return False
        except Exception as err:
            # Empty param should be trace for further debugging in case it's needed
            raise NetworkAgentFatalException(self.name, err, '')

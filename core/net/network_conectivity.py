#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Socket Module
import socket

""" 
This is a class for mathematical operations on complex numbers.
 
Attributes:
"""
class NetworkAgent:
    """
    Code Reference: https://stackoverflow.com/questions/3764291/checking-network-connection

    This class will establish the current state of the connectivity of the system in case it's needed.
    """
    def __init__(self):
        self.name = self.__class__.__name__
        self.default_host = '8.8.8.8'
        self.default_port = 53
        self.default_timeout = 3

    def network_status(self):
        """
        This Function will check the avaliability of the network

        Parameters:
            num (ComplexNumber): The complex number to be added.

        Returns:
            ComplexNumber: A complex number which contains the sum.

        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(self.default_timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.default_host, self.default_port))
            return True
        except socket.error:
            return False
        except Exception as err:
            print('FATAL ', err)


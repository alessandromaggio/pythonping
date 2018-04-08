"""Module that actually performs the ping, sending and receiving packets"""

import socket


class Message:
    """Represents an ICMP message with destination socket"""
    def __init__(self, target, packet, source):
        """Creates a message that may be sent, or used to represent a response

        :param target: Target IP or hostname of the message
        :type target: str
        :param packet: ICMP packet composing the message
        :type packet: icmp.ICMP
        :param source: Source IP or hostname of the message
        :type source: str"""
        self.target = target
        self.packet = packet
        self.source = source

    def send(self, source_socket):
        """Places the message on a socket

        :param source_socket: The socket to place the message on
        :type source_socket: socket"""
        source_socket.send(self.packet.packet)


class Response:
    """Represents a response to an ICMP message, with metadata like timing"""
    def __init__(self, message, time_elapsed):
        """Creates a representation of ICMP message received in response

        :param message: The message received
        :type message: Message
        :param time_elapsed: Time elapsed since the original request was sent, in seconds
        :type time_elapsed: float"""
        self.message = message
        self.time_elapsed = time_elapsed


class ResponseList:
    """Represents a series of ICMP responses"""
    def __init__(self, initial_set=None):
        """Creates a ResponseList with initial data if available

        :param initial_set: Already existing responses
        :type initial_set: list"""
        self._responses = []
        if initial_set is not None:
            self._responses = initial_set


class Communicator:
    """Instance actually communicating over the network, sending messages and handling responses"""
    def __init__(self, target, payload_provider):
        pass

    def listen_for(self, packet_id, timeout):
        """Listens for a packet of a given id for a given timeout

        :param packet_id: The ID of the packet to listen for, the same for request and response
        :type packet_id: int
        :param timeout: How long to listen for the specified packet, in seconds
        :type timeout: float
        :return: ???"""
        # TODO implement and define returns in the docstring
        pass

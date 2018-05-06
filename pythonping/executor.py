"""Module that actually performs the ping, sending and receiving packets"""

import os
from . import icmp
from . import network


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
        :type source_socket: network.Socket"""
        source_socket.send(self.packet.packet)

    def __repr__(self):
        return "{0}->{1}: {2}".format(self.source, self.target, self.packet.packet)


class Response:
    """Represents a response to an ICMP message, with metadata like timing"""
    def __init__(self, message, time_elapsed):
        """Creates a representation of ICMP message received in response

        :param message: The message received
        :type message: Union[None, Message]
        :param time_elapsed: Time elapsed since the original request was sent, in seconds
        :type time_elapsed: float"""
        self.message = message
        self.time_elapsed = time_elapsed

    def __repr__(self):
        return 'msg={0}; time={1}'.format(self.message, self.time_elapsed)


class ResponseList:
    """Represents a series of ICMP responses"""
    def __init__(self, initial_set=None):
        """Creates a ResponseList with initial data if available

        :param initial_set: Already existing responses
        :type initial_set: list"""
        self.clear()
        if initial_set is not None:
            self._responses = initial_set

    def clear(self):
        self._responses = []

    def append(self, value):
        self._responses.append(value)

    def __repr__(self):
        return str(self._responses)


class Communicator:
    """Instance actually communicating over the network, sending messages and handling responses"""
    def __init__(self, target, payload_provider, timeout, socket_options=(), seed_id=None):
        """Creates an instance that can handle communication with the target device

        :param target: IP or hostname of the remote device
        :type target: str
        :param payload_provider: An iterable list of payloads to send
        :type payload_provider: PayloadProvider
        :param timeout: Timeout that will apply to all ping messages, in seconds
        :type timeout: int
        :param socket_options: Options to specify for the network.Socket
        :type socket_options: tuple
        :param seed_id: The first ICMP packet ID to use
        :type seed_id: Union[None, int]"""
        self.socket = network.Socket(target, 'icmp', source=None, options=socket_options)
        self.provider = payload_provider
        self.timeout = timeout
        self.responses = ResponseList()
        self.seed_id = seed_id
        if self.seed_id is None:
            self.seed_id = os.getpid() & 0xFFFF

    def send_ping(self, packet_id, payload):
        """Sends one ICMP Echo Request on the socket

        :param packet_id: The ID to use for the packet
        :type packet_id: int
        :param payload: The payload of the ICMP message
        :type payload: bytes"""
        self.socket.send(icmp.ICMP(icmp.Types.EchoRequest, payload=payload, identifier=packet_id).packet)

    def listen_for(self, packet_id, timeout):
        """Listens for a packet of a given id for a given timeout

        :param packet_id: The ID of the packet to listen for, the same for request and response
        :type packet_id: int
        :param timeout: How long to listen for the specified packet, in seconds
        :type timeout: float
        :return: The response to the request with the specified packet_id
        :rtype: Response"""
        time_left = timeout
        response = icmp.ICMP()
        while time_left > 0:
            # Keep listening until a packet arrives
            raw_packet, source_socket, time_left = self.socket.receive(time_left)
            # If we actually received something
            if raw_packet != b'':
                response.unpack(raw_packet)
                if response.id == packet_id:
                    return Response(Message('', response, source_socket[0]), timeout-time_left)
        return Response(None, timeout)

    @staticmethod
    def increase_id(identifier, restore):
        """Increases an ICMP identifier leaving some noise on the first nibble

        :param identifier: The identifier to increase
        :type identifier: int
        :param restore: The value to restore the identifier to in case it fills the three rightmost nibbles
        :type restore: int
        :return: The increased or restored id
        :rtype: int"""
        identifier += 1
        if (identifier & 0x0FFF) >= 0xFFF:
            identifier = restore
        return identifier

    def run(self):
        """Performs all the pings and stores the responses"""
        self.responses.clear()
        identifier = self.seed_id
        for payload in self.provider:
            self.send_ping(identifier, payload)
            self.responses.append(self.listen_for(identifier, self.timeout))
            # identifier = self.increase_id(identifier, self.seed_id)

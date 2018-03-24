import random
import string
from . import icmp, network


class Constructor:
    @staticmethod
    def payload(size, pattern):
        """Creates a payload of the given size from the given pattern, if specified

        :param size: Size of the payload, may be 0 to simply use the pattern
        :type size: int
        :param pattern: Pattern from which to extrapolate the payload, or to repeat to create the payload
        :type pattern: Union[str, bytes]
        :return: The constructed payload
        :rtype: Union[str, bytes]

        If the size is None, the pattern itself is used. If the size is not none, but the pattern is, a random text is
        used instead. If both size and pattern are defined, the first N characters of the pattern are returned, where
        N=size. The pattern may be repeated until it is longer than the size specified."""
        if size < 0:
            raise ValueError('Payload size may not be negative')
        # If no size is specified, return the original pattern as is
        if size == 0:
            if pattern is not None:
                return pattern
            else:
                size = 4
        # If the size is specified, but the pattern is empty, create a random string
        if pattern is None:
            return random_text(size)
        # If both size and pattern are specified, repeat the pattern to create a payload of the right size
        else:
            while len(pattern) < size:
                pattern += pattern
            return pattern[:size]

    @staticmethod
    def repeat(count, size, pattern):
        """Returns a list of payloads generated from the same size and pattern

        :param count: How many payloads to generate
        :type count: int
        :param size: Size of the payload, may be 0 to simply use the pattern
        :type size: int
        :param pattern: Pattern from which to extrapolate the payload, or to repeat to create the payload
        :type pattern: Union[str, bytes]
        :return: The constructed payloads
        :rtype: list"""
        return [Constructor.payload(size, pattern) for _ in range(count)]

    @staticmethod
    def sweep(start, end, payload):
        """Returns a list of payloads of increasing sizes

        :param start: Size of the payload at the beginning
        :type start: int
        :param end: Size of the payload at the end of the sweep
        :type end: int
        :param payload: Pattern from which to extrapolate the payload, or to repeat to create the payload
        :type payload: Union[str, bytes]
        :return: The constructed payloads
        :rtype: list"""
        return [Constructor.payload(size, payload) for size in range(start, end)]

    @staticmethod
    def packet_to_payload_size(size):
        """Converts packet size to payload size

        :param size: Packet size
        :type size: int
        :return: ICMP payload size needed to obtain the specified packet size
        :rtype: int"""
        if size < icmp.ICMP.LEN_TO_PAYLOAD:
            return 0
        return size - icmp.ICMP.LEN_TO_PAYLOAD

    @staticmethod
    def construct(count, size, payload, sweep_start, sweep_end):
        """Constructs a list of payloads based on specified inputs

        :param count: How many payloads to generate
        :type count: int
        :param size: Expected size for the packet
        :type size: int
        :param payload: Pattern from which to extrapolate the payload, or to repeat to create the payload
        :type payload: Union[str, bytes]
        :param sweep_start: Size of the payload at the beginning
        :type sweep_start: int
        :param sweep_end: Size of the payload at the end of the sweep
        :type sweep_end: int
        :return: The constructed payloads
        :rtype: list"""
        size = Constructor.packet_to_payload_size(size)
        if sweep_start is not None and sweep_end is not None:
            return Constructor.sweep(sweep_start, sweep_end, payload)
        else:
            return Constructor.repeat(count, size, payload)


def random_text(size):
    """Returns a random text of the specified size

    :param size: Size of the random string, must be greater than 0
    :type size int
    :return: Random string
    :rtype: str"""
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def do_ping(socket, timeout, payload, identifier):
    """Performs a ping toward a remote device once, and handles the response

    :param socket: Socket that handles the ping
    :type socket: network.Socket
    :param timeout: time after which stop listening for a response
    :type timeout: int
    :param payload: Payload for the ICMP packet
    :type payload: Union[str, bytes]
    :param identifier: Identifier of this packet
    :type identifier: int
    :return: Whether the packet was received, The packet, remote socket, the time left before timeout, and checksum data
    :rtype: (bool, bytes, tuple, float, tuple)"""
    packet = icmp.ICMP(icmp.Types.EchoRequest, payload=payload, identifier=identifier)
    socket.send(packet.packet)
    return receive_ping(socket, timeout, identifier)


def receive_ping(socket, timeout, identifier):
    """Listen for the ICMP response of the specified packet (identifier) until timeout expires

    :param socket: Socket that handles the ping
    :type socket: network.Socket
    :param timeout: time after which stop listening for a response
    :type timeout: int
    :param identifier: Identifier of the source packet, looking for this value in incoming packets
    :type identifier: int
    :return: Whether the packet was received, The packet, remote socket, the time left before timeout, and checksum data
    :rtype: (bool, bytes, tuple, float, tuple)"""
    time_left = timeout
    response = icmp.ICMP()
    while time_left > 0:
        # Keep listening until a packet arrives
        raw_packet, source_socket, time_left = socket.receive(time_left)
        # If we actually received something
        if raw_packet != b'':
            response.unpack(raw_packet)
            if response.id == identifier:
                checksum_data = (response.is_valid, response.expected_checksum, response.received_checksum,)
                # True at the beginning indicates a response was received
                return True, raw_packet, source_socket, time_left, checksum_data
    # No response received, timeout
    # False at the beginning indicates no response was received
    return False, None, None, 0, None,


def process_pings(socket, timeout, payload_list, start_id):
    packet_id = start_id
    for payload in payload_list:
        yield do_ping(socket, timeout, payload, packet_id)
        packet_id += 1

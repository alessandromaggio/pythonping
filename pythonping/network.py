import socket
import select
import time


class Socket:
    DONT_FRAGMENT = (socket.SOL_IP, 10, 1)           # Option value for raw socket

    def __init__(self, destination, protocol, source=None, options=(), buffer_size=2048):
        """Creates a network socket to exchange messages

        :param destination: Destination IP address
        :type destination: str
        :param protocol: Name of the protocol to use
        :type protocol: str
        :param options: Options to set on the socket
        :type options: tuple
        :param source: Source IP to use - implemented in future releases
        :type source: Union[None, str]
        :param buffer_size: Size in bytes of the listening buffer for incoming packets (replies)
        :type buffer_size: int"""
        try:
            self.destination = socket.gethostbyname(destination)
        except socket.gaierror as e:
            raise RuntimeError('Cannot resolve address "' + destination + '", try verify your DNS or host file')
        self.protocol = socket.getprotobyname(protocol)
        self.buffer_size = buffer_size
        if source is not None:
            raise NotImplementedError('PythonPing currently does not support specification of source IP')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.protocol)
        if options:
            self.socket.setsockopt(*options)

    def send(self, packet):
        """Sends a raw packet on the stream

        :param packet: The raw packet to send
        :type packet: bytes"""
        self.socket.sendto(packet, (self.destination, 0))

    def receive(self, timeout=2):
        """Listen for incoming packets until timeout

        :param timeout: Time after which stop listening
        :type timeout: Union[int, float]
        :return: The packet, the remote socket, and the time left before timeout
        :rtype: (bytes, tuple, float)"""
        time_left = timeout
        while time_left > 0:
            start_select = time.perf_counter()
            data_ready = select.select([self.socket], [], [], time_left)
            elapsed_in_select = time.perf_counter() - start_select
            time_left -= elapsed_in_select
            if not data_ready[0]:
                # Timeout
                return b'', '', time_left
            packet, source = self.socket.recvfrom(self.buffer_size)
            return packet, source, time_left

    def __del__(self):
        try:
            if self.socket:
                self.socket.close()
        except AttributeError:
            raise AttributeError("Attribute error because of failed socket init. Make sure you have the root privilege."
                                 " This error may also be caused from DNS resolution problems.")
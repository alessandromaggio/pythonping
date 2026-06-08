import time
import select
import asyncio
from . import network

class AsyncSocket(network.Socket):
    def __init__(self, destination, protocol, options=(), buffer_size=2048, source=None):
        """Creates a async network socket to exchange messages

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
        if options is None:
            options = ()
        super().__init__(destination, protocol, options, buffer_size, source)
        # Nonblocking is required here to support asynchronous operations.
        self.socket.setblocking(False)
    
    async def send(self, packet):
        """Sends a raw packet on the stream

        :param packet: The raw packet to send
        :type packet: bytes"""
        loop = asyncio.get_running_loop()
        if self.source:
            self.socket.bind((self.source, 0))
        await loop.sock_sendto(self.socket, packet, (self.destination, 0))

    async def receive(self, timeout=2):
        """Listen for incoming packets until timeout

        :param timeout: Time after which stop listening
        :type timeout: Union[int, float]
        :return: The packet, the remote socket, and the time left before timeout
        :rtype: (bytes, tuple, float)"""
        loop = asyncio.get_running_loop()
        start_time = time.perf_counter()
        try:
            response = await asyncio.wait_for(
                loop.sock_recvfrom(
                    self.socket,
                    self.buffer_size
                ),
                timeout = timeout
            )
            packet, source = response
        except asyncio.TimeoutError:
            packet, source = b"", b""
        end_time = time.perf_counter()
        return packet, source, timeout - (end_time - start_time)
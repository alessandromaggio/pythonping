import asyncio

from . import executor
from . import aionetwork
from . import icmp

class AsyncCommunicator(executor.Communicator):
    socket: aionetwork.AsyncSocket

    @staticmethod
    def _create_socket(
        target,
        protocol='icmp',
        options=(),
        buffer_size=2048,
        source=None,
    ):
        return aionetwork.AsyncSocket(target, protocol, options, buffer_size, source)
    
    async def send_ping(self, packet_id, sequence_number, payload):
        """Sends one ICMP Echo Request on the socket

        :param packet_id: The ID to use for the packet
        :type packet_id: int
        :param sequence_number: The sequence number to use for the packet
        :type sequence_number: int
        :param payload: The payload of the ICMP message
        :type payload: Union[str, bytes]
        :rtype: ICMP"""
        i = icmp.ICMP(
            icmp.Types.EchoRequest,
            payload=payload,
            identifier=packet_id, sequence_number=sequence_number)
        await self.socket.send(i.packet)
        return i

    async def listen_for(self, packet_id, timeout, payload_pattern=None, source_request=None):
        """Listens for a packet of a given id for a given timeout

        :param packet_id: The ID of the packet to listen for, the same for request and response
        :type packet_id: int
        :param timeout: How long to listen for the specified packet, in seconds
        :type timeout: float
        :param payload_pattern: Payload reply pattern to match to request, if set to None, match by ID only
        :type payload_pattern: Union[None, bytes]
        :return: The response to the request with the specified packet_id
        :rtype: Response"""
        time_left = timeout
        response = icmp.ICMP()
        while time_left > 0:
            # Keep listening until a packet arrives
            raw_packet, source_socket, time_left = await self.socket.receive(time_left)
            # If we actually received something
            if raw_packet != b'':
                response.unpack(raw_packet)

                # Ensure we have not unpacked the packet we sent (RHEL will also listen to outgoing packets)
                if response.id == packet_id and response.message_type != icmp.Types.EchoRequest.type_id:
                    if payload_pattern is None:
                        # To allow Windows-like behaviour (no payload inspection, but only match packet identifiers),
                        # simply allow for it to be an always true in the legacy usage case
                        payload_matched = True
                    else:
                        payload_matched = (payload_pattern == response.payload)

                    if payload_matched:
                        return executor.Response(executor.Message('', response, source_socket[0]), timeout - time_left, source_request, repr_format=self.repr_format)
        return executor.Response(None, timeout, source_request, repr_format=self.repr_format)
    
    async def run(self, match_payloads=False):
        """Performs all the pings and stores the responses

        :param match_payloads: optional to set to True to make sure requests and replies have equivalent payloads
        :type match_payloads: bool"""
        self.responses.clear()
        identifier = self.seed_id
        seq = 1
        for payload in self.provider:
            icmp_out = await self.send_ping(identifier, seq, payload)
            if not match_payloads:
                self.responses.append(await self.listen_for(identifier, self.timeout, None, icmp_out))
            else:
                self.responses.append(await self.listen_for(identifier, self.timeout, icmp_out.payload, icmp_out))

            seq = self.increase_seq(seq)

            if self.interval:
                await asyncio.sleep(self.interval)

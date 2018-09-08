import sys
from . import network, executor, payload_provider
from .utils import random_text


def ping(target,
         timeout=2,
         count=4,
         size=1,
         payload=None,
         sweep_start=None,
         sweep_end=None,
         df=False,
         verbose=False,
         out=sys.stdout):
    """Pings a remote host and handles the responses

    :param target: The remote hostname or IP address to ping
    :type target: str
    :param timeout: How long before considering each non-arrived reply permanently lost
    :type timeout: int
    :param count: How many times to attempt the ping
    :type count: int
    :param size: Size of the entire packet to send
    :type size: int
    :param payload: Payload content, leave None if size is set to use random text
    :type payload: Union[str, bytes]
    :param sweep_start: If size is not set, initial size in a sweep of sizes
    :type sweep_start: int
    :param sweep_end: If size is not set, final size in a sweep of sizes
    :type sweep_end: int
    :param df: Don't Fragment flag value for IP Header
    :type df: bool
    :param verbose: Print output while performing operations
    :type verbose: bool
    :param out: Stream to which redirect the verbose output
    :type out: stream
    :return: List with the result of each ping
    :rtype: executor.ResponseList"""
    provider = payload_provider.Repeat(b'', 0)
    if size and size > 0:
        if not payload:
            payload = random_text(size)
        provider = payload_provider.Repeat(payload, count)
    elif sweep_start and sweep_end and sweep_end >= sweep_start:
        if not payload:
            payload = random_text(sweep_start)
        provider = payload_provider.Sweep(payload, sweep_start, sweep_end)
    options = ()
    if df:
        options = network.Socket.DONT_FRAGMENT
    comm = executor.Communicator(target, provider, timeout, socket_options=options, verbose=verbose, output=out)
    comm.run()
    return comm.responses

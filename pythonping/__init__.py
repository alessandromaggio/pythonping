import sys
import os
from . import network, helper


def ping(target,
         timeout=2,
         count=4,
         size=0,
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
    :rtype: result"""
    options = ()
    if df:
        options = (network.Socket.DONT_FRAGMENT,)
    net_socket = network.Socket(target, "icmp", options=options)
    payload_list = helper.Constructor.construct(count, size, payload, sweep_start, sweep_end)
    output = []
    if verbose:
        print("Pinging {0}, timeout is {1}s:".format(target, timeout))
    for ping_result in helper.process_pings(net_socket, timeout, payload_list, os.getpid() & 0xFF00):
        if verbose:
            if ping_result[4][0]:
                checksum_error = ''
            else:
                checksum_error = "[Checksum Error, expected {0} but got {1}]".format(
                    ping_result[4][1],
                    ping_result[4][2]
                )
            if ping_result[0]:
                message = "Reply from {0} in {1}ms {2}".format(
                    ping_result[2][0],
                    round((timeout - ping_result[3]) * 1000),
                    checksum_error
                )
            else:
                message = "No reply"
            print(" " + message, file=out)
        output.append(ping_result)
    if verbose:
        max_time = timeout - output[0][3]
        min_time = timeout - output[0][3]
        avg_time = timeout - output[0][3]
        success = 0
        failure = 0
        for i in range(1, len(output)):
            max_time = max(timeout - output[i][3], max_time)
            min_time = min(timeout - output[i][3], min_time)
            avg_time = (avg_time + (timeout - output[i][3])) / 2
            if output[i][0]:
                success += 1
            else:
                failure += 1
        print("{0}% success, min/avg/max is {1}/{2}/{3} ms".format(
            round(success / (success+failure) * 100),
            round(min_time * 1000),
            round(avg_time * 1000),
            round(max_time * 1000)
        ), file=out)
    return output

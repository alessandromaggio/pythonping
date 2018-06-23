# pythonping
PythonPing is simple way to ping in Python. With it, you can send ICMP Probes to remote devices like you would do from the terminal. PythonPing is modular, so that you can run it in a script as a standalone function, or integrate its components in a fully-fledged application.

## Basic Usage
The simplest usage of PythonPing is in a script. You can use the `ping` function to ping a target. If you want to see the output immediately, emulating what happens on the terminal, use the `verbose` flag as below.
```python
from pythonping import ping


ping('127.0.0.1', verbose=True)
```
This will yeld the following result.
```
Reply from 127.0.0.1, 9 bytes in 0.17ms
Reply from 127.0.0.1, 9 bytes in 0.14ms
Reply from 127.0.0.1, 9 bytes in 0.12ms
Reply from 127.0.0.1, 9 bytes in 0.12ms
```
Regardless of the verbose mode, the `ping` function will always return a `ResponseList` object. This is a special iterable object, containing a list of `Response` items. In each response, you can find the packet received and some meta information, like the time it took to receive the response and any error message.
You can also tune your ping by using some of its additional parameters:
* `size` is an integer that allows you to specify the size of the ICMP payload you desire
* `timeout` is the number of seconds you wish to wait for a response, before assuming the target is unreachable
* `payload` allows you to use a specific payload (bytes)
* `count` specify allows you to define how many ICMP packets to send
* `sweep_start` and `sweep_end` allows you to perform a ping sweep, starting from payload size defined in `sweep_start` and growing up to size defined in `sweep_end`. Here, we repeat the payload you provided to match the desired size, or we generate a random one if no payload was provided. Note that if you defined `size`, these two fields will be ignored
* `df` is a flag that, if set to True, will enable the *Don't Fragment* flag in the IP header
* `verbose` enables the verbose mode, printing output to a stream (see `out`)
* `out` is the target stream of verbose mode. If you enable the verbose mode and do not provide `out`, verbose output will be send to the `sys.stdout` stream. You may want to use a file here, for example.

## Advanced Usage
If you wish to extend PythonPing, or integrate it in your application, we recommend to use the classes that are part of Python Ping instead of the `ping` function.
`executor.Communicator` handles the communication with the target device, it takes care of sending ICMP requests and processing responses. It ultimately produces the `executor.ResponseList` object. The `Communicator` needs to know a target and which payloads to send to the remote device. For that, we have several classes in the `payload_provider` module. You may want to create your own provider by extending `payload_provider.PayloadProvider`. If you are interested in that, you should check the documentation of both `executor` and `payload_provider` module.

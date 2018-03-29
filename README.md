# pythonping
PythonPing is simple way to ping in Python.
Currently, pythonping is in a beta stage. This means it has limited features and some parts of the code may need further testing.
However, it is already stable enough to start using it. The best and simple way to do it is with the following code.
```python
from pythonping import ping


ping('8.8.8.8', verbose=True)
```
This will yeld the following result.
```
Pinging 8.8.8.8, timeout is 2s:
 Reply from 8.8.8.8 in 9ms 
 Reply from 8.8.8.8 in 9ms 
 Reply from 8.8.8.8 in 9ms 
 Reply from 8.8.8.8 in 9ms 
100% success, min/avg/max is 9/9/9 ms
```
The `ping` function will always return a list of responses for each packet received as ICMP Reply. Each response is a tuple, contaning
* True or False to indicate if we had a reply
* The bytes in the response packet
* A tuple with IP that sourced the reply and its port (which is always 0)
* Time left (timeout specified minus time elapsed to receive the reply)
* Checksum validation Data: a tuple, where the first value is a boolean True if the checksum is valid, then we have the expected checksum and the received checksum

> **Warning**: we plan to slightly modify the output of ping before releasing a stable version, this syntax will remain available in
> another function (e.g. old_ping), thus we reccomend importing ping with an alias.

import argparse
from pythonping import ping
def perform_ping(target, count=4):
    """Performs ICMP pings and displays the responses"""
    responses = ping(target, count=count)
    
    # Display ping results
    print(f"Ping results for {target}:")
    min_rtt = float('inf')
    max_rtt = 0
    total_rtt = 0
    for response in responses:
        if response.success:
            rtt = response.time_elapsed_ms
            total_rtt += rtt
            if rtt < min_rtt:
                min_rtt = rtt
            if rtt > max_rtt:
                max_rtt = rtt
            print(f"Reply from {response.message.source}, {len(response.message.packet.raw)} bytes in {response.time_elapsed_ms}ms")
            # Extracted attributes: source, packet, time_elapsed_ms
        else:
            print(f"Request timed out")
    
    # Calculate and display RTT statistics
    if len(responses) > 0:
        avg_rtt = total_rtt / len(responses)
        print(f"\nRound Trip Times min/avg/max is {min_rtt:.2f}/{avg_rtt:.2f}/{max_rtt:.2f} ms")

def ping_command_line():
    parser = argparse.ArgumentParser(description='PythonPing command-line tool')
    parser.add_argument('target', nargs='?', help='Target IP address to ping')
    parser.add_argument('--count', type=int, default=4, help='Number of pings to send')
    args = parser.parse_args()
    
    if args.target:
        perform_ping(args.target, count=args.count)
    else:
        print("Please provide a target IP address or hostname.")

if __name__ == "__main__":
    ping_command_line()

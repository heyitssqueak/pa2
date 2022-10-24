# Overview
The report explains the results from the project while this file goes over the procedure and commands used. All pcaps from every stage of the project are located in the `pcaps` folder. 

`TCPclient.py` is never used during the experiments, but it can connect to `TCPserver.py` if needed. All three scripts will send a file, `img.jpg` upon establishing a connection (TCP) or receiving an incoming packet (UDP). Each script can be run with the following commands:
- `sudo python3 TCPclient.py`
- `sudo python3 TCPserver.py`
- `sudo python3 UDPserver.py`


# Procedure
For all tasks in part 1, the setup was as follows:
Client: TCP/IP Debugger on iOS
Server: `TCPserver.py` or `UDPserver.py` on Ubuntu

For part 2:
Client: terminal on Ubuntu
Server: WifiPerf Endpoint on iOS

## 1.1
### TCP
Start the server by running `sudo python3 TCPserver.py`. Open Wireshark and start the packet capture. For close distance capture, place the phone next to the laptop. For a medium or far distance capture, walk the desired distance until the Wi-Fi connection gets weaker. Connect to the server using the TCP/IP Debugger app on the phone. Keep reconnecting to the server for a total of 10 times, which sends 10 files from the server to the client. Return to the laptop if necessary, and stop the packet capture.

Filter for TCP and FTP packets using the `ftp-data || ftp || tcp` filter. Go to Statistics > Protocol Hierarchy and scroll down to the bottom for the average throughput. Go to Statistics > I/O Graphs and hover the mouse over the peaks in the graph to estimate the instantaneous throughput. Repeat for each packet capture for each distance. To graph the average throughput on the I/O Graph, filter for TCP and FTP packets again but using a different version of the filter, such as `ftp-data || tcp || ftp`. This will register a new line within the graph. Then change the SMA period to be 1000 interval SMA. If desired, change the y-axis measurement to bits instead of packets.

### UDP
Start the server by running `sudo python3 UDPserver.py`. Open Wireshark and start the packet capture. For close distance capture, place the phone next to the laptop. For a medium or far distance capture, walk the desired distance until the Wi-Fi connection gets weaker. Connect to the server using the TCP/IP Debugger app on the phone and set the scheduled delivery to be every 5000ms. The packet data can be an arbitrary value or character. Press start and wait for 10 packets to be sent to the server by keeping track using the terminal within the app. After 10 packets have been sent, stop the scheduled delivery, return to the laptop if necessary, and stop the packet capture.

Filter for UDP packets using the `udp` filter. Go to Statistics > Protocol Hierarchy and scroll down to the bottom for the average throughput. Go to Statistics > I/O Graphs and hover the mouse over the peaks in the graph to estimate the instantaneous throughput. Repeat for each packet capture for each distance. To graph the average throughput on the I/O Graph, filter for UDP packets again but using a different version of the filter, such as `udp || udp`. This will register a new line within the graph. Then change the SMA period to be 1000 interval SMA. If desired, change the y-axis measurement to bits instead of packets.

## 1.2
The phone will be placed next to the laptop for all packet captures. Open a terminal in the virtual machine. Use the command `sudo tc qdisc add dev [enp0s7] root netem loss [\%]` to introduce a percentage of packet loss to the network, replacing the values within brackets with values that work for your computer. For each percent, take a packet capture of 10 file transfers as described in 1.1. After taking packet captures for each percent of packet loss, reset the packet loss to normal using `sudo tc qdisc delete dev [enp0s7] root netem loss` and take the control packet capture.

To get the statistics and graphs for each step, follow the instructions in 1.1 for either TCP or UDP protocol.

## 1.3
### TCP
First take the control packet capture. Then open a terminal in the virtual machine. For each parameter, the value will be changed, then a packet capture will be taken, and the value will be reset to default. This is to isolate each parameter so any change in network performance is due to only one parameter at a time.

TCP flavor: `sudo sysctl net.ipv4.tcp_congestion_control=reno` to vary, `sudo sysctl net.ipv4.tcp_congestion_control=cubic` to reset
Window scaling: `sudo sysctl net.ipv4.tcp_window_scaling=10` to vary, `sudo sysctl net.ipv4.tcp_window_scaling=1` to reset
Receive window: `sudo sysctl net.ipv4.tcp_rmem=131072` to vary, `sudo sysctl net.ipv4.tcp_rmem=4096` to reset
Send window: `sudo sysctl net.ipv4.tcp_wmem=16384` to vary, `sudo sysctl net.ipv4.tcp_wmem=4096` to reset

To get the number of streams as shown in the tables in Section 1.3 of the report, go to Statistics > TCP Stream Graphs > Window Scaling and press the up arrow next to the "Streams" label until it won't increase anymore. The value+1 is the total number of streams. The number of active streams is the number of streams that aren't blank, which can be found by looking at every TCP stream.

### UDP
First take the control packet capture. Then open a terminal in the virtual machine. For each parameter, two values will be changed, one "default" and "max" value. A packet capture is taken before both values are reset.

Receive window: `sudo sysctl net.core.rmem_default=26214400` and `sudo sysctl net.core.rmem_max=26214400` to vary, `sudo sysctl net.core.rmem_default=212992` and `sudo sysctl net.core.rmem_max=212992` to reset
Send window: `sudo sysctl net.core.wmem_default=26214400` and `sudo sysctl net.core.wmem_max=26214400` to vary, `sudo sysctl net.core.wmem_default=212992` and `sudo sysctl net.core.wmem_max=212992` to reset

## 1.4
The TCP flavor can be found by running `sysctl net.ipv4.tcp_congestion_control` in the terminal. 

## 2
Open the WifiPerf Endpoint app. Place the phone next to the laptop. Open a terminal in Ubuntu and run `iperf -c [10.140.230.67] -t 30 -i 1 -w 2m`. This runs the test for 30 seconds with updates every 1 second, with a window size of 2m. Run the test 10 times and take the average of the 10 results.


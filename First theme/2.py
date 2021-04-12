import socket
import time
import struct
import threading
import ntp_packet
from collections import deque


task_queue = deque()
stop_flag = False


class WorkTread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        global task_queue, stop_flag
        while True:
            if stop_flag:
                break
            try:
                data, addr, recv_timestamp = task_queue.popleft()
                recv_packet = ntp_packet.NTPPacket()
                recv_packet.unpack(data)
                timestamp_high, timestamp_low = recv_packet.get_tx_timestamp()
                send_packet = ntp_packet.NTPPacket(ver=3, mode=4)
                send_packet.stratum = 2
                send_packet.pool = 10
                send_packet.precision = 0xFA
                send_packet.root_delay = 0x0BFA
                send_packet.root_dispersion = 0x0AA7
                send_packet.ref_id = 0X808A8C2C
                send_packet.ref = recv_timestamp - 5



def read_config(path):
    with open(path) as cfg:
        data = cfg.read().split('=')
    if data[0] == "ERROR_TIME":
        return int(data[1])
    return None


def listen_port():
    error_time = read_config("./smtp_server.cfg")
    address = "localhost"
    port = 123
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((address, port))


if __name__ == "__main__":
    listen_port()

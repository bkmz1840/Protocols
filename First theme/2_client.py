import socket
import datetime
import time
import struct
import ntp_packet


def get_time():
    format_diff = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1))\
                      .days * 24 * 3600
    waiting_time = 5
    server = "localhost"
    port = 123
    packet = ntp_packet.NTPPacket(ver=2, mode=3,
                                  transmit=time.time() + format_diff)
    answer = ntp_packet.NTPPacket()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(waiting_time)
        sock.sendto(packet.pack(), (server, port))
        data = sock.recv(48)
        arrive_time = time.time() + format_diff
        answer.unpack(data)
        difference_time = answer.get_time_difference(arrive_time)
        return datetime.datetime.fromtimestamp(time.time() + difference_time)\
            .strftime("%c")


if __name__ == "__main__":
    print(get_time())
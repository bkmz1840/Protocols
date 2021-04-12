from scapy.all import *
from scapy.layers.inet import IP, ICMP
from ipwhois.ipwhois import IPWhois
import multiprocessing


def whois(ip):
    try:
        whois_obj = IPWhois(ip)
        results = whois_obj.lookup_rdap(depth=1)
        return results["asn_description"] + " - " + \
            results["network"]["remarks"][0]["description"]
    except Exception:
        return ""


def send_packet_and_get_reply(pck, ttl, is_end):
    reply = sr1(pck, verbose=0)  # ip <- ICMP - reply.payload
    if reply is None:
        is_end.value = 1
    ip = reply.src
    print(f"{ttl}: {ip}: {whois(ip)}")
    if reply.payload.type == 0:
        is_end.value = 1
    else:
        is_end.value = 0


def trace_route(hostname):
    for i in range(1, 31):
        pck = IP(dst=hostname, ttl=i) / ICMP()
        ret_value = multiprocessing.Value("i", 0, lock=False)
        process = multiprocessing.Process(
            target=send_packet_and_get_reply, args=(pck, i, ret_value))
        process.start()
        process.join(60)
        if process.is_alive():
            print("* * *")
            process.terminate()
            break
        else:
            if ret_value.value == 1:
                break


if __name__ == "__main__":
    try:
        trace_route(input())
    except OSError as error:
        print("Please, check your internet connection "
              "or try use script as administrator")

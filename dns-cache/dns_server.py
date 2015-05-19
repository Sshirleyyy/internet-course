from socket import *
import datetime
import urllib.parse
import asyncio
import argparse
from dns_packets import *
import pickle


def get_args():
    parser = argparse.ArgumentParser(description="DNS server")
    parser.add_argument(
        "forwarder",
        default="8.8.4.4",
        help="Forwarder IP address")
    parser.add_argument(
        "--port",
        help="Port",
        default=53, type=int)
    parser.add_argument(
        "--ttl",
        help="Time to life data in cache",
        default=3600, type=int)
    args = parser.parse_args()
    return args


class DNSServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        dns = DNS()
        answer = dns.get_addr(data)
        self.transport.sendto(answer, addr)


class DNSError(Exception):
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DNS(object, metaclass=Singleton):
    def __init__(self, forwarder, ttl, cache):
        self.cache = cache
        self.forwarder = forwarder
        self.err_count = 0
        self.ttl = ttl

    def get_addr(self, packet):
        dns_msg = DNSMessage()
        dns_msg.unpack(packet)

        for question in dns_msg.query:
            if question.name in self.cache.keys():
                answer, timestamp = self.cache[question.name]
                now = datetime.datetime.now()
                age = now - timestamp
                if age.seconds > self.ttl:
                    print('Record is too old\nGet new data')
                    return self._get_addr(question, dns_msg)
                else:
                    print('Record found in cache')
                    return answer.pack()
            else:
                print('Record is not found')
                return self._get_addr(question, dns_msg)


    def _get_addr(self, question, dns_msg):
        ID = dns_msg.header.identification
        flags = dns_msg.header.flags
        validation = dns_msg.validation
        header = HeaderQuery(
            identification=ID,
            flags=flags,
            responses_count=1,
            answers_count=0,
            resources_count=0,
            optional_count=0)
        msg = DNSMessage(header, [question], [])

        try:
            with socket(AF_INET, SOCK_DGRAM) as new_socket:
                new_socket.settimeout(2.0)
                new_socket.sendto(msg.pack(), (self.forwarder, 53))
                data, addr = new_socket.recvfrom(1024)

            answer = DNSMessage()
            answer.unpack(data)
            self.cache[question.name] = (
                answer, datetime.datetime.now())
            return data
        except Exception as e:
            self.err_count = self.err_count + 1
            # BLACK MAGICK
            if self.err_count > 5:
                self.forwarder = '8.8.4.4'
            raise DNSError(e)

def main(args):
    try:
        cache = pickle.load(open('dump', 'rb'))
    except Exception:
        cache = {}
    dns = DNS(args.forwarder, args.ttl, cache)
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(
        DNSServer, local_addr=('127.0.0.1', args.port))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pickle.dump(dns.cache, open('dump', 'wb'))

    transport.close()
    loop.close()

if __name__ == "__main__":
    args = get_args()
    main(args)

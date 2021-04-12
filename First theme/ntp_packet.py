import struct


class NTPPacket:
    _FORMAT = "!B B b b 11I"

    def __init__(self, ver=2, mode=3, transmit=0):
        self.leap_indicator = 0
        self.version = ver
        self.mode = mode
        self.stratum = 0
        self.pool = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0
        self.ref_id = 0
        self.ref = 0
        self.originate = 0
        self.receive = 0
        self.transmit = transmit

    def get_time_difference(self, arrive_time):
        return self.receive - self.originate - arrive_time + self.transmit

    @staticmethod
    def get_fraction(number, precision):
        return int((number - int(number)) * 2 ** precision)

    def pack(self):
        return struct.pack(NTPPacket._FORMAT,
                           (self.leap_indicator << 6) + (self.version << 3) +
                           self.mode,
                           self.stratum,
                           self.precision,
                           int(self.root_delay) +
                           NTPPacket.get_fraction(self.root_delay, 16),
                           int(self.root_dispersion) +
                           NTPPacket.get_fraction(self.root_dispersion, 16),
                           self.ref_id,
                           int(self.ref),
                           NTPPacket.get_fraction(self.ref, 32),
                           int(self.originate),
                           NTPPacket.get_fraction(self.originate, 32),
                           int(self.receive),
                           NTPPacket.get_fraction(self.receive, 32),
                           int(self.transmit),
                           NTPPacket.get_fraction(self.transmit, 32))

    def unpack(self, data: bytes):
        unpacked_data = struct.unpack(NTPPacket._FORMAT, data)
        self.leap_indicator = unpacked_data[0] >> 6
        self.version = unpacked_data[0] >> 3 & 0b111
        self.mode = unpacked_data[0] & 0b111
        self.stratum = unpacked_data[1]
        self.pool = unpacked_data[2]
        self.precision = unpacked_data[3]
        self.root_delay = (unpacked_data[4] >> 16) + \
                          (unpacked_data[4] & 0xFFFF) / 2 ** 16
        self.root_dispersion = (unpacked_data[5] >> 16) + \
                               (unpacked_data[5] & 0xFFFF) / 2 ** 16
        self.ref_id = str((unpacked_data[6] >> 24) & 0xFF) + " " + \
            str((unpacked_data[6] >> 16) & 0xFF) + " " + \
            str((unpacked_data[6] >> 8) & 0xFF) + " " + \
            str(unpacked_data[6] & 0xFF)
        self.ref = unpacked_data[7] + unpacked_data[8] / 2 ** 32
        self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32
        self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32
        self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32
        return self

from typing import List, Dict
import struct
import config
# Import pythonnet clr and .NET System namespace
import clr
clr.AddReference("System")
from System import Array, Byte

# Add a reference to the LibSie.dll, in your SIE install directory

clr.AddReference(config.SIE_DLL)

from LibSIE.IO.Iff import IffStream, IffWriter

class StringEntry:
    def __init__(self, id_: str, value: str):
        self.ID = id_
        self.Value = value

class StringFile:
    ABCD = 0xabcd

    def __init__(self, iff_stream=None):
        self.Entries: List[StringEntry] = []
        self.Version = 1
        self.NextUID = 1
        if iff_stream is not None:
            self.read_object(iff_stream)

    def read_object(self, iff_stream):
        abcd = iff_stream.GetUInt32()
        if abcd != self.ABCD:
            return

        self.Version = iff_stream.GetByte()
        self.NextUID = iff_stream.GetUInt32()
        num_string = iff_stream.GetUInt32()

        ht = {}
        for _ in range(num_string):  # Changed from uint i to range()
            num = iff_stream.GetUInt32()
            key = iff_stream.GetUInt32()
            length = 2 * iff_stream.GetUInt32()
            str_bytes = iff_stream.GetBytes(length)
            str_val = bytes(str_bytes).decode('utf-16le')  # Decoding assuming utf-16 little endian
            ht[num] = str_val

        self.Entries.clear()
        for _ in range(num_string):
            stf_key = iff_stream.GetUInt32()
            str_len = iff_stream.GetUInt32()
            entry_value = ht[stf_key]
            self.Entries.append(StringEntry(iff_stream.GetString(str_len), entry_value))

    def write_object(self, iff_stream):
        iff_stream.Write(struct.pack('<I', self.ABCD))
        iff_stream.Write(struct.pack('<B', self.Version))
        iff_stream.Write(struct.pack('<I', self.NextUID))
        iff_stream.Write(struct.pack('<I', len(self.Entries)))

        index = 1
        for entry in self.Entries:
            iff_stream.Write(struct.pack('<I', index))
            iff_stream.Write(struct.pack('<I', 0xFFFFFFFF))
            iff_stream.Write(struct.pack('<I', len(entry.Value)))
            iff_stream.Write(entry.Value.encode('utf-16le'))
            index += 1

        index = 1
        for entry in self.Entries:
            iff_stream.Write(struct.pack('<I', index))
            iff_stream.Write(struct.pack('<I', len(entry.ID)))
            iff_stream.Write(entry.ID.encode('ascii'))  # Assuming ASCII encoding
            index += 1
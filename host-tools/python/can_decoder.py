
import json, os

DEF_PATH = os.path.join('can-definitions','canonical_definitions.json')

def _bit_extract_le(data_bytes, start_bit, length, signed=False):
    val = int.from_bytes(data_bytes, 'little', signed=False)
    mask = (1 << length) - 1
    raw = (val >> start_bit) & mask
    if signed and (raw & (1 << (length-1))):
        raw -= (1 << length)
    return raw

def _bit_extract_be(data_bytes, start_bit, length, signed=False):
    total_bits = len(data_bytes)*8
    val = int.from_bytes(data_bytes, 'big', signed=False)
    msb_index = total_bits - start_bit - length
    mask = (1 << length) - 1
    raw = (val >> msb_index) & mask
    if signed and (raw & (1 << (length-1))):
        raw -= (1 << length)
    return raw

class CanDecoder:
    def __init__(self, path=DEF_PATH):
        self.db = {}
        if os.path.exists(path):
            with open(path,'r',encoding='utf-8') as f:
                self.db = json.load(f)

    def decode(self, can_id_hex, data_bytes):
        out = {}
        entry = self.db.get(can_id_hex)
        if not entry: return out
        for sig in entry.get('Signals', []):
            bs = int(sig.get('BitStart',0)); ln = int(sig.get('Length',8))
            signed = bool(sig.get('Signed',False))
            endian = str(sig.get('Endianess','Intel')).lower()
            factor = float(sig.get('Factor',1.0)); offset = float(sig.get('Offset',0.0))
            raw = _bit_extract_le(data_bytes, bs, ln, signed) if 'intel' in endian or 'little' in endian else _bit_extract_be(data_bytes, bs, ln, signed)
            out[sig.get('SignalName','sig')] = raw*factor + offset
        return out

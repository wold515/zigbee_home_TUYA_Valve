
import struct, sys
def parse_hex(h_path):
    blocks = []
    with open(h_path, "r") as f:
        for line in f:
            if not line.startswith(":"): continue
            size = int(line[1:3], 16)
            addr = int(line[3:7], 16)
            kind = int(line[7:9], 16)
            if kind == 0:
                blocks.append((addr, bytes.fromhex(line[9:9+size*2])))
    return blocks
def make_uf2(h_path, out_path, start_addr):
    hex_data = parse_hex(h_path)
    all_bytes = bytearray()
    curr_addr = start_addr
    for addr, data in hex_data:
        all_bytes.extend(data)
    chunk_size = 256
    num_blocks = (len(all_bytes) + chunk_size - 1) // chunk_size
    with open(out_path, "wb") as f:
        for i in range(num_blocks):
            chunk = all_bytes[i*chunk_size:(i+1)*chunk_size]
            if len(chunk) < chunk_size: chunk += b"\x00" * (chunk_size - len(chunk))
            block = struct.pack("<4I", 0x0A324655, 0x9E5D5157, 0x00002000, curr_addr + i * chunk_size)
            block += struct.pack("<4I", chunk_size, i, num_blocks, 0xADA52840)
            block += chunk
            block += b"\x00" * (512 - len(block) - 4)
            block += struct.pack("<I", 0x0AB16F30)
            f.write(block)
make_uf2("./merged.hex", "./flash_this.uf2", 0x26000)
print("=== SUCCESS: Done ===")


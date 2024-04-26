class NinebotTEA:
    DEFAULT_KEY = b'\xFE\x80\x1C\xB2\xD1\xEF\x41\xA6\xA4\x17\x31\xF5\xA0\x68\x24\xF0'
    def __init__(self, key=None, iv=b'\x00' * 8):
        if key is None:
            key = self.DEFAULT_KEY
        self.key = [int.from_bytes(key[i:i+4], 'little') for i in range(0, 16, 4)]
        self.iv = int.from_bytes(iv, 'little')
        self.delta = 0x9E3779B9
        self.num_rounds = 32
        self.mask = 0xFFFFFFFF

    def _update_key(self, key):
        new_key = bytearray()
        # Convert the key to bytes for processing each byte individually
        key_bytes = b''.join(k.to_bytes(4, 'little') for k in key)
        for i in range(16):  # Assuming key is always 128 bits / 16 bytes long
            new_byte = (key_bytes[i] + i) & 0xFF
            new_key.append(new_byte)
        # Convert the updated bytearray back to the integer format used in this class
        return [int.from_bytes(new_key[i:i+4], 'little') for i in range(0, 16, 4)]

    def put_checksum_and_pad(self, data):
        # First, calculate how much padding is needed to align data to 4 bytes
        padding_needed = (4 - len(data) % 4) % 4
        data += bytes(padding_needed)  # Add zero bytes to align to 4 bytes

        if ((len(data) % 8) == 0): # if needed, pad before checksum
            data += b'\x00' * 4

        # Calculate checksum including the newly added padding
        checksum_value = self.checksum(data).to_bytes(4, 'little')
        data += checksum_value  # Append checksum

        return data

    def verify_and_unpad(self, data):
        """Verify checksum and remove it from data."""
        if len(data) < 4:
            raise ValueError("Data too short to contain a valid checksum.")

        # Extract checksum from the last 4 bytes
        provided_checksum = int.from_bytes(data[-4:], 'little')
        data_without_checksum = data[:-4]

        # Verify checksum
        if self.checksum(data_without_checksum) != provided_checksum:
            raise ValueError("Checksum does not match.")

        return data_without_checksum

    def checksum(self, data):
        sum_values = sum(int.from_bytes(data[i:i+4], 'little') for i in range(0, len(data), 4))
        sum_values = ((sum_values >> 16) & 0xFFFF) | ((sum_values & 0xFFFF) << 16)
        return sum_values ^ 0xFFFFFFFF

    def _encrypt_block(self, y, z, key):
        sum = 0
        for _ in range(self.num_rounds):
            sum = (sum + self.delta) & self.mask
            y = (y + (((z << 4) + key[0]) ^ (z + sum) ^ ((z >> 5) + key[1]))) & self.mask
            z = (z + (((y << 4) + key[2]) ^ (y + sum) ^ ((y >> 5) + key[3]))) & self.mask
        return y, z

    def _decrypt_block(self, y, z, key):
        sum = self.delta * self.num_rounds
        for _ in range(self.num_rounds):
            z = (z - (((y << 4) + key[2]) ^ (y + sum) ^ ((y >> 5) + key[3]))) & self.mask
            y = (y - (((z << 4) + key[0]) ^ (z + sum) ^ ((z >> 5) + key[1]))) & self.mask
            sum = (sum - self.delta) & self.mask
        return y, z

    def encrypt(self, data):
        data = self.put_checksum_and_pad(data)
        encrypted = bytearray()
        iv = self.iv
        key = self.key
        processed_bytes = 0
        for i in range(0, len(data), 8):
            if processed_bytes == 1024:
                key = self._update_key(key)
                processed_bytes = 0  # Reset the byte counter after updating the key
            block = int.from_bytes(data[i:i+8], 'little') ^ iv
            y, z = block & 0xFFFFFFFF, block >> 32
            ey, ez = self._encrypt_block(y, z, key)
            encrypted_block = (ez << 32) | ey
            encrypted.extend(encrypted_block.to_bytes(8, 'little'))
            iv = encrypted_block
            processed_bytes += 8
        return encrypted

    def decrypt(self, data):
        decrypted = bytearray()
        iv = self.iv
        key = self.key
        processed_bytes = 0
        for i in range(0, len(data), 8):
            if processed_bytes == 1024:
                key = self._update_key(key)
                processed_bytes = 0
            block = int.from_bytes(data[i:i+8], 'little')
            y, z = self._decrypt_block(block & 0xFFFFFFFF, block >> 32, key)
            decrypted_block = ((z << 32) | y) ^ iv
            decrypted.extend(decrypted_block.to_bytes(8, 'little'))
            iv = block
            processed_bytes += 8
        return self.verify_and_unpad(decrypted)

def encrypt_file(input_path, output_path, key):
    tea = NinebotTEA(key=key)
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        encrypted_data = tea.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        print(f"File encrypted successfully and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

def decrypt_file(input_path, output_path, key):
    tea = NinebotTEA(key=key)
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        decrypted_data = tea.decrypt(data)
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        print(f"File decrypted successfully and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Encrypt or decrypt files using the TEA algorithm.')
    parser.add_argument('operation', choices=['encrypt', 'decrypt'], help='Operation to perform')
    parser.add_argument('input_path', help='Path of the file to process')
    parser.add_argument('output_path', help='Path to save the processed file')
    parser.add_argument('--key', help='Encryption key as a hex string (e.g., "fe801cb2d1ef41a6a41731f5a06824f0"). Optional.')

    args = parser.parse_args()

    # Convert the key hex string to bytes if provided, otherwise use None to default to internal key
    key = bytes.fromhex(args.key) if args.key else None
    if args.key and len(key) != 16:
        print("Error: Key must be exactly 128 bits (32 hex characters).")
        sys.exit(1)

    if args.operation == 'encrypt':
        encrypt_file(args.input_path, args.output_path, key)
    elif args.operation == 'decrypt':
        decrypt_file(args.input_path, args.output_path, key)

if __name__ == '__main__':
    main()
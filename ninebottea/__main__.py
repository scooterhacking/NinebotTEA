from ninebottea import NinebotTEA


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

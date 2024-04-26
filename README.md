
### NinebotTEA

---

#### Project Overview

NinebotTEA is an open-source command-line tool and library designed for the encryption and decryption needs of Ninebot manufactured scooter firmware. It is based on the Tiny Encryption Algorithm (TEA), tailored specifically to meet the requirements of Ninebot scooter firmware.

#### Features

- Command-line interface for easy encryption and decryption of firmware data.
- Library capabilities for integration into scooter firmware development projects.
- Supports Ninebot scooters and Xiaomi scooters manufactured by Ninebot.
- Customizable encryption keys.
- Optimized for handling ZIP firmware archives.


#### Usage

**CLI Usage:**

Navigate to the directory containing NinebotTEA and use the command line as follows:

- **Encrypt Firmware Data:**

  ```bash
  python NinebotTEA.py encrypt <input_path> <output_path> --key <hex_key>
  ```

- **Decrypt Firmware Data:**

  ```bash
  python NinebotTEA.py decrypt <input_path> <output_path> --key <hex_key>
  ```

**Library Usage:**

For firmware development, include NinebotTEA in your project to aid in the creation of ready to flash firmware packages:

```python
from NinebotTEA import NinebotTEA

# Initialize the TEA algorithm with an optional key
tea = NinebotTEA(key=your_optional_bytes_key)

# To encrypt data
encrypted_data = tea.encrypt(data_to_encrypt)

# To decrypt data
decrypted_data = tea.decrypt(encrypted_data)
```
An example code of how complete firmware packages can be created with the aid of this library can be found [here](https://github.com/scooterhacking/fw-zip-package-v3/blob/main/Python/pack.py).

#### Examples

- **Encrypting Firmware Data via CLI:**

  ```bash
  python NinebotTEA.py encrypt firmware_original.bin firmware_encrypted.bin --key 1a2b3c4d5e6f7890a1b2c3d4e5f60708
  ```

- **Decrypting Firmware Data via CLI:**

  ```bash
  python NinebotTEA.py decrypt firmware_encrypted.bin firmware_decrypted.bin --key 1a2b3c4d5e6f7890a1b2c3d4e5f60708
  ```

- **Using in a Firmware Project:**

  ```python
  # Assuming tea is an instance of NinebotTEA
  encrypted_zip = tea.encrypt(zip_content)
  ```

#### Contributing

We encourage contributions from those knowledgeable in encryption, scooter firmware, and scooter hacking in general. To contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

#### License

Distributed under the MIT License. See `LICENSE` for more information.

#### Getting Help

For any issues or questions, especially related to the use of NinebotTEA with Ninebot and Xiaomi scooter firmware or ZIP firmware archives, please file an issue on the project's GitHub issue tracker, or reach out to us on [the ScooterHacking Assembly](https://t.me/scooterhackingassembly).

---

# Implementation and Comparison of two solutions to Yao's Millionaires’ Problem

## Project Intro
This project implemented two protocols to Yao's Millionaires' Problem. Both protocols are implemented with python.
1. Yao's protocol
- TO FILL
2. Ioannidis and Ananth's protocol
- Communication
    - communication takes place at localhost
- Oblivious Transfer
    - 1 to 2 oblivious transfer
    - RSA based
    - 2048 bit key size
    
## Usage
Denpendencies:
- cryptography
- pycryptodome
### Yao's protocol
TO FILL
### Ioannidis and Ananth's protocol
1. run ``` python3 alice.py``` first, and enter alice's number
2. run ``` python3 bob.py```, then enter bob's number
3. wait and the result will appear in a few seconds
4. Additional Notes:
    - Maximum Bit of number that support is defined in number_size file, which by default is 64. This number can be changed but make sure the number is less than half of the OT key size.
    - The RSA key used is defined in keypair.pem (private key) and in publickey.crt (public key).
    
## Reference
- Lecture 10 slides from Giovanni Di Crescenzo, Ph.D.
- Ioanidis and Ananth's protocol from https://ieeexplore.ieee.org/abstract/document/1174464
- RSA based 1 to 2 oblivious transfer from https://en.wikipedia.org/wiki/Oblivious_transfer

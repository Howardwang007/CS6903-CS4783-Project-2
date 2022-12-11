# Implementation of two solutions to Yao's Millionaires’ Problem

## Project Intro
This project implemented two protocols to Yao's Millionaires' Problem. Both protocols are implemented with python.
1. Yao's protocol
- Communication
    - via socket connection
    - Adopt congig.py support over 20 nodes
- Millionaire Problem Based
    - RSA key size is determined by the bit-size of the value being sent
2. Ioannidis and Ananth's protocol
- Communication
    - communication takes place at localhost
- Oblivious Transfer
    - 1 to 2 oblivious transfer
    - RSA based
    - 2048 bit key size
    
## Usage
Denpendencies:
- cryptography ```pip install cryptography```
- pycryptodome ```pip install pycryptodome```
### Yao's protocol
1. run ``` python3 server.py``` first, and enter server(RSU)'s coordinate number,
2. run ``` python3 alice.py```, then enter alice's coordinate number and distance between server
3. run ``` python3 bob.py```, lastly enter bob's coordinate number and distance between server
4. run ``` python3 performance.py```, to test performance automated or manually type value to debug
5. Additional Notes:
    - congig.py support add more nodes 
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

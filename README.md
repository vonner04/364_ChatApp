## HOW TO RUN

1. Clone the repository

   ```bash
   git clone https://github.com/vonner04/364_ChatApp.git
   ```

2. Open the 364_ChatApp folder in a terminal.

3. Paste the following lines in different terminals. For linux replace python with python3.

   ```bash
   python server.py
   ```

   ```bash
   python client.py
   ```

4. In python client.py terminal you will receive prompts for username and password.

5. Enter a desired user-name and password (case-sensitive)

**NOTE:** if you run into an error regard cert.pem and key.pem.

- delete cert.pem and key.pem

- regenerate new pem files by running the openssl config in terminal.

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -config openssl.cnf -nodes
```

run this following command to regenerate cert.pem and key.pem then do steps 3-5 again.

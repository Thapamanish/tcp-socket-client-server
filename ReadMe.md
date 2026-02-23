# TCP Client-Server Application

**Language:** Python 3

---

## Overview

This project implements a TCP client-server application where:
- The **server** accepts connections and encodes/decodes messages
- The **client** connects to the server and sends messages for processing
- Messages are encoded by shifting each character to the next ASCII character
- Optional decoding functionality is included

### Example
- **Original:** "Hello World"
- **Encoded:** "Ifmmp!Xpsme"

---

## Requirements

- Python 3.6 or higher
- No external libraries required (uses built-in `socket` module)
- Works on Windows, Linux, and macOS

---

## Installation

1. Extract the project files to a directory
2. Ensure both files have execute permissions (Linux/macOS):
   ```bash
   chmod +x tcp_server.py tcp_client.py
   ```

---

## User Instructions

### Starting the Server

#### Basic Usage (Default Port 12345)
```bash
python tcp_server.py
```

#### Custom Port
```bash
python tcp_server.py -p 8080
```

#### Listen on All Network Interfaces
```bash
python tcp_server.py -H 0.0.0.0 -p 12345
```

#### Server Help
```bash
python tcp_server.py -h
```

**Server Output Example:**
```
[SERVER] Server started successfully
[SERVER] Listening on 127.0.0.1:12345
[SERVER] Waiting for connections...
```

---

### Running the Client

#### Interactive Mode (Recommended for Testing)
```bash
python tcp_client.py
```

This starts an interactive session where you can:
- Type any message to encode it
- Type `decode <message>` to decode a message
- Type `quit` or `exit` to close the client

**Interactive Mode Example:**
```
Enter message: Hello World
[CLIENT] Connecting to server at 127.0.0.1:12345...
[CLIENT] Connected successfully
[CLIENT] Sending message: 'Hello World'
[CLIENT] Operation: ENCODE
[CLIENT] Waiting for response...

[RESPONSE] Server returned: 'Ifmmp!Xpsme'

Enter message: decode Ifmmp!Xpsme
[RESPONSE] Server returned: 'Hello World'

Enter message: quit
[CLIENT] Exiting...
```

#### Single Message Mode (Encode)
```bash
python tcp_client.py -m "Hello World"
```

#### Single Message Mode (Decode)
```bash
python tcp_client.py -m "Ifmmp!Xpsme" -d
```

#### Connect to Remote Server
```bash
python tcp_client.py -H 192.168.1.100 -p 8080 -m "Test Message"
```

#### Client Help
```bash
python tcp_client.py -h
```

---

## Command-Line Arguments

### Server Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--host` | `-H` | Host address to bind to | 127.0.0.1 |
| `--port` | `-p` | Port number to listen on | 12345 |
| `--help` | `-h` | Show help message | - |

### Client Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--host` | `-H` | Server host address | 127.0.0.1 |
| `--port` | `-p` | Server port number | 12345 |
| `--message` | `-m` | Message to send | None (interactive) |
| `--decode` | `-d` | Decode instead of encode | False |
| `--help` | `-h` | Show help message | - |

---

## Protocol Details

### Message Format

The client can send two types of messages:

1. **Encode Request (Default):**
   ```
   ENCODE:<your message>
   ```
   or simply:
   ```
   <your message>
   ```

2. **Decode Request:**
   ```
   DECODE:<your encoded message>
   ```

### Server Response

- **Success:** Returns the processed message
- **Error:** Returns message starting with "ERROR:"

### Maximum Message Length

- **256 characters** (enforced by both client and server)
- Messages exceeding this limit will be rejected

---

## Error Handling

Both programs include comprehensive error handling for:

### Server Errors
- Port already in use
- Invalid bind address
- Client connection errors
- Message length validation
- Character encoding errors

### Client Errors
- Server not running (connection refused)
- Connection timeout (10 seconds)
- Network errors
- Message length validation
- Invalid input

---

## Testing Instructions

### Test 1: Basic Encoding
1. Start the server: `python tcp_server.py`
2. In another terminal, run: `python tcp_client.py -m "Hello World"`
3. Expected output: `Ifmmp!Xpsme`

### Test 2: Basic Decoding
1. Server should still be running
2. Run: `python tcp_client.py -m "Ifmmp!Xpsme" -d`
3. Expected output: `Hello World`

### Test 3: Interactive Mode
1. Server should still be running
2. Run: `python tcp_client.py`
3. Type various messages and observe encoding
4. Type `decode <encoded_message>` to decode
5. Type `quit` to exit

### Test 4: Special Characters
1. Test with: `python tcp_client.py -m "Test123!@#"`
2. Expected output: `Uftu234\"A$`

### Test 5: Error Handling - Message Too Long
1. Create a message > 256 characters
2. Both client and server should reject it with appropriate error message

### Test 6: Error Handling - Server Not Running
1. Stop the server (Ctrl+C)
2. Try to run client
3. Expected: Connection refused error message

---

## Features Implemented

### Required Features ✓
- [x] TCP server that accepts client connections
- [x] Receives text messages up to 256 characters
- [x] Encodes messages by shifting ASCII characters
- [x] TCP client that connects to server
- [x] Client displays encoded response
- [x] Error checking and validation
- [x] Well-documented code
- [x] User instructions

### Optional Features ✓
- [x] Decode functionality with flag
- [x] Interactive mode for multiple messages
- [x] Command-line argument parsing
- [x] Comprehensive error messages
- [x] Connection timeout handling
- [x] Support for custom host/port configuration

---

## Architecture

### Server Design
```
1. Create TCP socket
2. Bind to host:port
3. Listen for connections
4. Accept client connection
5. Receive message
6. Validate message length
7. Process message (encode/decode)
8. Send response
9. Close client connection
10. Wait for next connection
```

### Client Design
```
1. Create TCP socket
2. Connect to server
3. Send message with operation flag
4. Receive response
5. Display result
6. Close connection
```

---

## Troubleshooting

### "Address already in use" Error
- Another process is using the port
- Wait a few seconds and try again, or use a different port:
  ```bash
  python tcp_server.py -p 12346
  ```

### "Connection refused" Error
- Server is not running
- Start the server first before running the client
- Check that host and port match between client and server

### "Connection timed out" Error
- Server is not responding
- Check firewall settings
- Verify server is running and listening on correct port

---

## Code Structure

```
tcp_server.py
├── encode_message()        # Shift ASCII characters forward
├── decode_message()        # Shift ASCII characters backward
├── process_client_message() # Determine encode/decode operation
├── handle_client()         # Handle individual client connection
├── start_server()          # Main server loop
└── main()                  # Parse arguments and start server

tcp_client.py
├── send_message()          # Connect to server and send message
├── interactive_mode()      # Interactive message sending loop
├── single_message_mode()   # Send one message and exit
└── main()                  # Parse arguments and run client
```

---

## Sample Output

### Server Output
```
[SERVER] Server started successfully
[SERVER] Listening on 127.0.0.1:12345
[SERVER] Waiting for connections...
------------------------------------------------------------

[CONNECTION] Client connected from 127.0.0.1:54321
[RECEIVED] Message: 'ENCODE:Hello World'
[INFO] Message length: 18 characters
[PROCESSED] Result: 'Ifmmp!Xpsme'
[SENT] Response sent to client
[CONNECTION] Connection closed with ('127.0.0.1', 54321)
------------------------------------------------------------
```

### Client Output
```
============================================================
TCP Client - Single Message Mode
============================================================
[CLIENT] Connecting to server at 127.0.0.1:12345...
[CLIENT] Connected successfully
[CLIENT] Sending message: 'Hello World'
[CLIENT] Operation: ENCODE
[CLIENT] Waiting for response...

============================================================
RESULT
============================================================
Original message: Hello World
Operation:        ENCODE
Server response:  Ifmpp!Xpsme
============================================================
```

---

## Limitations

- Maximum message length: 256 characters
- ASCII characters only (extended ASCII supported)
- One client connection handled at a time (sequential processing)
- Server must be manually restarted after shutdown

---

## Future Enhancements

- Multi-threaded server to handle concurrent clients
- Support for Unicode characters
- Message logging to file
- SSL/TLS encryption for secure communication
- Configurable encoding shift value

---

## References

- Beej's Guide to Network Programming: http://beej.us/guide/bgnet/
- Python Socket Programming: https://docs.python.org/3/library/socket.html
- ASCII Table: https://www.asciitable.com/

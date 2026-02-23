#!/usr/bin/env python3
"""
Demonstration script that simulates the TCP client-server interaction
without requiring two separate terminals.
"""

import socket
import threading
import time
import sys

# Server configuration
HOST = '127.0.0.1'
PORT = 12347  # Using different port to avoid conflicts
BUFFER_SIZE = 1024


def encode_message(message):
    """Encode by shifting ASCII characters forward"""
    return ''.join(chr(ord(char) + 1) for char in message)


def decode_message(message):
    """Decode by shifting ASCII characters backward"""
    return ''.join(chr(ord(char) - 1) for char in message)


def server_thread():
    """Run the server in a separate thread"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("[SERVER] Server started on {}:{}".format(HOST, PORT))
        print("[SERVER] Waiting for connections...\n")

        # Accept 5 test connections
        for i in range(5):
            client_socket, client_address = server_socket.accept()
            print("[SERVER] Client connected from {}:{}".format(
                client_address[0], client_address[1]))

            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            print("[SERVER] Received: '{}'".format(data))

            # Process the message
            if data.startswith("DECODE:"):
                result = decode_message(data[7:])
                operation = "DECODE"
            else:
                if data.startswith("ENCODE:"):
                    result = encode_message(data[7:])
                else:
                    result = encode_message(data)
                operation = "ENCODE"

            print("[SERVER] Operation: {}".format(operation))
            print("[SERVER] Sending: '{}'\n".format(result))

            client_socket.send(result.encode('utf-8'))
            client_socket.close()

    finally:
        server_socket.close()


def client_request(message, operation='encode'):
    """Send a single client request"""
    time.sleep(0.5)  # Wait for server to be ready

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("[CLIENT] Connecting to {}:{}...".format(HOST, PORT))
        client_socket.connect((HOST, PORT))
        print("[CLIENT] Connected!")

        # Prepare message
        if operation == 'decode':
            full_message = "DECODE:{}".format(message)
        else:
            full_message = "ENCODE:{}".format(message)

        print("[CLIENT] Sending: '{}'".format(message))
        print("[CLIENT] Operation: {}".format(operation.upper()))

        client_socket.send(full_message.encode('utf-8'))

        response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print("[CLIENT] Response: '{}'\n".format(response))

        return response

    finally:
        client_socket.close()


def main():
    """Run demonstration"""
    print("=" * 70)
    print("TCP CLIENT-SERVER DEMONSTRATION")
    print("=" * 70)
    print()

    # Start server in background thread
    server = threading.Thread(target=server_thread, daemon=True)
    server.start()

    time.sleep(1)  # Give server time to start

    # Test cases
    test_cases = [
        ("Hello World", "encode"),
        ("Test123!@#", "encode"),
        ("Ifmmp!Xpsme", "decode"),
        ("CS 576 Assignment", "encode"),
        ("DT!687!Bttjhonfou", "decode")
    ]

    print("Running {} test cases...\n".format(len(test_cases)))
    print("=" * 70)

    for i, (message, operation) in enumerate(test_cases, 1):
        print("\nTEST CASE {}".format(i))
        print("-" * 70)
        response = client_request(message, operation)
        print("-" * 70)

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nAll {} test cases executed successfully!".format(len(test_cases)))
    print("\nKey Features Demonstrated:")
    print("  ✓ Server accepts client connections")
    print("  ✓ Client sends messages to server")
    print("  ✓ Server encodes messages (shifts ASCII forward)")
    print("  ✓ Server decodes messages (shifts ASCII backward)")
    print("  ✓ Client receives and displays responses")
    print("  ✓ Multiple sequential connections handled")


if __name__ == '__main__':
    main()
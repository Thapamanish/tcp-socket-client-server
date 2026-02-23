#!/usr/bin/env python3
"""
CS 576 - Programming Assignment 1
TCP Server Implementation

This server accepts connections from clients, receives text messages (max 256 characters),
and encodes them by shifting each character to the next ASCII character.
Optional: Supports both encoding and decoding based on a flag.

Author: [Your Name]
Date: February 13, 2026
"""

import socket
import sys
import argparse

# Configuration constants
DEFAULT_PORT = 12345
DEFAULT_HOST = '127.0.0.1'
MAX_MESSAGE_LENGTH = 256
BUFFER_SIZE = 1024


def encode_message(message):
    """
    Encode a message by replacing each character with the next ASCII character.

    Args:
        message (str): The message to encode

    Returns:
        str: The encoded message

    Example:
        "Hello World" -> "Ifmmp!Xpsme"
    """
    try:
        encoded = ''.join(chr(ord(char) + 1) for char in message)
        return encoded
    except Exception as e:
        raise ValueError(f"Error encoding message: {e}")


def decode_message(message):
    """
    Decode a message by replacing each character with the previous ASCII character.

    Args:
        message (str): The message to decode

    Returns:
        str: The decoded message

    Example:
        "Ifmmp!Xpsme" -> "Hello World"
    """
    try:
        decoded = ''.join(chr(ord(char) - 1) for char in message)
        return decoded
    except Exception as e:
        raise ValueError(f"Error decoding message: {e}")


def process_client_message(message):
    """
    Process the client message and determine the operation (encode/decode).

    Protocol:
        - Messages starting with "DECODE:" will be decoded
        - All other messages will be encoded

    Args:
        message (str): The raw message from client

    Returns:
        str: The processed message
    """
    if message.startswith("DECODE:"):
        # Extract the actual message after the flag
        actual_message = message[7:]  # Remove "DECODE:" prefix
        return decode_message(actual_message)
    else:
        # Check if message starts with "ENCODE:" and remove it
        if message.startswith("ENCODE:"):
            actual_message = message[7:]  # Remove "ENCODE:" prefix
            return encode_message(actual_message)
        else:
            # Default behavior: encode
            return encode_message(message)


def start_server(host, port):
    """
    Start the TCP server and listen for client connections.

    Args:
        host (str): The host address to bind to
        port (int): The port number to listen on
    """
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket options to reuse address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind the socket to the address and port
        server_socket.bind((host, port))

        # Listen for incoming connections (max 5 queued connections)
        server_socket.listen(5)

        print(f"[SERVER] Server started successfully")
        print(f"[SERVER] Listening on {host}:{port}")
        print(f"[SERVER] Waiting for connections...")
        print("-" * 60)

        # Server loop - continuously accept connections
        while True:
            try:
                # Accept a client connection
                client_socket, client_address = server_socket.accept()
                print(f"\n[CONNECTION] Client connected from {client_address[0]}:{client_address[1]}")

                # Handle the client connection
                handle_client(client_socket, client_address)

            except KeyboardInterrupt:
                print("\n[SERVER] Shutting down server...")
                break
            except Exception as e:
                print(f"[ERROR] Error accepting connection: {e}")
                continue

    except OSError as e:
        print(f"[ERROR] Failed to bind to {host}:{port}")
        print(f"[ERROR] {e}")
        print("[INFO] Make sure the port is not already in use")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        sys.exit(1)
    finally:
        server_socket.close()
        print("[SERVER] Server socket closed")


def handle_client(client_socket, client_address):
    """
    Handle communication with a connected client.

    Args:
        client_socket: The socket object for the client connection
        client_address: The address tuple (host, port) of the client
    """
    try:
        # Receive data from the client
        data = client_socket.recv(BUFFER_SIZE).decode('utf-8')

        if not data:
            print(f"[WARNING] No data received from {client_address}")
            return

        # Validate message length
        if len(data) > MAX_MESSAGE_LENGTH:
            error_msg = f"ERROR: Message exceeds maximum length of {MAX_MESSAGE_LENGTH} characters"
            client_socket.send(error_msg.encode('utf-8'))
            print(f"[ERROR] Message too long from {client_address}: {len(data)} characters")
            return

        print(f"[RECEIVED] Message: '{data}'")
        print(f"[INFO] Message length: {len(data)} characters")

        # Process the message (encode or decode based on flag)
        try:
            response = process_client_message(data)
            print(f"[PROCESSED] Result: '{response}'")

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))
            print(f"[SENT] Response sent to client")

        except ValueError as e:
            error_msg = f"ERROR: {str(e)}"
            client_socket.send(error_msg.encode('utf-8'))
            print(f"[ERROR] Processing error: {e}")

    except UnicodeDecodeError:
        error_msg = "ERROR: Invalid character encoding"
        client_socket.send(error_msg.encode('utf-8'))
        print(f"[ERROR] Encoding error from {client_address}")
    except Exception as e:
        print(f"[ERROR] Error handling client {client_address}: {e}")
    finally:
        # Close the client connection
        client_socket.close()
        print(f"[CONNECTION] Connection closed with {client_address}")
        print("-" * 60)


def main():
    """
    Main function to parse arguments and start the server.
    """
    parser = argparse.ArgumentParser(
        description='TCP Server for CS 576 Programming Assignment 1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tcp_server.py                    # Start server on default port 12345
  python tcp_server.py -p 8080           # Start server on port 8080
  python tcp_server.py -H 0.0.0.0 -p 9000  # Listen on all interfaces, port 9000

Protocol:
  - Send "ENCODE:<message>" to encode (or just send message directly)
  - Send "DECODE:<message>" to decode
        """
    )

    parser.add_argument('-H', '--host',
                        default=DEFAULT_HOST,
                        help=f'Host address to bind to (default: {DEFAULT_HOST})')
    parser.add_argument('-p', '--port',
                        type=int,
                        default=DEFAULT_PORT,
                        help=f'Port number to listen on (default: {DEFAULT_PORT})')

    args = parser.parse_args()

    # Validate port number
    if not (1024 <= args.port <= 65535):
        print("[ERROR] Port number must be between 1024 and 65535")
        sys.exit(1)

    # Start the server
    start_server(args.host, args.port)


if __name__ == '__main__':
    main()

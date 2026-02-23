#!/usr/bin/env python3
"""
CS 576 - Programming Assignment 1
TCP Client Implementation

This client connects to the TCP server, sends a text message (max 256 characters),
and displays the encoded/decoded response from the server.

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


def send_message(host, port, message, operation='encode'):
    """
    Connect to the server and send a message for encoding/decoding.

    Args:
        host (str): The server host address
        port (int): The server port number
        message (str): The message to send
        operation (str): Either 'encode' or 'decode'

    Returns:
        str: The response from the server, or None if error occurred
    """
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set timeout to avoid hanging indefinitely
    client_socket.settimeout(10)

    try:
        print(f"[CLIENT] Connecting to server at {host}:{port}...")

        # Connect to the server
        client_socket.connect((host, port))
        print(f"[CLIENT] Connected successfully")

        # Prepare the message with operation flag
        if operation.lower() == 'decode':
            full_message = f"DECODE:{message}"
        else:
            full_message = f"ENCODE:{message}"

        print(f"[CLIENT] Sending message: '{message}'")
        print(f"[CLIENT] Operation: {operation.upper()}")

        # Send the message to the server
        client_socket.send(full_message.encode('utf-8'))

        print("[CLIENT] Waiting for response...")

        # Receive the response from the server
        response = client_socket.recv(BUFFER_SIZE).decode('utf-8')

        if response.startswith("ERROR:"):
            print(f"[ERROR] Server returned error: {response}")
            return None

        return response

    except socket.timeout:
        print("[ERROR] Connection timed out - server did not respond")
        return None
    except ConnectionRefusedError:
        print(f"[ERROR] Connection refused - server is not running on {host}:{port}")
        print("[INFO] Please start the server first")
        return None
    except OSError as e:
        print(f"[ERROR] Network error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return None
    finally:
        client_socket.close()


def interactive_mode(host, port):
    """
    Run the client in interactive mode, allowing multiple messages.

    Args:
        host (str): The server host address
        port (int): The server port number
    """
    print("=" * 60)
    print("TCP Client - Interactive Mode")
    print("=" * 60)
    print(f"Server: {host}:{port}")
    print(f"Maximum message length: {MAX_MESSAGE_LENGTH} characters")
    print("\nCommands:")
    print("  - Type your message to encode it")
    print("  - Type 'decode' followed by message to decode")
    print("  - Type 'quit' or 'exit' to close the client")
    print("=" * 60)

    while True:
        try:
            # Get user input
            user_input = input("\nEnter message: ").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("[CLIENT] Exiting...")
                break

            # Skip empty input
            if not user_input:
                print("[WARNING] Please enter a message")
                continue

            # Parse operation and message
            operation = 'encode'
            message = user_input

            if user_input.lower().startswith('decode '):
                operation = 'decode'
                message = user_input[7:]  # Remove 'decode ' prefix

            # Validate message length
            if len(message) > MAX_MESSAGE_LENGTH:
                print(f"[ERROR] Message exceeds maximum length of {MAX_MESSAGE_LENGTH} characters")
                print(f"[INFO] Your message is {len(message)} characters long")
                continue

            # Send the message and get response
            response = send_message(host, port, message, operation)

            if response:
                print(f"\n[RESPONSE] Server returned: '{response}'")
                print(f"[INFO] Response length: {len(response)} characters")

        except KeyboardInterrupt:
            print("\n[CLIENT] Interrupted by user, exiting...")
            break
        except EOFError:
            print("\n[CLIENT] End of input, exiting...")
            break


def single_message_mode(host, port, message, operation):
    """
    Send a single message and exit.

    Args:
        host (str): The server host address
        port (int): The server port number
        message (str): The message to send
        operation (str): Either 'encode' or 'decode'
    """
    print("=" * 60)
    print("TCP Client - Single Message Mode")
    print("=" * 60)

    # Validate message length
    if len(message) > MAX_MESSAGE_LENGTH:
        print(f"[ERROR] Message exceeds maximum length of {MAX_MESSAGE_LENGTH} characters")
        print(f"[INFO] Your message is {len(message)} characters long")
        sys.exit(1)

    # Send the message and get response
    response = send_message(host, port, message, operation)

    if response:
        print(f"\n{'=' * 60}")
        print("RESULT")
        print(f"{'=' * 60}")
        print(f"Original message: {message}")
        print(f"Operation:        {operation.upper()}")
        print(f"Server response:  {response}")
        print(f"{'=' * 60}")
    else:
        sys.exit(1)


def main():
    """
    Main function to parse arguments and run the client.
    """
    parser = argparse.ArgumentParser(
        description='TCP Client for CS 576 Programming Assignment 1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tcp_client.py                           # Interactive mode
  python tcp_client.py -m "Hello World"          # Send single message (encode)
  python tcp_client.py -m "Ifmmp!Xpsme" -d       # Send single message (decode)
  python tcp_client.py -H 192.168.1.100 -p 8080  # Connect to remote server

Interactive Mode:
  If no message is provided with -m, the client runs in interactive mode
  where you can send multiple messages.
        """
    )

    parser.add_argument('-H', '--host',
                        default=DEFAULT_HOST,
                        help=f'Server host address (default: {DEFAULT_HOST})')
    parser.add_argument('-p', '--port',
                        type=int,
                        default=DEFAULT_PORT,
                        help=f'Server port number (default: {DEFAULT_PORT})')
    parser.add_argument('-m', '--message',
                        help='Message to send (if not provided, runs in interactive mode)')
    parser.add_argument('-d', '--decode',
                        action='store_true',
                        help='Decode the message instead of encoding')

    args = parser.parse_args()

    # Validate port number
    if not (1024 <= args.port <= 65535):
        print("[ERROR] Port number must be between 1024 and 65535")
        sys.exit(1)

    # Determine operation
    operation = 'decode' if args.decode else 'encode'

    # Run in appropriate mode
    if args.message:
        # Single message mode
        single_message_mode(args.host, args.port, args.message, operation)
    else:
        # Interactive mode
        interactive_mode(args.host, args.port)


if __name__ == '__main__':
    main()
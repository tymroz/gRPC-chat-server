import argparse
import sys
import threading

import grpc

import chat_pb2
import chat_pb2_grpc


def listen_for_messages(stub: chat_pb2_grpc.ChatServerStub) -> None:
    try:
        responses = stub.ChatStream(chat_pb2.Empty())
        for note in responses:
            print(f"[{note.name}] {note.message}")
    except grpc.RpcError:
        print("\nLost connection to server.")


def run(host: str, port: int, name: str) -> None:
    address: str = f"{host}:{port}"
    channel: grpc.Channel = grpc.insecure_channel(address)
    stub: chat_pb2_grpc.ChatServerStub = chat_pb2_grpc.ChatServerStub(channel)

    listener_thread: threading.Thread = threading.Thread(
        target=listen_for_messages,
        args=(stub,),
        daemon=True,
    )
    listener_thread.start()

    print("Type a message and press Enter (type 'quit' to exit)")

    try:
        while True:
            message: str = input()
            if message.lower() == "quit":
                break
            if message:
                note: chat_pb2.Note = chat_pb2.Note(name=name, message=message)
                stub.SendNote(note)
    except KeyboardInterrupt:
        pass
    finally:
        print("Leaving chat...")
        channel.close()
        sys.exit(0)


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Run gRPC chat client")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server IP address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Server port (default: 8080)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="UnknownUser",
        help="Username `(default: UnknownUser)",
    )
    args: argparse.Namespace = parser.parse_args()
    run(args.host, args.port, args.name)


if __name__ == "__main__":
    main()

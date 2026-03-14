import argparse
import queue
from concurrent import futures

import grpc

import chat_pb2
import chat_pb2_grpc


class ChatServer(chat_pb2_grpc.ChatServerServicer):
    def __init__(self) -> None:
        self.clients: list[queue.Queue[chat_pb2.Note]] = []

    def ChatStream(
        self,
        request: chat_pb2.Empty,
        context: grpc.ServicerContext,
    ) -> chat_pb2.Note:
        client_queue: queue.Queue[chat_pb2.Note] = queue.Queue()
        self.clients.append(client_queue)
        print("New client joined the chat.")

        try:
            while context.is_active():
                try:
                    note: chat_pb2.Note = client_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                yield note
        finally:
            self.clients.remove(client_queue)
            print("Client left the chat.")

    def SendNote(
        self,
        request: chat_pb2.Note,
        context: grpc.ServicerContext,
    ) -> chat_pb2.Empty:
        print(f"[{request.name}] {request.message}")
        for q in self.clients:
            q.put(request)
        return chat_pb2.Empty()


def serve(port: int) -> None:
    address: str = f"[::]:{port}"
    server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServerServicer_to_server(ChatServer(), server)
    server.add_insecure_port(address)
    try:
        server.start()
        print(f"Chat server running on port {port}...")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Run gRPC chat server")
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to listen on (default: 8080)",
    )
    args: argparse.Namespace = parser.parse_args()
    serve(args.port)


if __name__ == "__main__":
    main()

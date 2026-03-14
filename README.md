# gRPC Chat Server

A simple gRPC-based chat server and client in Python.

## Building

Install dependencies:

```bash
uv sync
```

Generate gRPC code from proto:

```bash
uv run python -m grpc_tools.protoc -I proto --python_out=src --grpc_python_out=src proto/chat.proto
```

## Running the Server

```bash
uv run python src/server.py --port <port number>
```

Options:
- `--port` - port to listen on (default: 8080)

## Running the Client

```bash
uv run python src/client.py --host <server ip address> --port <port number> --name <username>
```

Options:
- `--host` - server IP address (default: localhost)
- `--port` - server port (default: 8080)
- `--name` - username (default: UnknownUser)

Type messages and press Enter to send. Type `quit` to exit.

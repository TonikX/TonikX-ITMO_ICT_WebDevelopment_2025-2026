import socket
import time

HOST = "127.0.0.1"
PORT = 14900
BUFFER_SIZE = 1024
IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM


def pythagorean_theorem(operands):
    a, b = operands
    a = float(a)
    b = float(b)
    return str((a * a + b * b) ** 0.5)


def quadratic_equation(operands):
    a, b, c = map(float, operands)
    delta = b * b - 4 * a * c
    if delta < 0:
        return "The equation has no real root."
    elif delta == 0:
        return str(-b / (2 * a))
    else:
        x1 = (-b + delta**0.5) / (2 * a)
        x2 = (-b - delta**0.5) / (2 * a)
        return f"x1 = {x1}\t,\tx2 = {x2}"


def trapezoid(operands):
    a, b, h = map(float, operands)
    s = (a + b) * h / 2
    return str(s)


def parallelogram(operands):
    a, h = map(float, operands)
    return str(a * h)


def handle_request(req):

    operation_str, operands_str = req.split(";", 1)
    operation = int(operation_str)
    operands = operands_str.split(",")

    match operation:
        case 1:
            return pythagorean_theorem(operands)
        case 2:
            return quadratic_equation(operands)
        case 3:
            return trapezoid(operands)
        case 4:
            return parallelogram(operands)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    server_socket.setblocking(False)

    print(f"Server started on {HOST}:{PORT}")
    print("Press Ctrl+C to stop the server\n")

    try:
        while True:

            client_socket = None
            client_address = None

            try:
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                print(f"New connection from {client_address}")

                try:
                    data = client_socket.recv(BUFFER_SIZE)
                    if data:
                        response = handle_request(data.decode("utf-8"))
                        client_socket.send(response.encode())
                        print(f"\033[92mResponse sent to {client_address}\033[0m")

                except BlockingIOError:
                    print(f"No data from {client_address}")
                except Exception as e:
                    print(f"Error processing {client_address}: {e}")

                finally:
                    client_socket.close()
                    print(f"\033[91mConnection {client_address} closed\033[0m \n")

            except BlockingIOError:
                time.sleep(0.1)
                continue

            except Exception as e:
                print(f"Error accepting connection: {e}")
                if client_socket:
                    client_socket.close()

    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        server_socket.close()
        print("SERVER STOPPED.")


if __name__ == "__main__":
    main()

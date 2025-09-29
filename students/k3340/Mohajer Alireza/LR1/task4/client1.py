import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(f"\r{message}\n{username}: ", end="", flush=True)
        except:
            print("\rThe connection is broken!")
            client_socket.close()
            break


def start_client(host="localhost", port=14905):
    global username
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))

        username_request = client_socket.recv(1024).decode("utf-8")
        if username_request == "USERNAME":
            username = input("Enter username : ")
            client_socket.send(username.encode("utf-8"))

        receive_thread = threading.Thread(
            target=receive_messages, args=(client_socket,)
        )
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input(f"{username}: ")
            if message.lower() == "quit":

                break
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                print("Error sending the message!")
                break

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()

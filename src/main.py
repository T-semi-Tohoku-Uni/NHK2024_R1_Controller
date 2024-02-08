import socket

def send_udp_message(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip, port))
    print(f"Sent message: {message} to {ip}:{port}")

    # サーバーからの応答を受信する場合は以下のコメントを外す
    # data, addr = sock.recvfrom(1024)
    # print(f"Received response: {data} from {addr}")

if __name__ == "__main__":
    send_udp_message("raspberrypi.local", 12345, "Hello UDP Server")
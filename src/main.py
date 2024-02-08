import socket
import pygame
import json
from typing import Dict
import multiprocessing

class ControllerData:
    def __init__(
        self,
        joy_lx: int,
        joy_ly: int,
        btn_a: int,
        btn_b: int,
        btn_x: int,
        btn_y: int,
    ):
        self.joy_lx = joy_lx
        self.joy_ly = joy_ly
        self.btn_a = btn_a
        self.btn_b = btn_b
        self.btn_x = btn_x
        self.btn_y = btn_y

# ジョイスティックの出力数値を調整
def map_axis(val):
    val = round(val, 2)
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def send_udp_message(ip: str, port: int, message: Dict[str, int]):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip, port))
    print(f"Sent message: {message} to {ip}:{port}")

if __name__ == "__main__":
    #　サーバーの設定
    host_name: str = "raspberrypi.local"
    port: int = 12345
    
    print("Server Setting")
    print(f"Host Name: {host_name}")
    print(f"Port: {port}")
    
    #　コントローラの設定(pygameの初期化)
    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    # 前回の値（他のボタンの割り込みが起こった時に無視するため）
    last_ctr_data = ControllerData(
        joy_lx = 0,
        joy_ly = 0,
        btn_a = 0,
        btn_b = 0,
        btn_x = 0,
        btn_y = 0,
    )
    
    try:
        while True:
            if pygame.event.get():
                ctr_data = ControllerData(
                    joy_lx = map_axis(joystick.get_axis(0)),   # 左スティックx座標 (-100 to 100)
                    joy_ly = -map_axis(joystick.get_axis(1)),  # 左スティックy座標 (-100 to 100)
                    btn_a = joystick.get_button(0),            # Aボタン   (0 or 1)
                    btn_b = joystick.get_button(1),            # Bボタン   (0 or 1)
                    btn_x = joystick.get_button(2),            # Xボタン   (0 or 1)
                    btn_y = joystick.get_button(3),            # Yボタン   (0 or 1)
                )
                # 前回の値と比較. 同じだったら通信しない
                if ctr_data.__dict__ == last_ctr_data.__dict__:
                    continue
                
                # send_udp_message(host_name, port, json.dumps(ctr_data.__dict__)) # ラズパイに送信
                last_ctr_data = ctr_data # 前回の値を更新
                
                p = multiprocessing.Process(target=send_udp_message, args=(host_name, port, json.dumps(ctr_data.__dict__))) # データの送信
                p.start()                
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
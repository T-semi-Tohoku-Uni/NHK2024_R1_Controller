import socket
import pygame
import json
from typing import Dict
import multiprocessing
import math

class ControllerData:
    def __init__(
        self,
        v_x: int,
        v_y: int,
        omega: int,
        btn_a: int,
        btn_b: int,
        btn_x: int,
        btn_y: int,
        btn_lb: int,
        btn_rb: int,
        start_btn: int,
    ):
        self.v_x = v_x
        self.v_y = v_y
        self.omega = omega
        self.btn_a = btn_a
        self.btn_b = btn_b
        self.btn_x = btn_x
        self.btn_y = btn_y
        self.btn_lb = btn_lb
        self.btn_rb = btn_rb
        self.start_btn = start_btn

# ジョイスティックの出力数値を調整
def map_axis(val):
    val = round(val, 2)
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def validate(input: float):
    if (-0.3 < input and input < 0) or (0 < input and input < 0.3):
        return 0
    else:
        return input

def speed_x(p_x):
    v_x = round(p_x, 2) # -1 to 1
    v_x = validate(v_x) # if -0.3 < v_x < 0.3,  v_x => 0
    return int((v_x + 1) * (255 / 2))

def speed_y(p_y):
    v_y = round(-p_y, 2)
    v_y = validate(v_y) # if -0.3 < v_y < 0.3, v_y => 0
    return int((v_y + 1) * (255 / 2))

def cac_omega(o):
    o = round(o, 2)
    o = validate(o)
    return int((o + 1) * (255 / 2))

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
        v_x = 0,
        v_y = 0,
        omega = 0,
        btn_a = 0,
        btn_b = 0,
        btn_x = 0,
        btn_y = 0,
        btn_lb = 0,
        btn_rb = 0,
        start_btn=0,
    )
    
    try:
        while True:
            if pygame.event.get():
                p_x = joystick.get_axis(0)
                p_y = joystick.get_axis(1)
                o = joystick.get_axis(2)
                ctr_data = ControllerData(
                    v_x = speed_x(p_x),   # 左スティックx座標 (-100 to 100)
                    v_y = speed_y(p_y),  # 左スティックy座標 (-100 to 100)
                    omega = cac_omega(o),
                    btn_a = joystick.get_button(0),            # Aボタン   (0 or 1)
                    btn_b = joystick.get_button(1),            # Bボタン   (0 or 1)
                    btn_x = joystick.get_button(2),            # Xボタン   (0 or 1)
                    btn_y = joystick.get_button(3),            # Yボタン   (0 or 1)
                    btn_lb =  joystick.get_button(4),  
                    btn_rb = joystick.get_button(5),
                    start_btn = joystick.get_button(11), # Startボタン (0 or 1)
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
import pygame


# pygame初期化
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


# ジョイスティックの出力数値を調整
def map_axis(val):
    val = round(val, 2)
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# ジョイスティックの出力数値を調整(L2 R2ボタン)
def map_axis_t(val):
    val = map_axis(val)
    if val <= 0 and val >= -100:
        in_min = -100
        in_max = 0
        out_min = 0
        out_max = 50
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    else:
        in_min = 0
        in_max = 100
        out_min = 50
        out_max = 100
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def main():
    while True:
        # イベントチェック
        if pygame.event.get():
            gamepad_data = {
                "joy_lx": map_axis(joystick.get_axis(0)),   # 左スティックx座標 (-100 to 100)
                "joy_ly": -map_axis(joystick.get_axis(1)),  # 左スティックy座標 (-100 to 100)
                "joy_rx": map_axis(joystick.get_axis(3)),   # 右スティックx座標 (-100 to 100)
                "joy_ry": -map_axis(joystick.get_axis(4)),  # 右スティックy座標 (-100 to 100)
                "joy_lt": map_axis_t(joystick.get_axis(2)), # LT/7 (0 to 100)
                # "joy_rt": map_axis_t(joystick.get_axis(5)), # RT/8 (0 to 100)
                "hat_x": joystick.get_hat(0)[0],            # 十時左右  (-1 or 1)
                "hat_y": joystick.get_hat(0)[1],            # 十時上下  (-1 or 1)
                "btn_a": joystick.get_button(0),            # Aボタン   (0 or 1)
                "btn_b": joystick.get_button(1),            # Bボタン   (0 or 1)
                "btn_x": joystick.get_button(2),            # Xボタン   (0 or 1)
                "btn_y": joystick.get_button(3),            # Yボタン   (0 or 1)
                "btn_lb": joystick.get_button(4),           # LB/5     (0 or 1)
                "btn_rb": joystick.get_button(5),           # RB/6     (0 or 1)
                "btn_back": joystick.get_button(6),
                "btn_start": joystick.get_button(7),
                "btn_guide": joystick.get_button(8),
                "btn_joyl": joystick.get_button(9),         # ない？
                "btn_joyr": joystick.get_button(10),         # ない?
                "start_btn" : joystick.get_button(11) 
            }
            print(gamepad_data)


if __name__ == '__main__':
    main()
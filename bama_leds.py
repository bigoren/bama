import json

#enum AnimationMode {
#  AnimationModeClear = 0,
#  AnimationModeConfetti = 1,
#  AnimationModeFill = 2,
#  AnimationModeMovingSegments = 3,
#  AnimationModeRainbow = 4,
#};


def fill_msg(led_percent=0, led_color=100, animation_mode=0):
    data = {"led_percent" : led_percent/100, "led_color" : led_color, "animation_mode" : animation_mode}
    msg = json.dumps(data)
    return msg

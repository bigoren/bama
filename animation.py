import functions_pb2
import effects_pb2
import animation_pb2


def fill_msg():
    timed_animation = animation_pb2.TimedAnimationProto()
    animation = timed_animation.animation
    # animation = effects_pb2.AnimationProto()
    animation.duration_ms = 5000
    animation.num_repeats = 0

    effect = animation.effects.add()
    effect.effect_config.start_time = 0
    effect.effect_config.end_time = 1000
    effect.rainbow.hue_start.linear.start = 0.0
    effect.rainbow.hue_start.linear.end = 1.0
    effect.rainbow.hue_end.linear.start = 1.0
    effect.rainbow.hue_end.linear.end = 2.0
    #
    # effect = animation.effects.add()
    # effect.effect_config.start_time = 1000
    # effect.effect_config.end_time = 2000
    # effect.rainbow.hue_start.const_value.value = 0.0
    # effect.rainbow.hue_end.const_value.value = 1.0

    # effect = animation.effects.add()
    # effect.effect_config.start_time = 2000
    # effect.effect_config.end_time = 3000
    # effect.const_color.color.hue = 0.5
    # effect.const_color.color.sat = 1.0
    # effect.const_color.color.val = 1.0
    #
    # effect = animation.effects.add()
    # effect.effect_config.start_time = 4000
    # effect.effect_config.end_time = 5000
    # effect.const_color.color.hue = 0.1
    # effect.const_color.color.sat = 1.0
    # effect.const_color.color.val = 1.0

    msg = timed_animation.SerializeToString()
    print(len(msg))
    print(", ".join(str(c) for c in msg))
    return msg

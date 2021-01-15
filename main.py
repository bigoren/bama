# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import asyncio
from asyncio_mqtt import Client, MqttError
import animation
import bama_leds
import json
from statemachine import StateMachine, State


class BamaSM(StateMachine):
    empty = State('Empty', initial=True)
    present = State('Present')
    full = State('Full')

    stepped = empty.to(present)
    big_jump = empty.to(full)
    overload = present.to(full)
    cleared = present.to(empty)
    jump_end = full.to(present)
    hop_off = full.to(empty)


empty_thr = 5
present_low_thr = 50
present_high_thr = 90
full_thr = 200
jump_thr = 30
weight_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

bama_sm = BamaSM()

thing_name = "amir-test"
mqtt_topic = "animations/" + thing_name
mqtt_topic_bama = "sensors/bama/load"
mqtt_topic_leds = "sensors/bama/leds"


# async def main():
#     async with Client("10.0.0.200") as client:
#         while True:
#             msg = animation.fill_msg()
#             await client.publish(mqtt_topic, msg, qos=1)
#             await asyncio.sleep(2)

# async def main():
#     led_percent = 0
#     async with Client("192.168.1.26") as client:
#         while True:
#             led_percent = (led_percent + 10) % 100
#             msg = bama_leds.fill_msg(led_percent, 100, 2)
#             await client.publish(mqtt_topic_leds, msg, qos=1)
#             await asyncio.sleep(2)
#             print (led_percent)

async def main():
    #async with Client("10.0.0.200") as client:
    async with Client("192.168.1.26") as client:
        await client.subscribe(mqtt_topic_bama)
        msg = bama_leds.fill_msg(0, 100, 0)
        await client.publish(mqtt_topic_leds, msg, qos=1)
        async with client.filtered_messages(mqtt_topic_bama) as messages:
            async for message in messages:
                bama_msg = json.loads(message.payload.decode())
                weight = 0
                if bama_msg:
                    weight = int(bama_msg["weight"])
                    #print(weight)
                    weight_log.append(weight)
                    weight_log.pop(0)
                    #print(*weight_log, sep=", ")

                if bama_sm.is_present:
                    weight_log_start = weight_log[0:5]
                    weight_log_mid = weight_log[6:12]
                    weight_log_end = weight_log[13:19]
                    start_max = max(weight_log_start)
                    #print('start_max', start_max)
                    mid_min = min(weight_log_mid)
                    #print('mid_min', mid_min)
                    end_max = max(weight_log_end)
                    #print('end_max', end_max)
                    #print(*weight_log, sep=", ")
                    if ((start_max-mid_min) > jump_thr) and ((end_max-mid_min) > jump_thr):
                        print('jump occurred')
                        msg = bama_leds.fill_msg(100, 100, 2)
                        await client.publish(mqtt_topic_leds, msg, qos=1)
                        await asyncio.sleep(0.2)
                    else:
                        msg = bama_leds.fill_msg(0, 100, 0)
                        await client.publish(mqtt_topic_leds, msg, qos=1)

                # decide_state(weight)
                if bama_sm.is_empty & (weight >= present_low_thr) & (weight < full_thr):
                    bama_sm.stepped()
                    print(bama_sm.current_state)
                elif bama_sm.is_empty & (weight >= full_thr):
                    bama_sm.big_jump()
                    print(bama_sm.current_state)
                elif bama_sm.is_present & (weight >= full_thr):
                    bama_sm.overload()
                    print(bama_sm.current_state)
                elif bama_sm.is_present & (weight < empty_thr):
                    bama_sm.cleared()
                    print(bama_sm.current_state)
                elif bama_sm.is_full & (weight < present_high_thr) & (weight > present_low_thr):
                    bama_sm.jump_end()
                    msg = bama_leds.fill_msg(0, 100, 0)
                    await client.publish(mqtt_topic_leds, msg, qos=1)
                    print(bama_sm.current_state)
                elif bama_sm.is_full & (weight < empty_thr):
                    bama_sm.hop_off()
                    print(bama_sm.current_state)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Change to the "Selector" event loop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Run your async application as usual
    asyncio.run(main())

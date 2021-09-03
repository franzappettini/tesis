import nidaqmx
import time

while True:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        print(task.read())
        time.sleep(1)

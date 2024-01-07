import asyncio
from kasa import SmartPlug
import datetime

IP = "192.168.50.250"
run_time = datetime.timedelta(minutes=5)
run_every = datetime.timedelta(minutes=60)


async def main():
    last_on = datetime.datetime(2000, 1, 1)
    dev = SmartPlug(IP)
    while True:
        await dev.update()
        now = datetime.datetime.now()
        if dev.is_on:
            running = now - dev.on_since
            print(running)
            if running > run_time:
                print("Turning off")
                await dev.turn_off()
                last_on = now
        elif now - last_on > run_every:
            print("Turning on")
            await dev.turn_on()

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())

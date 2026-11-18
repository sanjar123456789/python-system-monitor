import time
from datetime import datetime

while True:

    with open("background_demo.log", "a") as log_file:

        log_file.write(
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | Monitor is running\n"
        )

    time.sleep(10)

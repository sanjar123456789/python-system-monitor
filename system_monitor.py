import psutil
from datetime import datetime

def check_status(value, warning, critical):
    if value >= critical:
        return "CRITICAL"
    elif value >= warning:
        return "WARNING"
    else:
        return "NORMAL"

# CPU monitoring
cpu_usage = psutil.cpu_percent(interval=1)

# RAM monitoring
ram_usage = psutil.virtual_memory().percent

print("\n--- SYSTEM MONITOR ---")

print(f"CPU Usage: {cpu_usage}%")
print(f"CPU Status: {check_status(cpu_usage, 70, 90)}")

print(f"RAM Usage: {ram_usage}%")
print(f"RAM Status: {check_status(ram_usage, 70, 90)}")

# Disk monitoring
disk_usage = psutil.disk_usage('/').percent

print(f"Disk Usage: {disk_usage}%")
print(f"Disk Status: {check_status(disk_usage, 70, 90)}")
# Monitoring log

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

report = (
    f"{timestamp} | "
    f"CPU: {cpu_usage}% [{check_status(cpu_usage, 70, 90)}] | "
    f"RAM: {ram_usage}% [{check_status(ram_usage, 70, 90)}] | "
    f"DISK: {disk_usage}% [{check_status(disk_usage, 70, 90)}]"
)

with open("monitor.log", "a") as file:
    file.write(report + "\n")

print("Log saved successfully!")

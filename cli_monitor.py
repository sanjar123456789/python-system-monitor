import argparse
import psutil
import logging
from datetime import datetime

logging.basicConfig(
    filename="cli_monitor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_status(value, warning, critical):
    if value >= critical:
        return "CRITICAL"
    elif value >= warning:
        return "WARNING"
    else:
        return "NORMAL"


def collect_metrics(resource):
    metrics = {}

    if resource in ("cpu", "all"):
        metrics["CPU"] = psutil.cpu_percent(interval=1)

    if resource in ("ram", "all"):
        metrics["RAM"] = psutil.virtual_memory().percent

    if resource in ("disk", "all"):
        metrics["DISK"] = psutil.disk_usage("/").percent

    return metrics


def main():
    parser = argparse.ArgumentParser(
        description="DevOps System Monitoring Tool"
    )

    parser.add_argument(
        "--resource",
        choices=["cpu", "ram", "disk", "all"],
        default="all",
        help="Choose resource to monitor"
    )

    parser.add_argument(
        "--show-time",
        action="store_true",
        help="Show current date and time"
    )

    args = parser.parse_args()

    try:
        metrics = collect_metrics(args.resource)

    except (OSError, psutil.Error) as error:
        logging.exception("Monitoring failed")
        print("ERROR:", error)
        return

    print("\nSYSTEM MONITORING REPORT")

    if args.show_time:
        print(
            "Time:",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    thresholds = {
        "CPU": (70, 90),
        "RAM": (80, 90),
        "DISK": (80, 95)
    }

    for name, value in metrics.items():
        warning, critical = thresholds[name]
        status = get_status(value, warning, critical)

        message = f"{name}: {value:.1f}% [{status}]"

        print(message)
        logging.info(message)


if __name__ == "__main__":
    main()

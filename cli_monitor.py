import argparse
import psutil
import logging
from datetime import datetime
from pathlib import Path

# Logging sozlamalari
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

    parser.add_argument(
        "--output",
        help="Save monitoring report to a file"
    )

    args = parser.parse_args()

    try:
        metrics = collect_metrics(args.resource)

    except (OSError, psutil.Error) as error:
        logging.exception("Monitoring failed")
        print("ERROR:", error)
        return

    report_lines = []
    report_lines.append("SYSTEM MONITORING REPORT")

    if args.show_time:
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        report_lines.append(f"Time: {current_time}")

    thresholds = {
        "CPU": (70, 90),
        "RAM": (80, 90),
        "DISK": (80, 95)
    }

    for name, value in metrics.items():
        warning, critical = thresholds[name]
        status = get_status(value, warning, critical)

        message = f"{name}: {value:.1f}% [{status}]"
        report_lines.append(message)
        logging.info(message)

    report = "\n".join(report_lines)

    print()
    print(report)

    if args.output:
        try:
            output_path = Path(args.output)
            output_path.write_text(report + "\n", encoding="utf-8")
            print(f"\nReport saved successfully: {output_path}")
            logging.info("Report saved to %s", output_path)

        except OSError as error:
            print("Could not save report:", error)
            logging.exception("Report saving failed")


if __name__ == "__main__":
    main()

import logging
import multiprocessing
import os
import subprocess
import sys
from time import sleep

import requests
from dotenv import load_dotenv

from log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

USER_SERVICE_SCRIPT = "user_service.py"
AUTH_SERVICE_SCRIPT = "auth_service.py"
MESSAGE_SERVICE_SCRIPT = "message_service.py"

load_dotenv()
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8282/")
MESSAGE_SERVICE_URL = os.getenv("MESSAGE_SERVICE_URL", "http://localhost:8383/")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8181/")


def run_service(script_name):
    """Function to run a service as a subprocess."""
    try:
        logger.info(f"Starting service: {script_name}")
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while running {script_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")


def start_services():
    """Function to start the services in separate processes."""
    logger.info("Starting all services...")

    # Create separate processes for each service
    processes = []

    process = multiprocessing.Process(target=check_services, args=())
    process.start()
    processes.append(process)

    services = [USER_SERVICE_SCRIPT, AUTH_SERVICE_SCRIPT, MESSAGE_SERVICE_SCRIPT]
    for service in services:
        process = multiprocessing.Process(target=run_service, args=(service,))
        processes.append(process)
        process.start()

    # Wait for all services to finish (or forever, depending on your use case)
    for process in processes:
        process.join()

    return processes


def stop_services(processes):
    """Function to stop services gracefully."""
    logger.info("Stopping all services...")

    # Iterate over each process and terminate it
    for process in processes:
        if process.is_alive():
            logger.info(f"Terminating {process.name}...")
            process.terminate()  # Send termination signal
            process.join()  # Wait for process to finish

    logger.info("All services stopped.")


def main():
    """Main function to control the service lifecycle."""
    processes = []
    try:
        # Start the services
        processes = start_services()

    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        logger.info("Received keyboard interrupt. Stopping services...")
        stop_services(processes)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        stop_services(processes)


def check_services():
    services = {
        "Auth Service": AUTH_SERVICE_URL,
        "Message Service": MESSAGE_SERVICE_URL,
        "User Service": USER_SERVICE_URL
    }
    while True:
        logger.info("Starting microservices health check...")
        for service_name, url in services.items():
            logger.info(f"Checking {service_name}...")
            response = requests.get(url)
            if response.status_code == 200:
                logger.info(f"Service at {service_name} is UP")
                logger.info(response.json())
            else:
                logger.error(f"Service at {service_name} is DOWN, and status code {response.status_code}")

        logger.info("Waiting for 10 seconds before next check...\n")
        sleep(10)  # Delay before next health check


if __name__ == "__main__":
    main()

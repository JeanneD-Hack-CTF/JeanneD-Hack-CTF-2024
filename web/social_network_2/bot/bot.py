#!/usr/bin/env python3

import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime


HIDDEN_ROUTE = "5F41C84A-6A21-4338-86B2-DD03230F20D6"


def log(message):
    print(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] {message}")


def admin_bot(host, port, headless=False, logout=False, delay=3):
    # Set options
    options = None
    if headless:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    # First, retrieve OTP
    log("Retrieve OTP code")
    driver.get(f"http://{host}:{port}/{HIDDEN_ROUTE}")
    log(driver.current_url)
    otp = driver.find_element(By.TAG_NAME, "body").text

    # Get login page
    log("Try to login as admin")
    driver.get(f"http://{host}:{port}/login")

    # Fill login form
    username, password = "admin", "D392C754-1BA8-4E1D-8A61-5B6F9E2E7368"
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")
    sleep(delay)
    user_input.send_keys(username)
    pass_input.send_keys(password)
    # Click submit button
    submit = driver.find_element(By.ID, "login")
    sleep(delay)
    submit.click()

    # Submit OTP validation
    log("Send OTP validation code")
    sleep(delay)
    log(driver.current_url)
    otp_input = driver.find_element(By.NAME, "otp")
    sleep(delay)
    otp_input.send_keys(otp)
    submit = driver.find_element(By.ID, "send_otp")
    sleep(delay)
    submit.click()

    # Go to administration panel
    log("Go to administration panel to trigger possibles XSS")
    driver.get(f"http://{host}:{port}/admin")
    sleep(delay)

    # Logout
    if logout:
        log("Logout")
        driver.get(f"http://{host}:{port}/logout")
        sleep(delay)

    driver.close()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true", help="Use headless navigation mode")
    parser.add_argument("--logout", action="store_true", help="Logout after trigger the potentials XSS")
    parser.add_argument("--host", type=str, help="IP address or hostname of target application", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, help="Listening port of target application", default=5000)
    parser.add_argument("-d", "--delay", type=int, help="Delay between each bot actions", default=3)
    args = parser.parse_args()
    # Run
    admin_bot(args.host, args.port, headless=args.headless, logout=args.logout, delay=args.delay)

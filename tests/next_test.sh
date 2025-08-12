#!/bin/bash
# Script to be run by "Next test" hotkey (default Mod+Return) configured in Dockerfile.
#
# Sends a SIGUSR1 signal to the pytest process to trigger the next test to run.
# (Applies only when truedriver_PAUSE_AFTER_TEST env variable is set to true)

set -e

pkill -USR1 -f "/app/.venv/bin/python /app/.venv/bin/pytest tests"

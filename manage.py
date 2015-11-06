#!/usr/bin/env python
import os
import subprocess
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lop.settings")

    # This is really annoying. AFL requires this command to get run
    # before it starts
    subprocess.call("echo core > /proc/sys/kernel/core_pattern", shell=True)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

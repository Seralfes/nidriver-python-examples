"""NI System Configuration - Get Elapsed System Time.

This example demonstrates how to get a system's start time since it was last restarted.
"""

import nisyscfg


with nisyscfg.Session(target="localhost") as session:
    system_start_time = session.resource.system_start_time
    current_time = session.resource.current_time

    print("Current Time: ", current_time, "\nSystem Start Time: ", system_start_time)

    elapsed_time = current_time - system_start_time

    hours = elapsed_time.seconds // 3600
    minutes = elapsed_time.seconds % 3600//60
    seconds = elapsed_time.seconds - hours * 3600 - minutes * 60

    print(f"Elapsed Time: {elapsed_time} \nDays: {elapsed_time.days}, Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")

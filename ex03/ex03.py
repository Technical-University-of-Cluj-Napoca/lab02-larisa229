RESET = "\033[0m"
COLORS = {
    "info": "\033[34m",  #blue
    "debug": "\033[90m", #gray
    "warning": "\033[33m", #yellow
    "error": "\033[31m"  #red
}

import os
from datetime import datetime

def smart_log(*args, **kwargs):
    level = kwargs.get("level", "info")
    timestamp = kwargs.get("timestamp", True)
    date = kwargs.get("date", False)
    save_to = kwargs.get("save_to", None)
    colored = kwargs.get("colored", True)

    message = " ".join(str(arg) for arg in args)

    time_str = ""
    if timestamp or date:
        now = datetime.now()
        if date and timestamp:
            time_str = now.strftime("[%Y-%m-%d %H:%M:%S]")
        elif date:
            time_str = now.strftime("[%Y-%m-%d]")
        elif timestamp:
            time_str = now.strftime("[%H:%M:%S]")

    final_message = f"{time_str}{message}"

    if colored and level in COLORS:
        colored_message = f"{COLORS[level]}{final_message}{RESET}"
    else:
        colored_message = final_message

    print(colored_message)

    if save_to:
        os.makedirs(os.path.dirname(save_to), exist_ok=True)
        with open(save_to, "a") as f:
            f.write(final_message + "\n")



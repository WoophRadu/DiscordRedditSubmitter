import logging

def log(msg, level="info"):
    if level == "debug":
        print("[DEBUG] " + msg,flush=True)
        logging.debug(msg)
    elif level == "info":
        print("[INFO] " + msg,flush=True)
        logging.info(msg)
    elif level == "warning":
        print("[WARNING] " + msg,flush=True)
        logging.warning(msg)
    elif level == "error":
        print("[ERROR] " + msg,flush=True)
        logging.error(msg)
    elif level == "critical":
        print("[CRITICAL] " + msg,flush=True)
        logging.critical(msg)

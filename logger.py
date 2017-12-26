import logging
loglevel = 20

def setlevel(level):
    global loglevel
    loglevel = int(level)

def log(msg, level="info"):
    if level == "debug" and loglevel <= 10:
        print("[DEBUG] " + msg,flush=True)
        logging.debug(msg)
    elif level == "info" and loglevel <= 20:
        print("[INFO] " + msg,flush=True)
        logging.info(msg)
    elif level == "warning" and loglevel <= 30:
        print("[WARNING] " + msg,flush=True)
        logging.warning(msg)
    elif level == "error" and loglevel <= 40:
        print("[ERROR] " + msg,flush=True)
        logging.error(msg)
    elif level == "critical" and loglevel <= 50:
        print("[CRITICAL] " + msg,flush=True)
        logging.critical(msg)

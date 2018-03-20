from os import environ

def is_debug_mode_set():
    return environ.get('DEBUG_MODE', False) == '1'

import sys, importlib
if 'firstrun.app' not in sys.modules.keys():
    from firstrun.app import dp
else:
    dp = importlib.reload(sys.modules['firstrun.app']).dp
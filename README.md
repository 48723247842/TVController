# Spotify DBUS Controller Server

## Necessary Config

```
redis-cli -n 1 set "CONFIG.SPOTIFY_DBUS_CONTROLLER_SERVER" "{\"port\": 11101}"
```

## Notes

1. For virtualenv , need `sudo apt-get install python-dbus`
2. also `sudo apt-get install python3-virtualenv`
3. `python3 -m venv --system-site-packages venv`
4. I can't get Docker to Talk to Host dbus socket. Its mounted, but idk
5. So apparently you can use pm2 now to run python apps even inside a virtualenv. wadu
6. `source venv/bin/activate`
7. `pm2 start server.py --name PythonDBUS`
8. `pm2 startup`
9. `pm2 save`
import threading
from time import sleep

import typer

from pyredis.datastore import DataStore
from pyredis.server import Server


REDIS_DEFAULT_PORT = 6379


def check_expiry(datastore):
    while True:
        datastore.remove_expired_keys()
        sleep(0.1)


def main(port=None):
  if port == None:
    port = REDIS_DEFAULT_PORT
  else:
    port = int(port)

  print(f"Starting PyRedis on port: {port}")

  datastore = DataStore()
  expiration_monitor = threading.Thread(target=check_expiry, args=(datastore,))
  expiration_monitor.start()

  server = Server(port, datastore)
  server.run()

if __name__ == "__main__":
  typer.run(main)
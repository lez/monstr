import asyncio
import logging
import sys
from monstr.client.client import Client, ClientPool
import signal
from monstr.encrypt import Keys
from monstr.event.event import Event
from monstr.util import util_funcs

tail = util_funcs.str_tails


async def listen_notes(url):
    run = True

    # so we get a clean exit on ctrl-c
    def sigint_handler(signal, frame):
        nonlocal run
        run = False
    signal.signal(signal.SIGINT, sigint_handler)

    # create the client and start it running
    c = Client(url)
    asyncio.create_task(c.run())
    await c.wait_connect()

    # just use func, you can also use a class that has a do_event
    # with this method sig, e.g. extend monstr.client.EventHandler
    def my_handler(the_client: Client, sub_id: str, evt: Event):
        print(evt.created_at, tail(evt.id), tail(evt.content, 30))

    # start listening for events
    c.subscribe(handlers=my_handler,
                filters={
                   'limit': 100
                })

    while run:
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    url = "ws://localhost:8080"

    asyncio.run(listen_notes(url))
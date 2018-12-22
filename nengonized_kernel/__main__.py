import asyncio
import json
import sys
import websockets

from nengonized_kernel.gql.schema import Context, schema
from nengonized_kernel.model_loader import ExecutionError, ModelLoader


class Handler(object):
    def __init__(self, context):
        self.context = context

    async def __call__(self, ws, path):
        while True:
            query = await ws.recv()
            result = schema.execute(query, context=context)
            await ws.send(json.dumps(result.data))


async def start_server(handler):
    async with websockets.serve(handler, 'localhost', 0) as server:
        for socket in server.sockets:
            sys.stdout.write(repr(socket.getsockname()) + '\n')
        sys.stdout.write('OK\n')
        sys.stdout.flush()
        while True:
            await asyncio.sleep(1)


# FIXME check argument number
with open(sys.argv[1], 'r') as f:
    model = None
    errors = None
    try:
        model = ModelLoader().from_string(f.read())
    except ExecutionError as err:
        errors = [err]
    context = Context(model=model, errors=errors)
    handler = Handler(context)

    asyncio.get_event_loop().run_until_complete(start_server(handler))

import asyncio
import json
import sys
import websockets

from nengonized_kernel.gql.schema import Context, schema
from nengonized_kernel.id_provider import IdProvider
from nengonized_kernel.model_loader import ExecutionError, ModelLoader


class Handler(object):
    def __init__(self, context):
        self.context = context

    async def __call__(self, ws, path):
        while True:
            query_data = json.loads(await ws.recv())
            query = query_data['query']
            variables = query_data.get('variables', None)
            result = schema.execute(
                    query, context=context, variables=variables)
            await ws.send(json.dumps(result.data))


async def start_server(handler):
    async with websockets.serve(handler, 'localhost', 0) as server:
        addresses = [socket.getsockname() for socket in server.sockets]
        json.dump({'graphql': addresses}, sys.stdout)
        sys.stdout.write('\n\n')
        sys.stdout.flush()
        while True:
            await asyncio.sleep(1)
            sys.stdout.flush()
            sys.stderr.flush()


# FIXME check argument number
with open(sys.argv[1], 'r') as f:
    model = None
    id_provider = None
    errors = None
    try:
        model, locals_dict = ModelLoader().from_string(f.read())
        id_provider = IdProvider(model, locals_dict)
    except ExecutionError as err:
        errors = [err]
    context = Context(model=model, errors=errors, id_provider=id_provider)
    handler = Handler(context)

    asyncio.get_event_loop().run_until_complete(start_server(handler))

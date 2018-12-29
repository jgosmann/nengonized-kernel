import asyncio
import json
import os.path
from subprocess import Popen, PIPE
import sys

import pytest
import websockets


VALID_MODEL_FILE = os.path.join(
        os.path.dirname(__file__), 'valid_model_file.py')
INVALID_MODEL_FILE = os.path.join(
        os.path.dirname(__file__), 'invalid_model_file.py')


class Kernel(object):
    def __init__(self, *args):
        self.args = args
        self.proc = None
        self.address = None

    async def __aenter__(self):
        self.proc = await asyncio.create_subprocess_exec(
                sys.executable, '-m', 'nengonized_kernel', *self.args,
                stdout=PIPE, stderr=PIPE)

        asyncio.get_running_loop().create_task(
                self._pipe(self.proc.stderr, sys.stderr, 'stderr'))

        conf = await self._read_json_conf(self.proc.stdout)
        asyncio.get_running_loop().create_task(
                self._pipe(self.proc.stdout, sys.stdout, 'stdout'))

        addr = conf['graphql'][0]
        is_ipv6 = len(addr) > 2
        if is_ipv6:
            self.address = f'ws://[{addr[0]}]:{addr[1]}'
        else:
            self.address = f'ws://{addr[0]}:{addr[1]}'
        return self

    async def _read_json_conf(self, stream):
        lines = []
        while len(lines) == 0 or lines[-1] != b'\n':
            lines.append(await stream.readline())
        return json.loads(b''.join(lines))

    async def _pipe(self, src, dest, name):
        async for line in src:
            dest.write(f'[kernel ({name})] {line.decode()}')

    async def __aexit__(self, exc_type, exc, tb):
        self.proc.terminate()
        try:
            await asyncio.wait_for(self.proc.wait(), timeout=1)
        except asyncio.TimeoutError:
            self.proc.kill()


@pytest.mark.asyncio
async def test_run_kernel_and_query_valid_model():
    async with Kernel(VALID_MODEL_FILE) as kernel:
        async with websockets.connect(kernel.address) as ws:
            await ws.send('{ model { ensembles { label } } }')
            result = await ws.recv()
    assert json.loads(result) == {
            'model': {'ensembles': [{'label': "Ensemble"}]}}


@pytest.mark.asyncio
async def test_run_kernel_and_query_invalid_model():
    async with Kernel(INVALID_MODEL_FILE) as kernel:
        async with websockets.connect(kernel.address) as ws:
            await ws.send('{ errors { message } }')
            result = await ws.recv()
    print(result)
    assert json.loads(result) == {'errors': [{'message': "An error"}]}

import pytest, requests
from ..src.utils import pack

AGENT_PORT = 3210

@pytest.mark.asyncio
async def test_hello_world():
    msg = {
        'type': 'test',
        'content': 'hello world'
    }
    response = requests.post('http://localhost:{}'.format(AGENT_PORT), data = await pack(msg))
    assert response.status_code == 202
    # Should call hello world script

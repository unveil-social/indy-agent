import pytest
from ..src.utils import encode, decode, get_config, pack, unpack

@pytest.mark.asyncio
async def test_encode_decode():
    msg = "Test message"
    assert msg == decode(encode(msg))

@pytest.mark.asyncio
async def test_plain_pack_unpack():
    obj = {"test": "message"}
    packed_message = await pack(obj)
    unpacked_msg = await unpack(packed_message)
    assert unpacked_msg == obj

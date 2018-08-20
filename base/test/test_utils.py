from ..src.utils import pack, unpack
import pytest


@pytest.mark.asyncio
async def test_pack():
    text = 'this is a test message'
    packed_message = await pack(text)
    unpacked_message = await unpack(text)
    assert unpacked_message == text

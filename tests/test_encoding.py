import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from pyredis.protocol import (extract_frame_from_buffer, encode_message)
from pyredis.types import (
    Array,
    BulkString,
    Error,
    Integer,
    SimpleString,
)

def test_encode_simple_string():
    input = SimpleString("Hello")
    assert "+Hello\r\n".encode() == encode_message(input)

from time import sleep, time_ns

import pytest

from pyredis.commands import handle_command
from pyredis.datastore import DataStore
from pyredis.types import Array, BulkString, Error, Integer, SimpleString


@pytest.mark.parametrize(
    "command, expected",
    [
        # Echo Tests
        (
            Array([BulkString(b"ECHO")]),
            Error("ERR wrong number of arguments for 'echo' command"),
        ),
        (Array([BulkString(b"echo"), BulkString(b"Hello")]), BulkString("Hello")),
        (
            Array([BulkString(b"echo"), BulkString(b"Hello"), BulkString("World")]),
            Error("ERR wrong number of arguments for 'echo' command"),
        ),
        # Exists Tests
        (
            Array([BulkString(b"exists")]),
            Error("ERR wrong number of arguments for 'exists' command"),
        ),
        (Array([BulkString(b"exists"), SimpleString(b"invalid key")]), Integer(0)),
        (Array([BulkString(b"exists"), SimpleString(b"key")]), Integer(1)),
        (
            Array(
                [
                    BulkString(b"exists"),
                    SimpleString(b"invalid key"),
                    SimpleString(b"key"),
                ]
            ),
            Integer(1),
        ),
        # Ping Tests
        (Array([BulkString(b"ping")]), SimpleString("PONG")),
        (Array([BulkString(b"ping"), BulkString(b"Hello")]), BulkString("Hello")),
        # Set Tests
        (
            Array([BulkString(b"set")]),
            Error("ERR wrong number of arguments for 'set' command"),
        ),
        (
            Array([BulkString(b"set"), SimpleString(b"key")]),
            Error("ERR wrong number of arguments for 'set' command"),
        ),
        (
            Array([BulkString(b"set"), SimpleString(b"key"), SimpleString(b"value")]),
            SimpleString("OK"),
        ),
        # Set with Expire Errors
        (
            Array([BulkString(b"set"), SimpleString(b"key"), SimpleString(b"value"), SimpleString(b"ex")]),
            Error("ERR syntax error"),
        ),
        (
            Array([BulkString(b"set"), SimpleString(b"key"), SimpleString(b"value"), SimpleString(b"px")]),
            Error("ERR syntax error"),
        ),
        (
            Array([BulkString(b"set"), SimpleString(b"key"), SimpleString(b"value"), SimpleString(b"foo")]),
            Error("ERR syntax error"),
        ),
        # Get Tests
        (
            Array([BulkString(b"get")]),
            Error("ERR wrong number of arguments for 'get' command"),
        ),
        (Array([BulkString(b"get"), SimpleString(b"key")]), BulkString("value")),
        (Array([BulkString(b"get"), SimpleString(b"invalid key")]), BulkString(None)),
        # Unrecognised Command
        (
            Array([BulkString(b"foo")]),
            Error("ERR unknown command 'foo', with args beginning with: "),
        ),
        (
            Array([BulkString(b"foo"), SimpleString(b"key")]),
            Error("ERR unknown command 'foo', with args beginning with: 'key'"),
        ),
        (
            Array([BulkString(b"foo"), SimpleString(b"key bar")]),
            Error("ERR unknown command 'foo', with args beginning with: 'key bar'"),
        ),
        # Del Tests
        (
            Array([BulkString(b"del")]),
            Error("ERR wrong number of arguments for 'del' command"),
        ),
        (Array([BulkString(b"del"), SimpleString(b"del key")]), Integer(1)),
        (Array([BulkString(b"del"), SimpleString(b"invalid key")]), Integer(0)),
        (
            Array(
                [
                    BulkString(b"del"),
                    SimpleString(b"del key2"),
                    SimpleString(b"invalid key"),
                ]
            ),
            Integer(1),
        ),
        # Incr Tests
        (
            Array([BulkString(b"incr")]),
            Error("ERR wrong number of arguments for 'incr' command"),
        ),
        (Array([BulkString(b"incr"), SimpleString(b"key")]), Error("ERR value is not an integer or out of range")),
        # Decr Tests
        (
            Array([BulkString(b"decr")]),
            Error("ERR wrong number of arguments for 'decr' command"),
        ),
        # Lpush Tests
        (
            Array([BulkString(b"lpush")]),
            Error("ERR wrong number of arguments for 'lpush' command"),
        ),
        # Rpush Tests
        (
            Array([BulkString(b"rpush")]),
            Error("ERR wrong number of arguments for 'rpush' command"),
        ),
        # (, ),
    ],
)
def test_handle_command(command, expected):
    datastore = DataStore({"key": "value", "del key": "value", "del key2": "value"})
    result = handle_command(command, datastore)
    assert result == expected


# Incr Tests
def test_handle_incr_command_valid_key():
    datastore = DataStore()
    result = handle_command(Array([BulkString(b"incr"), SimpleString(b"ki")]), datastore)
    assert result == Integer(1)
    result = handle_command(Array([BulkString(b"incr"), SimpleString(b"ki")]), datastore)
    assert result == Integer(2)


# Decr Tests
def test_handle_decr():
    datastore = DataStore()
    result = handle_command(Array([BulkString(b"incr"), SimpleString(b"kd")]), datastore)
    assert result == Integer(1)
    result = handle_command(Array([BulkString(b"incr"), SimpleString(b"kd")]), datastore)
    assert result == Integer(2)
    result = handle_command(Array([BulkString(b"decr"), SimpleString(b"kd")]), datastore)
    assert result == Integer(1)
    result = handle_command(Array([BulkString(b"decr"), SimpleString(b"kd")]), datastore)
    assert result == Integer(0)


def test_handle_decr_invalid_key():
    datastore = DataStore()
    result = handle_command(Array([BulkString(b"decr"), SimpleString(b"kmissing")]), datastore)
    assert result == Error("ERR value is not an integer or out of range")


# Lpush Tests
def test_handle_lpush_lrange():
    datastore = DataStore()
    result = handle_command(Array([BulkString(b"lpush"), SimpleString(b"klp"), SimpleString(b"second")]), datastore)
    assert result == Integer(1)
    result = handle_command(Array([BulkString(b"lpush"), SimpleString(b"klp"), SimpleString(b"first")]), datastore)
    assert result == Integer(2)
    result = handle_command(Array([BulkString(b"lrange"), SimpleString(b"klp"), BulkString(b"0"), BulkString(b"2")]), datastore)
    assert result == Array(data=[BulkString("first"), BulkString("second")])

# Rpush Tests
def test_handle_rpush_lrange():
    datastore = DataStore()
    result = handle_command(Array([BulkString(b"rpush"), SimpleString(b"krp"), SimpleString(b"first")]), datastore)
    assert result == Integer(1)
    result = handle_command(Array([BulkString(b"rpush"), SimpleString(b"krp"), SimpleString(b"second")]), datastore)
    assert result == Integer(2)
    result = handle_command(Array([BulkString(b"lrange"), SimpleString(b"krp"), BulkString(b"0"), BulkString(b"2")]), datastore)
    assert result == Array(data=[BulkString("first"), BulkString("second")])

@pytest.mark.parametrize(
    "command, expected",
    [
        (
            Array([
                BulkString(b"lrange"),
                SimpleString(b"list"),
                BulkString(b"0"),
                BulkString(b"0"),
            ]),
            Array(data=[BulkString("one")])
        ),
        (
            Array([
                BulkString(b"lrange"),
                SimpleString(b"list"),
                BulkString(b"-3"),
                BulkString(b"2"),
            ]),
            Array(data=[BulkString("one"), BulkString("two"), BulkString("three")])
        ),
        (
            Array(
            [
                BulkString(b"lrange"),
                SimpleString(b"list"),
                BulkString(b"-100"),
                BulkString(b"100"),
            ]),
            Array([BulkString("one"), BulkString("two"), BulkString("three")])
        ),
        (
            Array(
            [
                BulkString(b"lrange"),
                SimpleString(b"list"),
                BulkString(b"5"),
                BulkString(b"10"),
            ]),
            Array(data=[])
        )
    ]
)
def test_lrange(command, expected):
    datastore = DataStore()
    result = handle_command(
        Array([BulkString(b"rpush"), SimpleString(b"list"), SimpleString(b"one")]),
        datastore,
    )
    assert result == Integer(1)
    result = handle_command(
        Array([BulkString(b"rpush"), SimpleString(b"list"), SimpleString(b"two")]),
        datastore,
    )
    assert result == Integer(2)
    result = handle_command(
        Array([BulkString(b"rpush"), SimpleString(b"list"), SimpleString(b"three")]),
        datastore,
    )
    assert result == Integer(3)

    result = handle_command(command, datastore)
    assert result == expected




def test_set_with_expiry():
    datastore = DataStore()
    key = 'key'
    value = 'value'
    ex = 1
    px = 100

    base_command = [BulkString(b"set"), SimpleString(b"key"), SimpleString(b"value")]

    # seconds
    command = base_command[:]
    command.extend([BulkString(b"ex"), BulkString(f"{ex}".encode())])
    expected_expiry = time_ns() + (ex * 10**9)
    result = handle_command(command, datastore)
    assert result == SimpleString("OK")
    stored = datastore._data[key]
    assert stored.value == value
    diff = - expected_expiry - stored.expiry
    assert diff < 10000

    # milliseconds
    command = base_command[:]
    command.extend([BulkString(b"px"), BulkString(f"{px}".encode())])
    expected_expiry = time_ns() + (ex * 10**6)
    result = handle_command(command, datastore)
    assert result == SimpleString("OK")
    stored = datastore._data[key]
    assert stored.value == value
    diff = - expected_expiry - stored.expiry
    assert diff < 10000


def test_get_with_expiry():
    datastore = DataStore()
    key = 'key'
    value = 'value'
    px = 100

    command = [
        BulkString(b"set"),
        SimpleString(b"key"),
        SimpleString(b"value"),
        BulkString(b"px"),
        BulkString(f"{px}".encode())
    ]
    result = handle_command(command, datastore)
    assert result == SimpleString("OK")
    sleep((px + 100)/1000)
    command = [BulkString(b"get"), SimpleString(b"key")]
    result = handle_command(command, datastore)
    assert result == BulkString(None)
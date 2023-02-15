"""."""
from unittest import mock


def mocked_requests_get(*args, **_kwargs):  # pylint: disable=W0611, W0613
    """."""

    class MockResponse:
        """."""

        raw = mock.MagicMock()
        text = ""

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """."""
            return self.json_data

    if args[0] == "http://someurl.com/test.json":
        return MockResponse({"key1": []}, 200)

    if args[0] == "http://someurl2.com/test.json":
        return MockResponse(
            {
                "key1": [
                    {
                        "ip": "ip",
                        "port": "port",
                        "protocols": "protocols",
                    }
                ]
            },
            200,
        )

    if args[0] == "wont_work":
        return MockResponse("127.0.0.1", 200)

    if args[0] == "http://bad.status_code.com":
        return MockResponse("127.0.0.1", 500)

    if args[0] == "http://not_proxied.com":
        res = MockResponse("127.0.0.1", 200)
        res.raw._original_response.fp.raw._sock.getpeername.return_value = ["127.0.0.1"]
        return res

    return MockResponse(None, 404)

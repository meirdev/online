import urllib.error
from unittest import mock

import pytest
from pytest_httpserver import HTTPServer

from online import URLS, check_connection, main


def test_check_connection_google(httpserver: HTTPServer):
    httpserver.expect_request("/generate_204").respond_with_data(status=204)

    assert check_connection(URLS[0])


def test_check_connection_apple(httpserver: HTTPServer):
    httpserver.expect_request("/hotspot-detect.html").respond_with_data(
        response_data=b"<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>"
    )

    assert check_connection(URLS[1])


def test_check_connection_microsoft(httpserver: HTTPServer):
    httpserver.expect_request("/connecttest.txt").respond_with_data(
        response_data=b"Microsoft Connect Test"
    )

    assert check_connection(URLS[2])


def test_main_ok():
    with mock.patch("online.check_connection") as mock_check_connection:
        mock_check_connection.return_value = True

        with pytest.raises(SystemExit) as excinfo:
            main()

        assert excinfo.value.code == 0


def test_main_fail():
    with mock.patch("online.check_connection") as mock_check_connection:
        mock_check_connection.return_value = False

        with pytest.raises(SystemExit) as excinfo:
            main()

        assert excinfo.value.code == 1


def test_check_connection_exception():
    with mock.patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("")

        with pytest.raises(SystemExit) as excinfo:
            main()

        assert excinfo.value.code == 1

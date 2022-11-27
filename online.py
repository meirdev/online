import http.client
import sys
import urllib.error
import urllib.request
from typing import Callable, NamedTuple, NoReturn


class Url(NamedTuple):
    name: str
    url: str
    excepted: Callable[[http.client.HTTPResponse], bool]


URLS: list[Url] = [
    Url(
        name="Google",
        url="http://connectivitycheck.gstatic.com/generate_204",
        excepted=lambda response: response.status == 204,
    ),
    Url(
        name="Apple",
        url="https://captive.apple.com/hotspot-detect.html",
        excepted=lambda response: response.read() == b"Success",
    ),
    Url(
        name="Microsoft",
        url="http://www.msftconnecttest.com/connecttest.txt",
        excepted=lambda response: response.read() == b"Microsoft Connect Test",
    ),
]


def check_connection(url: Url) -> bool:
    try:
        with urllib.request.urlopen(url.url) as response:
            return url.excepted(response)
    except urllib.error.URLError:
        return False


def main() -> NoReturn:
    for url in URLS:
        if check_connection(url):
            sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    main()

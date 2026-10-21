"""World audit: does the vault describe reality? Network allowed (localhost here).

    python3 -I world.py [VAULT_DIR]

Starts the toy service from world/server.py as a separate process, makes real
HTTP calls to it, and prints what the doc claims next to what the world
answered. The diff IS the finding.

  ASSERTION  doc said X, world said Y -> RED on mismatch
  SNAPSHOT   volatile value: reported, never fails the build

Exit 0 green, 1 red, 2 could not measure (an auditor that cannot measure must
not print green).
"""
import json
import pathlib
import re
import socket
import subprocess
import sys
import time
import urllib.request
from decimal import Decimal

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def doc(path, pattern):
    m = re.search(pattern, (root / path).read_text())
    if not m:
        print(f"world audit: cannot find the claim in {path} (pattern {pattern!r})")
        sys.exit(2)
    return m.group(1)


claims = {
    "price": doc("state/price.md", r"(\d+\.\d{2}) USD"),
    "requests": doc("state/traffic.md", r"requests today: (\d+)"),
}

with socket.socket() as s:
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]

server = subprocess.Popen(
    [sys.executable, "-I", str(root / "world" / "server.py"), str(port)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
# no proxies: this is a call to localhost, and the proxy must not answer for it
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


calls = 0


def get(path):
    global calls
    calls += 1
    with opener.open(f"http://127.0.0.1:{port}{path}", timeout=2) as r:
        return json.load(r)


try:
    for _ in range(50):
        try:
            get("/price")
            break
        except OSError:
            time.sleep(0.1)
    else:
        print("world audit: the service did not come up, nothing was measured")
        sys.exit(2)

    price = get("/price")["price_usd"]
    requests = get("/requests")["requests_today"]
finally:
    server.terminate()
    server.wait()

reds = 0
print(f"{'kind':<10}{'claim':<10}{'doc says':<14}{'world answered':<16}verdict")
ok = Decimal(claims["price"]) == Decimal(price)
reds += 0 if ok else 1
print(f"{'ASSERTION':<10}{'price':<10}{claims['price']+' USD':<14}{price+' USD':<16}{'ok' if ok else 'RED'}")
print(f"{'SNAPSHOT':<10}{'requests':<10}{claims['requests']:<14}{str(requests):<16}reported, never fails")

print(f"world audit: 1 assertion, 1 snapshot, {calls} HTTP calls")
if reds:
    print(f"world audit: RED, {reds} assertion(s) drifted. The world wins: fix the doc first.")
    sys.exit(1)
print("world audit: green. Green means what the scripts watch is still in place, and nothing more.")

import sys

import afl

from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_rfc6979_signature,
)

afl.start()

try:
    decode_rfc6979_signature(sys.stdin.read())
except ValueError:
    pass

sys.exit(0)

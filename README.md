# Cryptography Coursework

Implementations of SHA-256, HMAC-SHA256 and Base64 written from scratch in Python,
without calling any cryptographic or encoding library. Written for a cryptography
course.

The point of the exercise is to follow the specifications directly: the bit
operations, the padding rules and the constants are all spelled out in the code
rather than delegated to `hashlib` or `base64`.

## Contents

| Folder | Implementation |
| --- | --- |
| `sha256/` | The SHA-256 hash function and HMAC-SHA256 built on top of it |
| `base64/` | Base64 encoder and decoder |

## Requirements

Python 3. No third-party packages. Verified with Python 3.14.

## sha256 — SHA-256 and HMAC

```bash
cd sha256
python sha256_hmac.py
```

### SHA-256

The hash function is implemented end to end:

- The 64 round constants `K`, derived from the cube roots of the first 64 primes
- The 8 initial hash values `H`, derived from the square roots of the first 8 primes
- Message padding: append `0x80`, pad with zero bytes until the length is 56 modulo
  64, then append the original bit length as 8 bytes big-endian
- Processing in 512-bit chunks
- The message schedule, expanding 16 words into 64 using the `s0` and `s1`
  rotations
- The 64-round compression loop with the `maj` and `ch` functions and the `t1` and
  `t2` temporaries
- Accumulation of each chunk's result back into the running hash state

All arithmetic is masked with `0xFFFFFFFF` to emulate 32-bit unsigned overflow,
which Python does not provide natively.

### HMAC-SHA256

HMAC follows the standard construction on top of the hash above:

- Keys longer than the 64-byte block are replaced by their own hash
- Keys shorter than the block are zero-padded to 64 bytes
- The inner pad XORs the key with `0x36`, the outer pad with `0x5C`
- The result is `hash(outer_pad + hash(inner_pad + message))`

The two-pass structure is what makes HMAC resistant to length-extension attacks, so
it cannot be simplified to a single hash of the key concatenated with the message.

## base64 — Encoder and decoder

```bash
cd base64
python base64_codec.py
```

Encoding reads three bytes at a time, joins them into a 24-bit group, and splits
that group into four 6-bit indices into the 64-character alphabet. Decoding reverses
the process, reading four characters into a 24-bit group and emitting up to three
bytes from it.

Padding follows the rule that the number of `=` characters is the complement of the
input length modulo three: a remainder of one requires two `=`, a remainder of two
requires one, and an exact multiple of three requires none. The decoder reads the
padding to know how many of the three output bytes are real.

The file is named `base64_codec.py` rather than `base64.py` on purpose. A module
named `base64.py` in the working directory takes precedence over the standard
library module of the same name, so any `import base64` in that directory would
silently pick up this file instead.

## Verification

Both implementations were checked against the Python standard library, which was
used strictly as an oracle and is not imported by the implementations themselves.

| Implementation | Reference | Cases | Result |
| --- | --- | --- | --- |
| SHA-256 | `hashlib.sha256` | 10 messages, from empty to 1000 bytes, including the padding boundaries at 55, 56, 63, 64, 119 and 120 bytes | all match |
| HMAC-SHA256 | `hmac.new` | 6 keys of length 0, 10, 63, 64, 65 and 200 bytes, covering both the zero-padding and the key-hashing branches | all match |
| Base64 | `base64.b64encode` | 14 inputs covering every length remainder, plus a lossless round-trip check on each | all match |

The lengths were not chosen arbitrarily. A message of 55 bytes still fits in a
single padded block, 56 forces a second one, and 64 is an exact block: these are
where padding implementations usually break. Likewise, a key of exactly 64 bytes
and one of 65 exercise the two different branches of HMAC key normalisation.

## Notes

Two rough edges remain in `sha256_hmac.py`.

The demonstration code sits at module level rather than inside an
`if __name__ == "__main__":` guard, so importing the module runs it and prints. A
guard would make the functions reusable from other code.

The final line prints `Mensagem decodificada:` followed by the original message. The
label is misleading, since SHA-256 is a one-way function and nothing is being
decoded; the script is simply printing the input it started from. `Mensagem original`
would describe it correctly.

Comments and printed output are in Portuguese.

## License

Academic work, shared for reference.

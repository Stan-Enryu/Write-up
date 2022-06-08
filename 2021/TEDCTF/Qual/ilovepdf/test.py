import struct, z3

h = bytes.fromhex('3ed50eac373185348499454857b06fd3') # md5(flag ^ 'h')
x = bytes.fromhex('448582faa78b404a898d0532542d327b') # md5(flag ^ 'x')
p = bytes.fromhex('9973f05fde3fe6320be04a918c5b50ab') # md5(flag ^ 'p')

a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
ah, bh, ch, dh = struct.unpack('IIII', h)
ax, bx, cx, dx = struct.unpack('IIII', x)
ap, bp, cp, dp = struct.unpack('IIII', p)

unknown_words = z3.BitVecs('f0 f1 f2 f3', 32)
remaining_words = struct.unpack('I' * 12, b'\x80' + b'\x00' * 39 + struct.pack('Q', 128))

h_flag = [w ^ 0x68686868 for w in unknown_words] + list(remaining_words)
x_flag = [w ^ 0x78787878 for w in unknown_words] + list(remaining_words)
p_flag = [w ^ 0x70707070 for w in unknown_words] + list(remaining_words)

K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
     0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
     0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be]
S = [7, 12, 17, 22] * 3
def FF(b, c, d):
    return (b & c) | ((~b) & d)
def u32(value):
    return (value + (1 << 32)) % (1 << 32) if isinstance(value, int) else value
def ror(value, shift):
    if isinstance(value, int):
        shift %= 32
        shifted = u32(value) >> shift
        excess = value & ((1 << shift) - 1)
        return shifted | (excess << (32 - shift))
    return z3.RotateRight(value, shift)
def invert_md5(a, b, c, d, values):
    a -= a0
    b -= b0
    c -= c0
    d -= d0
    for r in range(11, -1, -1):
        B, C, D = c, d, a
        a_t1 = u32(ror(b - c, S[r]) - K[r])
        a_t2 = u32(a_t1 - values[r])
        A = u32(a_t2 - FF(B, C, D))
        a, b, c, d = A, B, C, D
    print(a, b, c, d)
    return z3.And(a == a0, b == b0, c == c0, d == d0)

ss = z3.Solver()
print('Adding H flag')
ss.add(invert_md5(ah, bh, ch, dh, h_flag))
print('Adding X flag')
ss.add(invert_md5(ax, bx, cx, dx, x_flag))
print('Adding P flag')
ss.add(invert_md5(ap, bp, cp, dp, p_flag))
print('Solving')
print(ss.check())

m = ss.model()
result = struct.pack('IIII', *[int(str(m.evaluate(w))) for w in unknown_words])
print('hxp{' + result.decode() + '}')
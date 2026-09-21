def sha256(message):
    # Constante com os valores de K usados no algoritmo SHA-256
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

     # Valores iniciais do hash
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    # Pre-processamento da mensagem (inclui o padding e o comprimento da mensagem original)
    original_byte_len = len(message)
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8

    # Padding the message
    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += original_bit_len.to_bytes(8, 'big')

    # Divide a mensagem em chunks de 512 bits (64 bytes) e processa cada chunk
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]

        # Inicializa os valores do hash para este chunk
        a, b, c, d, e, f, g, h = H

        # Calcula o schedule de mensagem (prepara o schedule de mensagem)
        words = [0] * 64
        for j in range(16):
            words[j] = int.from_bytes(chunk[j*4:j*4+4], 'big')
        for j in range(16, 64):
            s0 = (rotate_right(words[j-15], 7) ^ rotate_right(words[j-15], 18) ^ (words[j-15] >> 3))
            s1 = (rotate_right(words[j-2], 17) ^ rotate_right(words[j-2], 19) ^ (words[j-2] >> 10))
            words[j] = (words[j-16] + s0 + words[j-7] + s1) & 0xFFFFFFFF

        # Loop principal da função de compressão
        for j in range(64):
            s0 = (rotate_right(a, 2) ^ rotate_right(a, 13) ^ rotate_right(a, 22))
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = s0 + maj
            s1 = (rotate_right(e, 6) ^ rotate_right(e, 11) ^ rotate_right(e, 25))
            ch = (e & f) ^ ((~e) & g)
            t1 = h + s1 + ch + K[j] + words[j]

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        # Atualiza os valores do hash
        H[0] = (H[0] + a) & 0xFFFFFFFF 
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    # Retorna o hash final (no formato big-endian)
    return b''.join(x.to_bytes(4, 'big') for x in H)

# Função que codifica uma mensagem usando HMAC-SHA256 com uma chave fornecida
def hmac_sha256_encode(key, message):
    # Se a chave tiver mais de 64 bytes, reduz-a ao tamanho necessário calculando seu hash
    if len(key) > 64:
        key = sha256(key)
    if len(key) < 64:
        key += b'\x00' * (64 - len(key))

    # Calcula os pads-chave (key pads) usando as operações XOR com os valores constantes 0x5C e 0x36
    o_key_pad = bytes((x ^ 0x5C) for x in key)
    i_key_pad = bytes((x ^ 0x36) for x in key)

    # Calcula o hash externo usando o pad-chave externo e o hash interno
    inner_hash = sha256(i_key_pad + message)
    outer_hash = sha256(o_key_pad + inner_hash)

    # Retorna o hash externo
    return outer_hash




def rotate_right(n, d):
    return (n >> d) | (n << (32 - d)) & 0xFFFFFFFF



message = b"Aula de criptografia"
key = b"secret_key"

encoded_message = hmac_sha256_encode(key, message)


print("Mensagem codificada:", encoded_message)
print("Mensagem decodificada:", message)
def encodeBase64(input):
    # Tabela Base64
    base64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    # Codificação de caracteres
    encoded_chars = []
    input_length = len(input)

    i = 0
    while i < input_length:
        # Coleta três caracteres para codificação
        octet_a = ord(input[i]) if i < input_length else 0
        octet_b = ord(input[i + 1]) if i + 1 < input_length else 0
        octet_c = ord(input[i + 2]) if i + 2 < input_length else 0

        # Combina os três octetos em um grupo de 24 bits
        triple = (octet_a << 16) + (octet_b << 8) + octet_c

        # Divide o grupo de 24 bits em quatro grupos de 6 bits
        encoded_chars.append(base64_table[(triple >> 18) & 0x3F])
        encoded_chars.append(base64_table[(triple >> 12) & 0x3F])
        encoded_chars.append(base64_table[(triple >> 6) & 0x3F])
        encoded_chars.append(base64_table[triple & 0x3F])

        i += 3

    # Adiciona os caracteres de preenchimento '=' se necessário
    # A quantidade de '=' é o complemento do resto: resto 1 exige dois '=', resto 2 exige um
    padding = (3 - input_length % 3) % 3
    if padding > 0:
        encoded_chars[-padding:] = ['='] * padding

    return ''.join(encoded_chars)

def decodeBase64(input):
    # Tabela Base64
    base64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    # Decodificação de caracteres
    decoded_chars = []
    input_length = len(input)

    i = 0
    while i < input_length:
        # Coleta quatro caracteres para decodificação
        sextet_a = base64_table.index(input[i])
        sextet_b = base64_table.index(input[i + 1])
        sextet_c = base64_table.index(input[i + 2]) if input[i + 2] != '=' else 0
        sextet_d = base64_table.index(input[i + 3]) if input[i + 3] != '=' else 0

        # Combina os quatro sextetos em um grupo de 24 bits
        triple = (sextet_a << 18) + (sextet_b << 12) + (sextet_c << 6) + sextet_d

        # Divide o grupo de 24 bits em três octetos
        decoded_chars.append(chr((triple >> 16) & 0xFF))
        if input[i + 2] != '=':
            decoded_chars.append(chr((triple >> 8) & 0xFF))
        if input[i + 3] != '=':
            decoded_chars.append(chr(triple & 0xFF))

        i += 4

    return ''.join(decoded_chars)

def main():
    original_string = "Hello kaue, vamo que vamo"
    
    # Codificar para Base64
    encoded_string = encodeBase64(original_string)
    print("Encoded:", encoded_string)

    # Decodificar de Base64
    decoded_string = decodeBase64(encoded_string)
    print("Decoded:", decoded_string)

if __name__ == "__main__":
    main()

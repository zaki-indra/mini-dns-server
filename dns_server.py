from socket import *


SERVER_PORT = 9060
IP = "35.226.90.66"
PORT = 54321
BUFFER_SIZE = 2048

ip_map = {
    "lotus.compnet.csui": "152.118.100.1",
    "orchid.compnet.csui": "152.118.100.2"
}

def main():
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(("", SERVER_PORT))
    client_socket = socket(AF_INET, SOCK_DGRAM)

    print("READY")

    while True:
        message, client_address = server_socket.recvfrom(BUFFER_SIZE)

        print(f"Request from {client_address[0]} (ID: {(message[0] << 4) + message[1]})")

        temp = f"{int(message[2]):08b}{int(message[3]):08b}"

        print(f"QR: {int(temp[0], 2)} | OPCODE: {int(temp[1:5], 2)} | AA: {int(temp[5], 2)} | TC: {int(temp[6], 2)} | RD: {int(temp[7], 2)} | RA: {int(temp[8], 2)}")

        print(f"RCODE: {int(temp[-4::], 2)} | QDCOUNT: {(message[4] << 4) + message[5]} | ANCOUNT: {(message[6] << 4) + message[7]} | NSCOUNT: {(message[8] << 4) + message[9]} | ARCOUNT: {(message[10] << 4) + message[11]}")

        i = 12
        website = ""

        while message[i] != 0:
            if message[i] > 60:
                website += chr(message[i])
            else:
                website += "."
            i += 1

        print(f"\nName: {website[1::]}")
        print(f"QTYPE: {(int(message[i+1]) << 4) + int(message[i+2])} | QCLASS: {(int(message[i+3]) << 4) + int(message[i+4])}")
        print("--------------------------------------------------------------")

        try:
            ip_resolve = ip_map[website[1::]]

            reply = message[12:i+1]
            reply += bytes.fromhex("00010001000000000004" + "".join([format(int(x), '02x') for x in ip_resolve.split(".")]))

            resolve_message = message[0:2] + bytes.fromhex("8580") + message[4:6] + bytes.fromhex("0001") + message[8:i+5] + reply

        except KeyError:
            client_socket.sendto(message, (IP, PORT))
            resolve_message, _ = client_socket.recvfrom(BUFFER_SIZE)

        finally:
            print("\n\n")
            server_socket.sendto(resolve_message, client_address)

if __name__ == "__main__":
    main()

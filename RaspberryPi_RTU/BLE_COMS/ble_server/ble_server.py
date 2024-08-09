import bluetooth

uuid_service = "19fa165e-dfe4-44ac-a518-1e71feae6900"

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)


print("Waiting for connection on RFCOMM channel %d with UUID %s" %
      (port, uuid_service))

bluetooth.advertise_service(
    server_sock,
    "Bluetooth Communication Test",
    service_id=uuid_service,
    service_classes=[uuid_service],
    profiles=[bluetooth.SERIAL_PORT_PROFILE]
)

# 클라이언트 연결 수락
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received : ", data.decode('utf-8'))

        client_sock.send("Bluetooth Communication Success")
except Exception as e:
    print(f"Error : {e}")
finally:
    client_sock.close()
    server_sock.close()

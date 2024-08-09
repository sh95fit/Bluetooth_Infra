import bluetooth

# 라즈베리파이 블루투스 주소와 서비스 UUID
server_address = "B8:27:EB:A4:63:87"  # 라즈베리파이 블루투스 MAC 주소로 교체
port = 1
uuid_service = "19fa165e-dfe4-44ac-a518-1e71feae6900"

# 블루투스 클라이언트 소켓 생성
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    # 서비스 검색
    services = bluetooth.find_service(
        uuid=uuid_service, address=server_address)
    if not services:
        print("Service not found")
        exit(1)

    # 첫 번째 서비스를 선택하여 연결
    service = services[0]
    port = service['port']

    client_sock.connect((server_address, port))
    print("Connected to server")

    # 서버로 데이터 송신
    client_sock.send("Hello from client!")

    # 서버로부터 데이터 수신
    data = client_sock.recv(1024)
    print("Received:", data.decode('utf-8'))
finally:
    client_sock.close()

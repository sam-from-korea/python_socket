import socket
import os


def create_request_payload(image_path):
    """이미지 파일을 포함한 멀티파트 요청 데이터 생성"""
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    # 헤더 생성
    headers = [
        f"--{boundary}",
        'Content-Disposition: form-data; name="author"',
        '',
        '1',
        f"--{boundary}",
        'Content-Disposition: form-data; name="title"',
        '',
        'curl 테스트',
        f"--{boundary}",
        f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(image_path)}"',
        'Content-Type: image/jpeg',
        ''
    ]

    # 이미지 파일 읽기
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 바디 생성
    body = b"\r\n".join([h.encode() for h in headers]) + b"\r\n" + image_data + b"\r\n--" + boundary.encode() + b"--\r\n"
    return body, boundary


def run_client(ip, port, image_path):
    """클라이언트 실행하여 서버로 요청 전송"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    # 요청 데이터 생성
    request_payload, boundary = create_request_payload(image_path)
    
    # 요청 헤더 생성
    request_headers = (
        f"POST / HTTP/1.1\r\n"
        f"Host: {ip}:{port}\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        f"Content-Length: {len(request_payload)}\r\n"
        f"\r\n"
    ).encode()

    # 요청 전송
    sock.sendall(request_headers + request_payload)

    # 응답 받기
    response = b""
    while True:
        data = sock.recv(1024)
        if not data:
            break
        response += data
    
    print("Response from server:\n", response.decode())

    # 소켓 닫기
    sock.close()


if __name__ == "__main__":
    IMAGE_PATH = "C:\\Users\\xsamk\\Desktop\\a.jpg"  # 이미지 경로
    run_client("127.0.0.1", 8000, IMAGE_PATH)

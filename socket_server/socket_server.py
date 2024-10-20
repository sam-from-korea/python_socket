import os
import socket
import re
from datetime import datetime


class SocketServer:
    def __init__(self):
        self.bufsize = 1024 # 버퍼 크기 설정
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()  # 응답 파일 읽기
            
        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)
        
    def createDir(self, path):
        """디렉토리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def run(self, ip, port):
        """서버 실행"""
        # 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        self.sock.settimeout(5.0)  # 메인 소켓에도 타임아웃 설정 (5초)
        print("Start the socket server...")
        print("\"Ctrl+C\" for stopping the server!\r\n")
        
        try:
            while True:
                # 클라이언트의 요청 대기
                clnt_sock, req_addr= self.sock.accept()
                clnt_sock.settimeout(5.0)  # 타임아웃 설정(5초)
                print("Request message...\r\n")
                
                # 클라이언트의 요청 데이터 수신
                response = b""
                while True:
                    try:
                        data = clnt_sock.recv(self.bufsize)
                        if not data:
                            break
                        response += data
                    except socket.timeout:
                        break
                
                # 파일 저장 (년-월-일-시-분-초.bin 형식)
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                bin_filename = os.path.join(self.DIR_PATH, f"{timestamp}.bin")
                with open(bin_filename, 'wb') as bin_file:
                    bin_file.write(response)
                    
                # 이미지 파일 추출 및 저장
                image_match = re.search(b'Content-Disposition: form-data; name="image"; filename="(.+?)"\r\nContent-Type: image/.+?\r\n\r\n(.+?)\r\n--', response, re.DOTALL)
                if image_match:
                    image_data = image_match.group(2)
                    image_filename = os.path.join(self.DIR_PATH, f"{timestamp}.jpg")
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(image_data)
                
                # 응답 전송
                clnt_sock.sendall(self.RESPONSE)
                
                # 클라이언트 소켓 닫기
                clnt_sock.close()
        except KeyboardInterrupt:
            print("\r\nStop the server...")
        
        # 서버 소켓 닫기
        self.sock.close()
        
if __name__== "__main__":
    with open('response.bin', 'wb') as f:
        f.write(b'Hello, Client!')

    server = SocketServer()
    server.run("127.0.0.1", 8000)
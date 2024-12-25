import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDesktopWidget

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Control Server")
        self.setGeometry(100, 100, 500, 400)
        
        self.init_ui()
        self.client_socket = None
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.move_to_tv()
        
        # Display for server logs
        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)
        self.layout.addWidget(self.log_display)
        
        # Command input field
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter command")
        self.layout.addWidget(self.command_input)
        
        # Send button
        self.send_button = QPushButton("Send Command", self)
        self.send_button.clicked.connect(self.send_command)
        self.layout.addWidget(self.send_button)
        
        # Main widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def log_message(self, message):
        self.log_display.append(message)
    
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 5555))
        server.listen(5)
        self.log_message("[INFO] Server started on port 5555")
        
        self.client_socket, addr = server.accept()
        self.log_message(f"[INFO] Connected ")
        
        # Start a thread to receive responses from the client
        threading.Thread(target=self.receive_responses).start()
    
    def send_command(self):
        if self.client_socket:
            command = self.command_input.text()
            self.client_socket.send(command.encode())
            self.log_message(f"[SENT] {command}")
            if command.lower() == "exit":
                self.log_message("[INFO] Closing connection...")
                self.client_socket.close()
                self.client_socket = None
        else:
            self.log_message("[ERROR] No client connected.")
    
    def receive_responses(self):
        while self.client_socket:
            try:
                response = self.client_socket.recv(4096).decode()
                self.log_message(f" {response}")
            except Exception as e:
                self.log_message(f"[ERROR] {e}")
                break

    def move_to_tv(self):
       
        desktop = QDesktopWidget()
        screen_count = desktop.screenCount()

        if screen_count > 1:
           
            screen_geometry = desktop.screenGeometry(1)
            
            
            screen_center_x = screen_geometry.left() + (screen_geometry.width() // 2)
            screen_center_y = screen_geometry.top() + (screen_geometry.height() // 2)
            
            
            window_width = self.width()
            window_height = self.height()

           
            window_x = screen_center_x - (window_width // 2)
            window_y = screen_center_y - (window_height // 2)
            
          
            self.move(window_x, window_y)
        else:
            print("TV screen not detected. Defaulting to the primary screen.")

if __name__ == "__main__":
    app = QApplication([])
    window = ServerApp()
    window.show()
    app.exec_()


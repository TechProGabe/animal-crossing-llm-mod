import socket
import sys
import time
from typing import Optional, List, Tuple

class GdbMemoryReader:
    """
    Experimental Memory Reader using Dolphin's GDB Stub over TCP.
    This bypasses OS-level security restrictions (like macOS SIP)
    by talking to the emulator via a local network socket.
    """
    def __init__(self, host='127.0.0.1', port=2345):
        self.host = host
        self.port = port
        self.sock = None
        self.is_connected = False

    def _send_cmd(self, cmd: str) -> Optional[str]:
        if not self.sock:
            return None
        
        # GDB packet format: $command#checksum
        checksum = sum(ord(c) for c in cmd) % 256
        packet = f"${cmd}#{checksum:02x}"
        
        try:
            self.sock.sendall(packet.encode('ascii'))
            
            # Read ACK '+'
            ack = self.sock.recv(1)
            if ack != b'+':
                print(f"❌ GDB Stub: Expected ACK '+', got {ack}")
                return None
                
            # Read response
            response = b""
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b'#' in chunk:
                    break
                    
            if not response:
                return None
                
            # Parse response $data#checksum
            response_str = response.decode('ascii')
            start = response_str.find('$')
            end = response_str.find('#')
            if start != -1 and end != -1:
                return response_str[start+1:end]
            return None
            
        except Exception as e:
            print(f"❌ GDB Stub Error: {e}")
            self.disconnect()
            return None

    def connect_to_process(self) -> bool:
        """Connect to Dolphin's GDB Stub."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2.0)
            self.sock.connect((self.host, self.port))
            self.is_connected = True
            print(f"✅ Successfully connected to Dolphin GDB Stub at {self.host}:{self.port}")
            
            # Disable ack mode to speed things up (optional, but standard for modern GDB)
            # We'll just keep it simple with standard ack mode for compatibility
            return True
        except ConnectionRefusedError:
            print(f"❌ Failed to connect to Dolphin GDB Stub on port {self.port}")
            print("   Please ensure Dolphin is running, a game is loaded, and")
            print("   'Enable GDB Stub' is checked in Configuration -> Advanced.")
            return False
        except Exception as e:
            print(f"❌ GDB connection error: {e}")
            return False

    def get_memory_regions(self) -> List[Tuple[int, int, str]]:
        """
        Return a fake memory region that matches the GameCube memory space.
        This tricks the MemoryIPC class into using GameCube virtual addresses directly.
        """
        return [(0x80000000, 0x1800000, 'rw')]

    def read_memory(self, address: int, size: int) -> Optional[bytes]:
        """Read memory from the GDB stub."""
        if not self.is_connected:
            return None
            
        # GDB read memory command: m<addr>,<length>
        cmd = f"m{address:x},{size:x}"
        hex_data = self._send_cmd(cmd)
        
        if hex_data and not hex_data.startswith('E'): # 'E' signifies error in GDB protocol
            try:
                return bytes.fromhex(hex_data)
            except ValueError:
                return None
        return None

    def write_memory(self, address: int, data: bytes) -> bool:
        """Write memory to the GDB stub."""
        if not self.is_connected:
            return False
            
        # GDB write memory command: M<addr>,<length>:<hex_data>
        hex_data = data.hex()
        cmd = f"M{address:x},{len(data):x}:{hex_data}"
        response = self._send_cmd(cmd)
        
        return response == "OK"

    def disconnect(self):
        """Close the GDB connection."""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.sock = None
        self.is_connected = False

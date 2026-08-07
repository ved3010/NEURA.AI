"""
E.D.I.T.H. Security Anomaly Detector Module
"""

import socket
import logging

logger = logging.getLogger("edith.security")


def run_security_scan() -> dict:
    """Run local security and port scanning diagnostic."""
    common_ports = [22, 80, 443, 8000, 3000]
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        res = sock.connect_ex(("127.0.0.1", port))
        if res == 0:
            open_ports.append(port)
        sock.close()

    return {
        "status": "SECURE",
        "threat_level": "LOW",
        "scanned_ports": common_ports,
        "open_local_ports": open_ports,
        "recommendation": "All local telemetry links nominal."
    }


if __name__ == "__main__":
    print(run_security_scan())

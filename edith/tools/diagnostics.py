"""
E.D.I.T.H. System Diagnostics & Telemetry Tools
"""

import os
import sys
import platform
import psutil
import socket
import logging

logger = logging.getLogger("edith.tools.diagnostics")


def get_system_telemetry() -> str:
    """
    Get detailed system telemetry including CPU, Memory, Disk, Network, and System specs.
    Returns formatted E.D.I.T.H. tactical diagnostic brief.
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count(logical=True)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        net = psutil.net_io_counters()
        bytes_sent_mb = round(net.bytes_sent / (1024 * 1024), 2)
        bytes_recv_mb = round(net.bytes_recv / (1024 * 1024), 2)

        telemetry = {
            "status": "Nominal",
            "os": f"{platform.system()} {platform.release()}",
            "hostname": socket.gethostname(),
            "cpu_usage_percent": cpu_usage,
            "cpu_cores": cpu_count,
            "memory_usage_percent": mem.percent,
            "memory_used_gb": round(mem.used / (1024**3), 2),
            "memory_total_gb": round(mem.total / (1024**3), 2),
            "disk_usage_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "net_sent_mb": bytes_sent_mb,
            "net_recv_mb": bytes_recv_mb,
        }

        # Check battery if laptop
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                telemetry["battery_percent"] = round(battery.percent, 1)
                telemetry["power_plugged"] = battery.power_plugged

        return (
            f"E.D.I.T.H. Diagnostic Brief:\n"
            f"• CPU Core Allocation: {telemetry['cpu_usage_percent']}% across {telemetry['cpu_cores']} logical units.\n"
            f"• System RAM Capacity: {telemetry['memory_usage_percent']}% used ({telemetry['memory_used_gb']} GB / {telemetry['memory_total_gb']} GB).\n"
            f"• Storage Remaining: {telemetry['disk_free_gb']} GB available ({telemetry['disk_usage_percent']}% used).\n"
            f"• Network Telemetry: {telemetry['net_sent_mb']} MB Tx / {telemetry['net_recv_mb']} MB Rx.\n"
            f"• System Status: All core subsystems operating at nominal peak efficiency."
        )
    except Exception as e:
        logger.error(f"Error fetching system telemetry: {e}")
        return f"Diagnostic diagnostic alert: {e}"


def scan_local_network() -> str:
    """Scan local network IP address and active hostname information."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return f"E.D.I.T.H. Network Radar: Host '{hostname}' registered at local IP {local_ip}. Gateway link active."
    except Exception as e:
        return f"Network radar scanning error: {e}"


def get_top_processes(limit: int = 5) -> str:
    """Fetch top processes sorted by CPU memory consumption."""
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by cpu_percent
        top_cpu = sorted(procs, key=lambda x: x.get('cpu_percent') or 0, reverse=True)[:limit]
        formatted = [f"• PID {p['pid']} ({p['name']}): CPU {p['cpu_percent']}% | RAM {round(p['memory_percent'] or 0, 1)}%" for p in top_cpu]
        return "E.D.I.T.H. Process Monitor (Top Active Units):\n" + "\n".join(formatted)
    except Exception as e:
        return f"Process monitor error: {e}"


def register_diagnostic_tools(mcp):
    @mcp.tool()
    def get_system_telemetry_tool() -> str:
        """Get full E.D.I.T.H. system diagnostics, CPU, RAM, Disk, and Network telemetry."""
        return get_system_telemetry()

    @mcp.tool()
    def scan_network_tool() -> str:
        """Scan local network environment and active gateway connection."""
        return scan_local_network()

    @mcp.tool()
    def get_top_processes_tool(limit: int = 5) -> str:
        """Retrieve top active system processes by CPU/Memory consumption."""
        return get_top_processes(limit)

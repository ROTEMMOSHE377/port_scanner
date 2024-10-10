#!/usr/bin/env python3

import socket
import tkinter as tk
from tkinter import messagebox


def scan_ports(target_ip, port_range):
    print(f"Starting scan on {target_ip}")
    open_ports = []

    for port in port_range:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            print(f"Port {port} is open")
            open_ports.append(port)
        sock.close()

    return open_ports


def scan_network(base_ip, start_port, end_port):
    results = []
    for i in range(1, 255):
        target_ip = f"{base_ip}.{i}"
        try:
            print(f"Scanning {target_ip}...")
            open_ports = scan_ports(target_ip, range(start_port, end_port + 1))
            if open_ports:
                results.append(f"Open ports on {target_ip}: {open_ports}")
        except Exception as e:
            print(f"Could not scan {target_ip}: {e}")

    return results


def start_scan():
    base_ip = entry_ip.get()
    port_range_input = entry_ports.get()

    if not base_ip or not port_range_input:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        start_port, end_port = map(int, port_range_input.split('/'))
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port range (e.g., 1/1024).")
        return

    results = scan_network(base_ip, start_port, end_port)

    if results:
        messagebox.showinfo("Scan Results", "\n".join(results))
    else:
        messagebox.showinfo("Scan Results", "No open ports found.")


root = tk.Tk()
root.title("Port Scanner")

tk.Label(root, text="Enter base IP (e.g.,):").pack()
entry_ip = tk.Entry(root)
entry_ip.pack()

tk.Label(root, text="Port Range (e.g., 1/1024):").pack()
entry_ports = tk.Entry(root)
entry_ports.pack()

tk.Button(root, text="Start Scan", command=start_scan).pack()

root.mainloop()

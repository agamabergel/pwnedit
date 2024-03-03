import sys
import re
import os
from ctypes import CDLL, c_ulong, c_long 

PTRACE_ATTACH = 16
PTRACE_DETTACH = 17

c_ptrace = CDLL("libc.so.6").ptrace
c_ptrace.argtypes = (c_ulong, c_ulong, c_ulong, c_ulong)
c_ptrace.restype = c_long


def ptrace(__ptrace_request: int, pid: int) -> bool:
    return c_ptrace(__ptrace_request, c_ulong(pid), c_ulong(0), c_ulong(0))


def _addresses_map(pid: int) -> list[tuple[int, int, str, str]]:
        
    recpie_regex = r"^([a-f0-9]+)\-([a-f0-9]+)\s(...)"
    maps_info = []

    with open(f"/proc/{pid}/maps", 'r') as maps:
        while line := maps.readline():
            if result := re.match(recpie_regex, line):
                start_addr, end_addr, permissions = result.groups()
                maps_info.append((int(start_addr, 16), int(end_addr, 16), permissions))

    return maps_info


def _dump_mem_file(pid: int, _segment: str) -> str:
    
    maps_info = _addresses_map(pid)
    print(maps_info)

    with open(f"dump[{pid}]", 'wb') as dump:
        ptrace(PTRACE_ATTACH, pid)

        with open(f"/proc/{pid}/mem", 'rb') as mem:
            for start_addr, end_addr, permissions in maps_info:
                if 'r' in permissions or 'w' in permissions:
                    mem.seek(start_addr, os.SEEK_SET)
                    print(hex(start_addr))
                    blob = mem.read(end_addr - start_addr)
                    dump.write(blob)

        ptrace(PTRACE_DETTACH, pid)

    return f"./dump[{pid}]"

def main():

    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <pid> <segment>")
        exit(-1)

    pid = int(sys.argv[1])
    #segment = sys.argv[2]
    print(">$ dump file for pid {} in current directory {} ^_^".format(pid, _dump_mem_file(pid, 11)))

if __name__ == "__main__":
    main()

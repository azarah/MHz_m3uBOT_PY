import re

def parse_m3u(content: str):
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
    return lines

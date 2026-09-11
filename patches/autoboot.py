#!/usr/bin/env python3
# 通电自启 (auto-boot): rewrite androidboot.mode=charger -> normal in the kernel
# cmdline before parse_early_param, so userspace init never enters `on charger`
# (LPM) and always boots the full system. No /system or super modification.
# Same length replace ("charger"->"normal "), applied in setup_command_line().
import sys, os

f = sys.argv[1]  # init/main.c
os.chmod(f, 0o644)
s = open(f).read()
if "auto-boot: force normal boot" in s:
    print("[autoboot] already applied")
    sys.exit(0)
anchor = "\tsize_t len, xlen = 0, ilen = 0;\n"
inject = (
    "\tsize_t len, xlen = 0, ilen = 0;\n"
    "\t/* auto-boot: force normal boot, never LPM charger mode */\n"
    "\t{\n"
    "\t\tchar *_abm = strstr(boot_command_line, \"androidboot.mode=charger\");\n"
    "\t\tif (_abm) memcpy(_abm + 17, \"normal \", 7);\n"
    "\t\t_abm = strstr(command_line, \"androidboot.mode=charger\");\n"
    "\t\tif (_abm) memcpy(_abm + 17, \"normal \", 7);\n"
    "\t}\n"
)
if anchor in s:
    s = s.replace(anchor, inject, 1)
    open(f, "w").write(s)
    print("[autoboot] charger->normal injected into setup_command_line")
else:
    print("[autoboot] WARN: setup_command_line anchor not found")
    sys.exit(1)

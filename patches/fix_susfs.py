#!/usr/bin/env python3
# fs/susfs.c uses security_sb_statfs() (declared in linux/security.h) but does
# not include that header -> implicit-declaration. Add the missing include.
import sys, os, re

f = sys.argv[1]  # fs/susfs.c
os.chmod(f, 0o644)
s = open(f).read()
needed = "#include <linux/security.h>\n"
if needed in s:
    print("[fix_susfs] security.h already included")
    sys.exit(0)
m = list(re.finditer(r"^#include .*\n", s, re.M))
if m:
    pos = m[0].end()
    s = s[:pos] + needed + s[pos:]
    open(f, "w").write(s)
    print("[fix_susfs] added linux/security.h include")
else:
    print("[fix_susfs] WARN: no include block found")

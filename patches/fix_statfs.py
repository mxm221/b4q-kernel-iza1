#!/usr/bin/env python3
# Fix susfs statfs.c: the extern decl of susfs_sus_kstat_spoof_vfs_statfs is
# emitted AFTER its use (implicit-declaration error). Hoist the externs to the
# top (after includes), guarded by CONFIG_KSU_SUSFS_SUS_KSTAT. Harmless if the
# patch also declares them later (redundant externs are legal C).
import sys, os, re

f = sys.argv[1]
os.chmod(f, 0o644)
s = open(f).read()
if "susfs_sus_kstat_spoof_vfs_statfs" not in s:
    print("[fix_statfs] nothing to do (no susfs usage)")
    sys.exit(0)
decl = ("\n#ifdef CONFIG_KSU_SUSFS_SUS_KSTAT\n"
        "extern bool susfs_is_inode_sus_kstat(struct inode *inode, bool *out_is_fuse);\n"
        "extern int susfs_sus_kstat_spoof_vfs_statfs(struct inode *inode, struct kstatfs *buf, bool *is_fuse);\n"
        "#endif\n")
if "hoisted susfs kstat externs" in s:
    print("[fix_statfs] already applied")
    sys.exit(0)
inc = list(re.finditer(r"^#include .*\n", s, re.M))
if inc:
    pos = inc[-1].end()
    s = s[:pos] + "/* hoisted susfs kstat externs */" + decl + s[pos:]
    print("[fix_statfs] externs hoisted after includes")
else:
    print("[fix_statfs] WARN: include block not found")
open(f, "w").write(s)

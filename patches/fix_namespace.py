#!/usr/bin/env python3
# Fix susfs' copy_mnt_ns hunk misplacement on Samsung KDP kernels.
# Samsung's copy_mnt_ns() has an extra KDP copy_tree() variant that breaks the
# fuzzy patch context, so `copy_flags |= CL_COPY_MNT_NS;` lands out of scope.
# Remove any misplaced insert and re-insert it right after CL_SHARED_TO_SLAVE.
import sys

f = sys.argv[1]
s = open(f).read()
line = "\tcopy_flags |= CL_COPY_MNT_NS;\n"
s = s.replace(line, "")  # undo misplacement(s)
marker = "\t\tcopy_flags |= CL_SHARED_TO_SLAVE;\n"
if marker in s:
    s = s.replace(marker, marker + line, 1)
    print("[fix_namespace] copy_flags |= CL_COPY_MNT_NS re-inserted in scope")
else:
    print("[fix_namespace] WARN: CL_SHARED_TO_SLAVE marker not found")
open(f, "w").write(s)

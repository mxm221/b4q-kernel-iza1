# b4q-kernel-iza1

Self-build ReSukiSU/SukiSU-Ultra + SUSFS kernel for **Samsung Galaxy Z Flip4 (SM-F721N, b4q, SM8475/waipio)**, matching stock **A16 / One UI 8 build F721NKSS6IZA1** (kernel **5.10.236-android12-9**).

- Source: Samsung Open Source `SM-F721B_16_Opensource` (Kernel.tar.gz, 5.10.236) — uploaded as release asset `src`.
- Toolchain: AOSP **clang-r416183b** (same as stock → `/proc/version` compiler string matches).
- uname target (exact): `5.10.236-android12-9-31998796-abF721NKSS6IZA1 (build-user@build-host) ... clang version 12.0.5 ... #1 SMP PREEMPT Thu Jan  8 08:21:45 UTC 2026`
- Samsung specifics: DEFEX / PROCA / FIVE disabled so root works.

Output: `arch/arm64/boot/Image[.lz4]` → repacked into stock boot.img off-CI, flashed via Odin.

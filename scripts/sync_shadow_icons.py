#!/usr/bin/env python3
"""Re-import original Shadow-rEFInd PNGs at a pinned commit, checking Git blob SHA.
Requires network access. Does not touch Bazzite icon, wallpaper or boot configuration.
"""
import hashlib
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
COMMIT = "fe639d2869f59d291489c0c416c17577bd166046"
ASSETS = {
  "Shadow-rEFInd/os_win.png": ("137f82aae2f4bcd51010f8a8c0b6082b9852aad1", ["icons/os_win.png", "icons/os_win11.png", "icons/os_windows.png"]),
  "Shadow-rEFInd/func_firmware.png": ("d280dc82aa2b3f0a612ef705bbe2302b03416bc1", ["icons/func_firmware.png"]),
  "Shadow-rEFInd/func_reset.png": ("b053033819e48f1e529ecdaf733afd8fe6d454e6", ["icons/func_reset.png"]),
  "Shadow-rEFInd/func_shutdown.png": ("b7d46c05121f45d461c6c7292e1ea0af48a69035", ["icons/func_shutdown.png"]),
  "Shadow-rEFInd/tool_shell.png": ("1ce1d29e3ce2287c665f124224d029d7da03d5cd", ["icons/tool_shell.png"]),
  "Shadow-rEFInd/tool_rescue.png": ("1bdd7c737b83243e1ccfc1ac3a2a39089b07fbf8", ["icons/tool_rescue.png"]),
  "Shadow-rEFInd/selection_big.png": ("04c7871608ae66161ca546f484fea5311a978b21", ["selection_big.png"]),
  "Shadow-rEFInd/selection_small.png": ("d01c92552444220650cf4d03b79c86078fee1b37", ["selection_small.png"]),
}
for source, (expected, destinations) in ASSETS.items():
    url = f"https://raw.githubusercontent.com/chris1111/Shadow-rEFInd/{COMMIT}/{source}"
    with urlopen(url, timeout=30) as reply:
        data = reply.read()
    actual = hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()
    if actual != expected:
        raise RuntimeError(f"Incorrect source blob SHA for {source}: {actual}")
    for name in destinations:
        path = ROOT/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        print(f"Imported {name}")

# rEFInd Bazzite Penguin Swarm

An experimental, 4K Bazzite rEFInd theme inspired by the approved **Penguin Swarm** concept: dozens of penguins under blue-violet neon lighting, a glowing horizon, and four frosted blue glass-card icons. It is an alternate design to [`rEFInd-bazzite-pneaple`](https://github.com/zany130/rEFInd-bazzite-pneaple), not a replacement for rEFInd or its boot configuration.

> **Status: visual installation candidate.** PNG dimensions, paths, and archive integrity are validated; it has **not been boot-tested** on actual firmware. Preview images are illustrations, **not screenshots of rEFInd**.

![Approved concept, illustration only](screenshots/approved-concept.png)

## What is included

- `background.png`: 3840×2160 RGB wallpaper rebuilt **from the approved screenshot**. The unoccluded header, penguins, foreground, and planetary horizon are preserved; only areas blocked by mockup cards and labels are reconstructed. No frozen menu icons are retained.
- `icons/os_bazzite.png`, `os_win.png`, `os_win11.png`, `os_windows.png`: 576×576 RGBA transparent glass-card icons for Bazzite and Windows.
- `icons/os_shell.png` / `os_rescue.png`: optional 576×576 icons. These **do not create a working boot menu entry by themselves**.
- `icons/func_firmware.png`, `func_reset.png`, `func_shutdown.png`: 96×96 utility buttons for built-in rEFInd functions.
- `selection_big.png`: 648×648 transparent blue outline/glow for the selected OS icon.
- `selection_small.png`: 128×128 transparent glow for selected utility buttons.
- `screenshots/`: original approved mockup and an illustrative composite preview.
- `source/`: approved source files and reconstructed lower-res background; not needed on your EFI partition.

## Approved-concept background correction

The original `background.png` was too different from `screenshots/approved-concept.png`: the initial generator rebuilt almost the entire middle and lower scene, introducing an unnatural crowd of small penguins in front of the planet. The revised generator uses the **approved concept as the primary image** and preserves every unobstructed portion of it. Only the four big card/label overlays and the three small tool controls are replaced with blended, source-derived artwork. This is a clean *background*, not a frozen UI screenshot or a pixel-perfect recovery of the obscured areas.

The GitHub Actions workflow on this fix branch regenerates the PNG assets reproducibly from the files already checked in. Inspect `background.png` alongside the approved concept before merging or using this for an installer release. The preview under `screenshots/asset-composition-preview.png` may predate the rebuild; it should not be mistaken for an actual firmware screenshot.

## Installation (existing working rEFInd installation only)

**Do not replace `refind.conf` with an upstream theme config or touch any `.efi` bootloader binaries.**

The install ZIP unpacks to a folder named `rEFInd-bazzite-penguin-swarm`. On the Bazzite machine, first back up your existing config **off the EFI partition**:

```sh
cp /boot/efi/EFI/refind/refind.conf "$HOME/refind.conf.before-penguin-swarm.bak"
```

Then, in the directory containing the extracted theme folder:

```sh
sudo cp -a rEFInd-bazzite-penguin-swarm /boot/efi/EFI/refind/themes/
```

Edit only the last `include themes/.../theme.conf` in `/boot/efi/EFI/refind/refind.conf` to:

```conf
include themes/rEFInd-bazzite-penguin-swarm/theme.conf
```

Keep all your existing menu stanzas, `volume`, loader paths, `scanfor`, and `default_selection` settings unchanged. If your working manual Bazzite entry doesn't already specify a Bazzite icon, add just this line within its existing stanza:

```conf
icon /EFI/refind/themes/rEFInd-bazzite-penguin-swarm/icons/os_bazzite.png
```

In particular, keep your **working Secure Boot chain through `/EFI/fedora/shimx64.efi`**. Never point the Bazzite boot stanza at GRUB directly in this configuration.

### System utility icons

If desired, `showtools firmware,reboot,shutdown` belongs in the *main* `refind.conf` so changing themes never alters which tools are enabled. The EFI Shell normally appears as a **utility** (if enabled); adding an `os_shell.png` does not move it into the OS row. An OS-row Shell icon requires a manually defined entry with a trusted shell EFI loader; `os_rescue.png` similarly needs a real boot target.

### Limitations / what differs from the mockup

- rEFInd shows only the currently selected OS entry's label by default; the mockup shows several simultaneously. The glass-card art, however, is part of each transparent PNG and can be reproduced on real rEFInd menus.
- Boot icon coordinates cannot be arbitrarily fixed to the mockup. Depending on how many entries are discovered, card sizes, menu locations, and tool alignment may differ at runtime.
- Since icons are 576px wide and the selection glow adds 72px, **large numbers of detected boot entries may overflow the row**. Reduce `big_icon_size` to 448 or 384 and test if that happens (images will be scaled automatically).
- The wallpaper is a recolored and recomposed derivative of the penguin illustration attributed to Universal Blue's **100K Penguins!** announcement, plus the user's approved AI concept screenshot; it is not an unmodified official image. Background is resampled from 1672×941 to 4K, not natively 4K-rendered.

## Revert

Restore the previous include line (and previous Bazzite manual icon path if changed) or restore the saved config backup. Leave the previous theme installed until you verify this one boots and looks correct. No EFI binaries or NVRAM entries are changed by this theme package.

## Building from source

Requires Python 3, Pillow and NumPy. Run `python3 scripts/build_assets.py` from anywhere. It uses `scripts/rebuild_approved_background.py` to restore the approved composition rather than the earlier regenerated all-over penguin collage. To rebuild *only* the wallpaper, run `python3 scripts/rebuild_approved_background.py`. The image regions hidden by icons in the concept cannot be recovered exactly; those regions are reconstructed from the original supplied penguin source and unobstructed dark planetary surface. `source/` is intentionally omitted from the compact install ZIP.

## Source artwork: "100K Penguins!"

The original penguin-swarm image supplied for this theme is attributed to the **[100K Penguins! announcement](https://universal-blue.discourse.group/t/100k-penguins/12577)** on the official Universal Blue community forum. The announcement was posted by **kylegospo on October 13, 2026**, celebrating 100,000 weekly active users of Universal Blue. That identifies the *publisher and occasion*, **not necessarily the original illustrator or full copyright owner**.

This theme's `source/user-supplied-penguin-swarm.png` is the original image supplied for our redesign. The published `background.png` is a **modified, tinted, resampled and re-composited derivative** featuring the user's approved glowing planetary horizon. The accompanying concept screenshots are illustrations rather than photographs or real firmware captures.

**Permission status:** The announcement identifies a credible official source, but does **not explicitly specify a reuse/derivative license** for the penguin illustration. Even though the image appeared in an official project announcement, that alone does not establish permission to redistribute edited copies under the theme's MIT license. Confirm copyright ownership and derivative/redistribution permission with the Bazzite/Universal Blue team or image rights holder before treating the wallpaper as freely reusable. A source credit is useful but is **not a substitute for a license or permission**.

This is an **unofficial fan/community rEFInd theme**; it is not affiliated with, sponsored by, or endorsed by Bazzite or Universal Blue. Logos and other trademarks remain the property of their respective owners.

## Authorship, sources, and licensing

Inspired by Lumen's glass-card aesthetic ([Shoxjaxon Atabayev](https://github.com/shoxjaxon-atabayev/rEFInd-lumen), MIT); the layout and assets here are separately composed. Icon shadows take inspiration from BsxM1 by AlexFullmoon. The source penguin image was supplied by the user and traced to the official **100K Penguins!** forum announcement. **The announcement does not state a clear redistribution/derivatives license; obtain permission or confirm the rights before redistributing the modified wallpaper.** The README and Python build script are MIT-licensed; that license does not automatically apply to third-party imagery or OS trademarks. See `ATTRIBUTION.md` and `LICENSE`.

This theme is not affiliated with or endorsed by Bazzite, Universal Blue, Microsoft, or the creators of other rEFInd themes.

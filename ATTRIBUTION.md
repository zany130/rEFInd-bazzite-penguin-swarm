# Credits, asset provenance and license scope

This repository is an **unofficial rEFInd theme**, not an official or endorsed release of Bazzite, Universal Blue, Microsoft, rEFInd, or the other projects cited below. Names, artwork and trademarks belong to their respective rights holders.

## Shadow-rEFInd graphics (GNU AGPL-3.0)

The rEFInd icon collection is sourced from [chris1111/Shadow-rEFInd](https://github.com/chris1111/Shadow-rEFInd) at pinned Git revision `fe639d2869f59d291489c0c416c17577bd166046`.

- Imported original PNGs in `icons/` cover the upstream OS icon family (`os_*`), functional icons (`func_*`), utility icons (`tool_*`), volume badges (`vol_*`), boot labels (`boot_*`), and navigation/decorative icons. The two selection images are shipped as `selection_big.png` and `selection_small.png`; equivalent copies also appear under `icons/`.
- **Upstream asset bytes are unmodified** for their corresponding filenames. Extra aliases such as `icons/os_win11.png` (and `os_win10.png` where present) reuse the corresponding Shadow Windows icon image to support common rEFInd icon names. The custom `icons/os_bazzite.png` was made for this theme collection and is **not** a Shadow-rEFInd original.
- Imported assets remain under Shadow-rEFInd's **GNU AGPL-3.0** license. Preserve the source attribution and the complete license notice in [third_party/Shadow-rEFInd-AGPL-3.0.txt](third_party/Shadow-rEFInd-AGPL-3.0.txt) when redistributing.
- The repository's root `LICENSE` applies **MIT only to independently originated project material**, not to imported AGPL-3.0 graphics; the MIT license does not supersede AGPL-3.0 terms.

## Penguin Swarm illustration and wallpaper

- **Original illustration:** `source/user-supplied-penguin-swarm.png`, supplied by the theme creator; the image was traced to Universal Blue's [“100K Penguins!” announcement](https://universal-blue.discourse.group/t/100k-penguins/12577) published by `kylegospo` on **October 13, 2026**.
- **What that citation establishes:** the original image appeared in an official Bazzite/Universal Blue forum announcement. It **does not** establish that the post author illustrated it, owns all rights, or has granted reuse permission.
- **Modification:** `background.png` is an edited, tinted, resampled and recomposited Penguin Swarm wallpaper with the user-approved planetary horizon and final “Penguin Swarm” heading. `source/clean-background-1672x941.png` and other `source/` PNGs document earlier compositing inputs and artwork.
- **Screenshots:** `screenshots/approved-concept.png` is a historical AI-assisted concept. `screenshots/asset-composition-preview.png` shows earlier artwork layout. `screenshots/preview.png` captures actual rEFInd running in **QEMU/OVMF**, not physical firmware.
- **Rights status:** neither the original illustrator/rights holder nor a license expressly allowing redistribution or adaptation has been verified. **Source credit is not permission.** Contact the copyright holder or Universal Blue/Bazzite project before asserting commercial use, redistribution or the derivative's open-source license status.

## Inspiration

- [rEFInd Lumen](https://github.com/shoxjaxon-atabayev/rEFInd-lumen), Shoxjaxon Atabayev (MIT): visual inspiration for glossy/menu-card treatment. No upstream Lumen images or code are claimed to have been copied.
- [BsxM1](https://github.com/AlexFullmoon/refind-bsxm1-theme), AlexFullmoon: inspiration for icon-shadow treatment, not a copied asset source.

## Logo and permission caveats

Bazzite, Universal Blue, Microsoft, Windows, and other third-party identifiers are the property of their respective owners. The custom Bazzite icon is not an official branding-license grant. This documentation records known sources and license terms; it does not imply consent from rightsholders or resolve any specifically unverified wallpaper permissions.

See the project [README](README.md) for safe installation and QEMU-versus-hardware testing distinctions.

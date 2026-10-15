#!/usr/bin/env python3
"""UI-free Penguin Swarm wallpaper faithful to the approved concept.

Preserves the original screenshot everywhere except where the mockup
obscures underlying artwork. Only those masked regions are reconstructed
using the original user-supplied penguin source and unobscured ocean pixels.
Requires Pillow and NumPy.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def rectangle_mask(size, rect, blur):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rectangle(rect, fill=255)
    return np.asarray(mask.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255.0


def render_background(root: Path) -> Image.Image:
    src = root / "source"
    approved = Image.open(root / "screenshots" / "approved-concept.png").convert("RGB")
    penguins = Image.open(src / "user-supplied-penguin-swarm.png").convert("RGB")
    W, H = approved.size
    if (W, H) != (1672, 941):
        raise ValueError(f"Unexpected concept dimensions: {(W, H)}")

    original = np.asarray(approved, dtype=np.float32)
    swarm = np.asarray(penguins.resize((W, H), Image.Resampling.BICUBIC),
                       dtype=np.float32)
    y, x = np.mgrid[0:H, 0:W]
    xn, yn = x / W, y / H
    blue = np.exp(-(((xn - .3) / .9) ** 2 + ((yn - .3) / .7) ** 2) * 1.8)
    magenta = np.exp(-(((xn - 1.05) / .55) ** 2 + ((yn - .28) / .56) ** 2) * 1.6)

    fill = np.empty_like(swarm)
    fill[:, :, 0] = swarm[:, :, 0] * (.27 + .12 * magenta) + 2 + 12 * magenta + 2 * blue
    fill[:, :, 1] = swarm[:, :, 1] * (.35 + .08 * blue) + 3 + 9 * blue
    fill[:, :, 2] = swarm[:, :, 2] * (.52 + .13 * blue) + 12 + 21 * blue + 15 * magenta
    fill = np.asarray(Image.fromarray(np.uint8(np.clip(fill, 0, 255)), "RGB")
                      .filter(ImageFilter.GaussianBlur(3)), dtype=np.float32)

    # Cover the four OS cards, cyan glow, permanent labels and caption.
    # Exact visible pixels outside the original overlay are retained.
    mid = rectangle_mask((W, H), (190, 222, 1480, 630), 13)
    clean = original * (1 - mid[:, :, None]) + fill * mid[:, :, None]

    # The tools lie on a dark planet reflection. Extend its unobscured
    # neighboring pixels, blending left/right for smooth visual continuity.
    seafill = original.copy()
    for row in range(700, 894):
        left, right = original[row, 510], original[row, 1180]
        weights = np.linspace(0, 1, 671, dtype=np.float32)[:, None]
        gradient = left * (1 - weights) + right * weights
        texture = original[row, 0:671] * .45 + original[row, 1001:1672] * .55
        seafill[row, 510:1181] = .45 * gradient + .55 * texture
    seafill = np.asarray(Image.fromarray(np.uint8(np.clip(seafill, 0, 255)), "RGB")
                         .filter(ImageFilter.GaussianBlur(6)), dtype=np.float32)
    tools = rectangle_mask((W, H), (565, 715, 1108, 875), 13)
    clean = clean * (1 - tools[:, :, None]) + seafill * tools[:, :, None]

    result = Image.fromarray(np.uint8(np.clip(clean, 0, 255)), "RGB")
    result.save(src / "clean-background-1672x941.png", optimize=True)
    result.resize((3840, 2160), Image.Resampling.LANCZOS).save(
        root / "background.png", compress_level=8)
    return result


if __name__ == "__main__":
    render_background(Path(__file__).resolve().parents[1])
    print("Rebuilt the approved Penguin Swarm illustration as a clean 4K background")

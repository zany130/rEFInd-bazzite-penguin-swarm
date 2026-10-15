#!/usr/bin/env python3
"""Build a rEFInd Penguin Swarm theme from the conversation's approved mockup.

The background is reconstituted from a user-provided penguin swarm image and
unobstructed parts of the approved mockup; no UI tiles are baked into it.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import zipfile, shutil, textwrap

BASE = Path(__file__).resolve().parent.parent
OUTER = BASE.parent
ROOT = BASE
ICONS = ROOT / 'icons'
SOURCES = ROOT / 'source'
PREVIEWS = ROOT / 'screenshots'
for p in (ROOT, ICONS, SOURCES, PREVIEWS): p.mkdir(parents=True,exist_ok=True)

# Faithful wallpaper repair: keep the approved art wherever the mockup was
# not obscured by UI. Reconstruct ONLY the card and tool overlay regions.
from rebuild_approved_background import render_background
bg=render_background(ROOT)

# 4K icon size; card art embedded in each icon to reproduce glass theme in stock rEFInd.
CARD=576
HIGHLIGHT=648
SMALL=96

def glass_card(size=576):
    im=Image.new('RGBA',(size,size),(0,0,0,0))
    c=size/576
    # Shadow (farther away first)
    shadow=Image.new('RGBA',im.size)
    ds=ImageDraw.Draw(shadow)
    ds.rounded_rectangle((int(31*c),int(24*c),int(545*c),int(548*c)),radius=int(52*c),fill=(0,4,25,170))
    shadow=shadow.filter(ImageFilter.GaussianBlur(int(22*c)))
    im.alpha_composite(shadow)
    d=ImageDraw.Draw(im,'RGBA')
    box=(int(16*c),int(16*c),int(560*c),int(560*c))
    d.rounded_rectangle(box,radius=int(55*c),fill=(6,18,45,218),outline=(92,142,223,170),width=max(1,int(3*c)))
    # Blue tinted lower glass wave, clipping with rounded mask.
    wave=Image.new('RGBA',(size,size),(0,0,0,0));wd=ImageDraw.Draw(wave,'RGBA')
    pts=[(int(16*c),int(397*c)),(int(80*c),int(420*c)),(int(180*c),int(450*c)),(int(290*c),int(482*c)),(int(390*c),int(450*c)),(int(492*c),int(410*c)),(int(560*c),int(385*c)),(int(560*c),int(560*c)),(int(16*c),int(560*c))]
    wd.polygon(pts,fill=(19,88,187,86))
    wd.polygon([(int(16*c),int(490*c)),(int(164*c),int(440*c)),(int(310*c),int(506*c)),(int(460*c),int(440*c)),(int(560*c),int(456*c)),(int(560*c),int(560*c)),(int(16*c),int(560*c))],fill=(14,55,162,65))
    mask=Image.new('L',(size,size),0);ImageDraw.Draw(mask).rounded_rectangle(box,radius=int(55*c),fill=255)
    wave.putalpha(Image.fromarray(np.uint8(np.array(wave.getchannel('A'))*np.array(mask)/255)))
    im.alpha_composite(wave)
    d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle(box,radius=int(55*c),outline=(130,174,248,150),width=max(1,int(3*c)))
    # Top and left highlights, subdued enough for white glyphs.
    d.arc((int(23*c),int(23*c),int(551*c),int(551*c)),180,290,fill=(194,228,255,130),width=max(1,int(2*c)))
    return im

mapping={
 'os_bazzite.png':'glowing_cyan_to_magenta_monogram_icon.png',
 'os_win.png':'neon_glass_windows_logo.png',
 'os_shell.png':'glossy_neon_terminal_icon.png',
 'os_rescue.png':'neon_frosted_six_tooth_gear.png',
}
for name,source_name in mapping.items():
    img=glass_card(CARD)
    symbol=Image.open(SOURCES/source_name).convert('RGBA')
    aa=symbol.getchannel('A').point(lambda v:0 if v<=3 else v)
    symbol.putalpha(aa)
    symbol=symbol.resize((350,350),Image.Resampling.LANCZOS)
    img.alpha_composite(symbol,(113,99))
    img.save(ICONS/name,format='PNG',optimize=True)
# Aliases cover rEFInd Windows icon autodetection possibilities
for alt in ['os_windows.png','os_win11.png']:
    shutil.copyfile(ICONS/'os_win.png',ICONS/alt)
# Use built-in tool convention for automatic replacement with circular button look.
for name,sr in {
 'func_firmware.png':'neon_frosted_six_tooth_gear.png',
 'func_reset.png':'glowing_glass_reboot_icon.png',
 'func_shutdown.png':'glowing_cyan_purple_power_icon.png',
}.items():
    icon=Image.open(SOURCES/sr).convert('RGBA')
    icon=icon.resize((68,68),Image.Resampling.LANCZOS)
    tile=Image.new('RGBA',(96,96),(0,0,0,0))
    d=ImageDraw.Draw(tile,'RGBA')
    d.ellipse((4,4,92,92),fill=(5,13,43,175),outline=(94,148,242,160),width=2)
    tile.alpha_composite(icon,(14,14))
    tile.save(ICONS/name,format='PNG',optimize=True)
# Alternate legacy names are not essential but common aliases.
shutil.copyfile(ICONS/'func_firmware.png',ICONS/'func_csr_rotate.png') if False else None

# Selection background must be visible outside the glass tile, never obscure the logo.
sel=Image.new('RGBA',(HIGHLIGHT,HIGHLIGHT),(0,0,0,0))
ox=(HIGHLIGHT-CARD)//2
# Bright outer glow with transparent center.
glow=Image.new('RGBA',sel.size)
dg=ImageDraw.Draw(glow)
dg.rounded_rectangle((ox+4,ox+4,HIGHLIGHT-ox-4,HIGHLIGHT-ox-4),radius=72,outline=(31,158,255,240),width=12)
glow=glow.filter(ImageFilter.GaussianBlur(26))
sel.alpha_composite(glow)
glow2=Image.new('RGBA',sel.size)
dg=ImageDraw.Draw(glow2)
dg.rounded_rectangle((ox+8,ox+8,HIGHLIGHT-ox-8,HIGHLIGHT-ox-8),radius=70,outline=(47,205,255,190),width=12)
glow2=glow2.filter(ImageFilter.GaussianBlur(10))
sel.alpha_composite(glow2)
d=ImageDraw.Draw(sel)
d.rounded_rectangle((ox+8,ox+8,HIGHLIGHT-ox-8,HIGHLIGHT-ox-8),radius=70,outline=(100,230,255,200),width=6)
sel.save(ROOT/'selection_big.png',format='PNG',optimize=True)
small_sel=Image.new('RGBA',(128,128),(0,0,0,0))
sglow=Image.new('RGBA',(128,128),(0,0,0,0))
dg=ImageDraw.Draw(sglow);dg.ellipse((10,10,118,118),outline=(65,170,255,220),width=8)
sglow=sglow.filter(ImageFilter.GaussianBlur(10));small_sel.alpha_composite(sglow)
ImageDraw.Draw(small_sel).ellipse((16,16,112,112),outline=(110,205,255,190),width=4)
small_sel.save(ROOT/'selection_small.png',format='PNG',optimize=True)

# Very conservative visual-only theme config.
(ROOT/'theme.conf').write_text('''# rEFInd Bazzite Penguin Swarm — artwork-only theme.
# Do not change the working menu entries, Shim/Secure Boot chain, or scan rules.
icons_dir themes/rEFInd-bazzite-penguin-swarm/icons
banner themes/rEFInd-bazzite-penguin-swarm/background.png
banner_scale fillscreen
big_icon_size 576
small_icon_size 96
selection_big themes/rEFInd-bazzite-penguin-swarm/selection_big.png
selection_small themes/rEFInd-bazzite-penguin-swarm/selection_small.png
''', encoding='utf8')

# Reproducible compositing preview, not claimed to be a rEFInd screenshot.
mock=bg.copy().convert('RGBA')
# At 1672 rendering, big icon 576/2.296 -> 251 pixels each.
for i,name in enumerate(['os_bazzite.png','os_win.png','os_shell.png','os_rescue.png']):
    xx=[235,540,844,1149][i]; yy=267
    size=270
    if i==0:
        hs=Image.open(ROOT/'selection_big.png').resize((305,305),Image.Resampling.LANCZOS)
        mock.alpha_composite(hs,(xx-17,yy-17))
    icon=Image.open(ICONS/name).resize((size,size),Image.Resampling.LANCZOS)
    mock.alpha_composite(icon,(xx,yy))
for i,name in enumerate(['func_firmware.png','func_reset.png','func_shutdown.png']):
    xx=[644,790,936][i];yy=746
    symbol=Image.open(ICONS/name).resize((64,64),Image.Resampling.LANCZOS)
    mock.alpha_composite(symbol,(xx,yy))
# Actual rEFInd positions and labels vary; keep preview without simulated permanent labels.
mock.convert('RGB').save(PREVIEWS/'asset-composition-preview.png',format='PNG',optimize=True)


print('Assets successfully rebuilt in', ROOT)

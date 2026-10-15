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

# Reconstitute background using *real* swarming penguins rather than baked-in UI.
SWARM = SOURCES / 'user-supplied-penguin-swarm.png'
MOCKUP = PREVIEWS / 'approved-concept.png'
assert SWARM.exists() and MOCKUP.exists()
W,H=1672,941
src=Image.open(SWARM).convert('RGB')
orig=Image.open(MOCKUP).convert('RGB')
# Fit center-crop original grayscale penguin artwork to widescreen.
w,h=src.size
crop_h=int(w*H/W)
src=src.crop((0,max(0,(h-crop_h)//2),w,min(h,(h+crop_h)//2)))
src=src.resize((W,H),Image.Resampling.LANCZOS)
a=np.array(src).astype(np.float32)
y,x=np.mgrid[0:H,0:W]
xn=x/W;yn=y/H
# Add cool-blue rim lighting and magenta on right, retaining penguin detail.
blue=np.exp(-(((xn-.76)/.57)**2+((yn-.16)/.72)**2)*1.7)
magenta=np.exp(-(((xn-.98)/.36)**2+((yn-.30)/.55)**2)*1.8)
# Dark navy background with gently lit low-key penguin shapes.
base=np.zeros_like(a)
base[:,:,0]=a[:,:,0]*(.37+.12*magenta)+5+15*magenta+3*blue
base[:,:,1]=a[:,:,1]*(.48+.12*blue)+6+12*blue
base[:,:,2]=a[:,:,2]*(.91+.15*blue)+15+37*blue+25*magenta
# Broad cyan left/blue overhead pools provide atmosphere.
spot=np.exp(-(((xn-.12)/.5)**2+((yn-.04)/.31)**2)*1.6)
base[:,:,1]+=spot*6;base[:,:,2]+=spot*20
base=np.uint8(np.clip(base,0,255))
orig_arr=np.array(orig).astype(np.float32)
bg=base.astype(np.float32)
# Original screenshot's unobstructed header/upper penguins with static branding.
head=np.clip((280-y)/95,0,1)[:,:,None]
bg=bg*(1-head)+orig_arr*head
# Planet/horizon is untouched in the approved screenshot between y=625-710.
# Blend away from this stripe to reconstruct the area behind its UI.
hmask=np.minimum(np.clip((y-615)/25,0,1),np.clip((765-y)/75,0,1))[:,:,None]
bg=bg*(1-hmask)+orig_arr*hmask
# Retain the unobstructed foreground penguins at the very bottom edge.
bot=np.clip((y-875)/45,0,1)[:,:,None]
bg=bg*(1-bot)+orig_arr*bot
# Low-contrast vignette conceals transitions and preserves icon legibility.
vig=np.clip(1-.13*np.maximum(np.abs(xn-.5)*1.1,np.abs(yn-.5)*.8),.75,1)
bg=Image.fromarray(np.uint8(np.clip(bg*vig[:,:,None],0,255)),'RGB')
# Store original 1672px clean composite for reproducibility.
bg.save(SOURCES/'clean-background-1672x941.png',format='PNG',optimize=True)
bg_4k=bg.resize((3840,2160),Image.Resampling.LANCZOS)
bg_4k.save(ROOT/'background.png',format='PNG',compress_level=8)
if SWARM.resolve() != (SOURCES/'user-supplied-penguin-swarm.png').resolve():
    shutil.copy2(SWARM, SOURCES/'user-supplied-penguin-swarm.png')
if MOCKUP.resolve() != (PREVIEWS/'approved-concept.png').resolve():
    shutil.copy2(MOCKUP, PREVIEWS/'approved-concept.png')

# This builder intentionally regenerates only original background assets.
# Shadow-rEFInd PNGs and the visual-only theme.conf are deliberately kept intact.
# For upstream icon import with verified Git SHA hashes, use sync_shadow_icons.py.
print("Rebuilt penguin-swarm background; Shadow-rEFInd icons and config preserved")

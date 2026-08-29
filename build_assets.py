#!/usr/bin/env python3
"""
build_assets.py - Script de otimizacao de assets para o site 7x Patrimonial

Uso:
    python build_assets.py            # comprime imagens + minifica CSS/JS
    python build_assets.py --images   # so imagens
    python build_assets.py --css      # so CSS
    python build_assets.py --js       # so JS
"""

import os
import sys
import glob
import time
import io

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")
IMG_DIR    = os.path.join(STATIC_DIR, "img")
CSS_DIR    = os.path.join(STATIC_DIR, "css")
JS_DIR     = os.path.join(STATIC_DIR, "js")

JPEG_QUALITY = 82
WEBP_QUALITY = 82

def human_size(n):
    for u in ["B","KB","MB"]:
        if abs(n) < 1024.0:
            return f"{n:.1f} {u}"
        n /= 1024.0
    return f"{n:.1f} GB"

def savings(before, after):
    if before == 0: return "0%"
    return f"-{(1 - after/before)*100:.0f}%"

def compress_images():
    try:
        from PIL import Image
    except ImportError:
        print("  [!] Pillow nao encontrado.")
        return
    print("\n  Comprimindo imagens...")
    for ext in ("jpg","jpeg","png"):
        for path in glob.glob(os.path.join(IMG_DIR,"**",f"*.{ext}"), recursive=True):
            if path.endswith(".min.jpg"): continue
            before = os.path.getsize(path)
            try:
                img = Image.open(path)
                fmt = "JPEG" if ext in ("jpg","jpeg") else "PNG"
                if fmt == "JPEG":
                    if img.mode not in ("RGB","L"):
                        img = img.convert("RGB")
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
                else:
                    buf = io.BytesIO()
                    img.save(buf, format="PNG", optimize=True)
                buf.seek(0)
                data = buf.getvalue()
                if len(data) < before:
                    with open(path,"wb") as f: f.write(data)
                    after = len(data)
                else:
                    after = before
                print(f"    {os.path.basename(path):<35} {human_size(before):>8} -> {human_size(after):>8}  {savings(before,after)}")
                # WebP
                webp_path = os.path.splitext(path)[0] + ".webp"
                if not os.path.exists(webp_path):
                    img2 = Image.open(path).convert("RGB")
                    img2.save(webp_path, format="WebP", quality=WEBP_QUALITY)
                    print(f"    {os.path.basename(webp_path):<35} [WebP gerado]")
            except Exception as e:
                print(f"    [!] Erro em {os.path.basename(path)}: {e}")

def minify_css():
    try:
        import rcssmin
    except ImportError:
        print("  [!] rcssmin nao encontrado.")
        return
    print("\n  Minificando CSS...")
    tot_b = tot_a = 0
    for path in glob.glob(os.path.join(CSS_DIR,"**","*.css"), recursive=True):
        if path.endswith(".min.css"): continue
        before = os.path.getsize(path)
        tot_b += before
        try:
            with open(path,"r",encoding="utf-8") as f: c = f.read()
            minified = rcssmin.cssmin(c)
            min_path = path[:-4] + ".min.css"
            with open(min_path,"w",encoding="utf-8") as f: f.write(minified)
            after = os.path.getsize(min_path)
            tot_a += after
            print(f"    {os.path.basename(path):<35} {human_size(before):>8} -> {human_size(after):>8}  {savings(before,after)}")
        except Exception as e:
            print(f"    [!] Erro em {os.path.basename(path)}: {e}")
    print(f"    TOTAL CSS: {human_size(tot_b)} -> {human_size(tot_a)}  {savings(tot_b,tot_a)}")

def minify_js():
    try:
        import rjsmin
    except ImportError:
        print("  [!] rjsmin nao encontrado.")
        return
    print("\n  Minificando JS...")
    tot_b = tot_a = 0
    for path in glob.glob(os.path.join(JS_DIR,"*.js")):
        if path.endswith(".min.js"): continue
        before = os.path.getsize(path)
        tot_b += before
        try:
            with open(path,"r",encoding="utf-8") as f: c = f.read()
            minified = rjsmin.jsmin(c)
            min_path = path[:-3] + ".min.js"
            with open(min_path,"w",encoding="utf-8") as f: f.write(minified)
            after = os.path.getsize(min_path)
            tot_a += after
            print(f"    {os.path.basename(path):<35} {human_size(before):>8} -> {human_size(after):>8}  {savings(before,after)}")
        except Exception as e:
            print(f"    [!] Erro em {os.path.basename(path)}: {e}")
    print(f"    TOTAL JS: {human_size(tot_b)} -> {human_size(tot_a)}  {savings(tot_b,tot_a)}")

if __name__ == "__main__":
    args = sys.argv[1:]
    run_all = not args
    start = time.time()
    print("7x Patrimonial - Build de Assets")
    print("=" * 50)
    if run_all or "--images" in args: compress_images()
    if run_all or "--css" in args: minify_css()
    if run_all or "--js" in args: minify_js()
    print(f"\nConcluido em {time.time()-start:.1f}s")

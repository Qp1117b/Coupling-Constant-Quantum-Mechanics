"""
按需下载 3DSC 的 CIF 文件(可复用工具)
======================================
数据源: aimat-lab/3DSC GitHub, superconductors_3D/data/final/MP/cifs/
        (3DSC, Nature Sci Data 2023, doi:10.1038/s41597-023-02721-y, CC BY 4.0)

用法:
  python download_cifs.py --class Cuprate --max 20     # 下载铜氧化物前20个
  python download_cifs.py --all                         # 下载全部(约5773个, 较慢)
  python download_cifs.py --ids mp-22719 mp-35109       # 按 material_id 下载

断点续传: 已存在的 CIF 自动跳过。
"""
import csv, sys, os, argparse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

DATA = "06 超导/cqm_analysis/data_raw/3DSC_MP.csv"
CIFDIR = "06 超导/cqm_analysis/data_raw/cifs"
BASE = "https://raw.githubusercontent.com/aimat-lab/3DSC/main/superconductors_3D/data/final/MP/"

def load_rows():
    with open(DATA, encoding="utf-8") as fh:
        lines = fh.readlines()
    hi = [i for i, l in enumerate(lines) if l.startswith("formula_sc,")][0]
    hdr = lines[hi].rstrip().split(",")
    return list(csv.DictReader([l for l in lines[hi+1:] if l.strip()], fieldnames=hdr))

def download(cif_path):
    name = os.path.basename(cif_path)
    dst = os.path.join(CIFDIR, name)
    if os.path.exists(dst) and os.path.getsize(dst) > 100:
        return "skip", name
    url = BASE + cif_path.replace("data/final/MP/", "")
    try:
        urllib.request.urlretrieve(url, dst)
        if os.path.getsize(dst) > 100:
            return "ok", name
        os.remove(dst)
        return "empty", name
    except Exception as e:
        return f"err:{type(e).__name__}", name

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--class", dest="cls", default=None)
    ap.add_argument("--max", type=int, default=None)
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    os.makedirs(CIFDIR, exist_ok=True)
    rows = load_rows()
    picked = []
    if args.ids:
        idset = set(args.ids)
        picked = [r for r in rows if r.get("material_id_2", "").strip() in idset]
    elif args.cls:
        picked = [r for r in rows if r.get("sc_class", "") == args.cls and r.get("cif", "").strip()]
    elif args.all:
        picked = [r for r in rows if r.get("cif", "").strip()]
    else:
        # default: one representative per class
        seen = set()
        for r in rows:
            c = r.get("sc_class", "")
            if c not in seen and r.get("cif", "").strip():
                seen.add(c); picked.append(r)

    if args.max:
        picked = picked[:args.max]

    counts = {}
    for r in picked:
        status, name = download(r["cif"].strip())
        counts[status] = counts.get(status, 0) + 1
        print(f"  [{status:12s}] {name}")
    print(f"\nsummary: {counts}  -> {CIFDIR}")

if __name__ == "__main__":
    main()

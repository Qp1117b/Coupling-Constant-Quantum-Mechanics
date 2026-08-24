"""
从AFLOW免费数据库获取Nb的DFT数据

AFLOW API不需要API key，直接用HTTP请求。
文档: https://aflowlib.org/
"""

import urllib.request
import json

# AFLOW API基础URL
AFLOW_URL = "http://aflowlib.org/API/aflux/?"

# 搜索Nb (BCC结构)
# AFLOW用aflux查询语言
query = "species(Nb),catalog(ICSD),natom(1)"
url = AFLOW_URL + query + "&direct"

print("尝试从AFLOW获取Nb的数据...")
print(f"URL: {url}")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read().decode('utf-8')
        print(f"响应长度: {len(data)}")
        print(f"前500字符: {data[:500]}")
except Exception as e:
    print(f"AFLOW请求失败: {e}")

# 尝试直接获取Nb的属性
print("\n尝试获取Nb的基本属性...")
url2 = "http://aflowlib.org/API/aflux/?species(Nb),natom(1),property(auid,structure,geometry)"
try:
    req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read().decode('utf-8')
        print(f"响应长度: {len(data)}")
        print(data[:1000])
except Exception as e:
    print(f"失败: {e}")

# 尝试NIST JARVIS
print("\n尝试NIST JARVIS API...")
# JARVIS REST API
jarvis_url = "https://www.ctcms.nist.gov/~kc6/jdft_3d/jdft_3d.json"
try:
    req = urllib.request.Request(jarvis_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read().decode('utf-8')
        print(f"JARVIS响应长度: {len(data)}")
        # 搜索Nb
        if "Nb" in data:
            print("JARVIS包含Nb数据!")
            # 找到Nb的位置
            idx = data.find('"Nb"')
            if idx > 0:
                print(f"Nb数据片段: {data[idx:idx+500]}")
except Exception as e:
    print(f"JARVIS失败: {e}")
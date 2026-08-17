"""生成 MVP 元素数据 JSON 文件（20个元素，覆盖主要超导体系）"""
import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# MVP 元素数据（实验值来自 NIST/NUBASE）
ELEMENTS = {
    "H": {"Z":1,"name":"氢","name_en":"Hydrogen","mass":1.00794,"cat":"nonmetal","g":1,"p":1,"b":"s","val":1,"en":2.20,"r":53,"cr":31,"color":"#FFFFFF",
          "isotopes":[(1,0,1.007825,0.999855,True,None,None,0.5),(2,1,2.014102,0.000145,True,None,None,1.0),(3,2,3.016049,0.0,False,3.888e8,"beta_minus",0.5)]},
    "He": {"Z":2,"name":"氦","name_en":"Helium","mass":4.002602,"cat":"noble_gas","g":18,"p":1,"b":"s","val":2,"en":0,"r":31,"cr":28,"color":"#D9FFFF",
           "isotopes":[(3,1,3.016029,1.34e-6,True,None,None,0.5),(4,2,4.002603,0.99999866,True,None,None,0.0)]},
    "B": {"Z":5,"name":"硼","name_en":"Boron","mass":10.811,"cat":"metalloid","g":13,"p":2,"b":"p","val":3,"en":2.04,"r":87,"cr":84,"color":"#FFB5B5",
          "isotopes":[(10,5,10.012937,0.199,True,None,None,3.0),(11,6,11.009305,0.801,True,None,None,1.5)]},
    "C": {"Z":6,"name":"碳","name_en":"Carbon","mass":12.0107,"cat":"nonmetal","g":14,"p":2,"b":"p","val":4,"en":2.55,"r":67,"cr":76,"color":"#909090",
          "isotopes":[(12,6,12.0,0.9893,True,None,None,0.0),(13,7,13.003355,0.0107,True,None,None,0.5)]},
    "N": {"Z":7,"name":"氮","name_en":"Nitrogen","mass":14.0067,"cat":"nonmetal","g":15,"p":2,"b":"p","val":5,"en":3.04,"r":56,"cr":71,"color":"#3050F8",
          "isotopes":[(14,7,14.003074,0.99636,True,None,None,1.0),(15,8,15.000109,0.00364,True,None,None,0.5)]},
    "O": {"Z":8,"name":"氧","name_en":"Oxygen","mass":15.9994,"cat":"nonmetal","g":16,"p":2,"b":"p","val":6,"en":3.44,"r":48,"cr":66,"color":"#FF0D0D",
          "isotopes":[(16,8,15.994915,0.99757,True,None,None,0.0),(17,9,16.999132,0.00038,True,None,None,2.5),(18,10,17.999161,0.00205,True,None,None,0.0)]},
    "F": {"Z":9,"name":"氟","name_en":"Fluorine","mass":18.9984,"cat":"halogen","g":17,"p":2,"b":"p","val":7,"en":3.98,"r":42,"cr":57,"color":"#90E050",
          "isotopes":[(19,10,18.998403,1.0,True,None,None,0.5)]},
    "Mg": {"Z":12,"name":"镁","name_en":"Magnesium","mass":24.305,"cat":"alkaline_earth","g":2,"p":3,"b":"s","val":2,"en":1.31,"r":150,"cr":141,"color":"#8AFF00",
           "isotopes":[(24,12,23.985042,0.7899,True,None,None,0.0),(25,13,24.985837,0.1000,True,None,None,2.5),(26,14,25.982593,0.1101,True,None,None,0.0)]},
    "Al": {"Z":13,"name":"铝","name_en":"Aluminum","mass":26.9815,"cat":"post_transition_metal","g":13,"p":3,"b":"p","val":3,"en":1.61,"r":118,"cr":121,"color":"#D8D8D8",
           "isotopes":[(27,14,26.981541,1.0,True,None,None,2.5)]},
    "Si": {"Z":14,"name":"硅","name_en":"Silicon","mass":28.0855,"cat":"metalloid","g":14,"p":3,"b":"p","val":4,"en":1.90,"r":111,"cr":111,"color":"#F0C8A0",
           "isotopes":[(28,14,27.976927,0.92223,True,None,None,0.0),(29,15,28.976495,0.04667,True,None,None,0.5),(30,16,29.973770,0.03110,True,None,None,0.0)]},
    "P": {"Z":15,"name":"磷","name_en":"Phosphorus","mass":30.9738,"cat":"nonmetal","g":15,"p":3,"b":"p","val":5,"en":2.19,"r":98,"cr":107,"color":"#FF8000",
          "isotopes":[(31,16,30.973762,1.0,True,None,None,0.5)]},
    "S": {"Z":16,"name":"硫","name_en":"Sulfur","mass":32.065,"cat":"nonmetal","g":16,"p":3,"b":"p","val":6,"en":2.58,"r":88,"cr":105,"color":"#FFFF30",
          "isotopes":[(32,16,31.972071,0.9499,True,None,None,0.0),(33,17,32.971459,0.0075,True,None,None,1.5),(34,18,33.967867,0.0425,True,None,None,0.0)]},
    "Fe": {"Z":26,"name":"铁","name_en":"Iron","mass":55.845,"cat":"transition_metal","g":8,"p":4,"b":"d","val":2,"en":1.83,"r":126,"cr":125,"color":"#E06600",
           "isotopes":[(54,28,53.939611,0.05845,True,None,None,0.0),(56,30,55.934938,0.91754,True,None,None,0.0),(57,31,56.935394,0.02119,True,None,None,0.5)]},
    "Cu": {"Z":29,"name":"铜","name_en":"Copper","mass":63.546,"cat":"transition_metal","g":11,"p":4,"b":"d","val":1,"en":1.90,"r":128,"cr":132,"color":"#C88040",
           "isotopes":[(63,34,62.929598,0.6915,True,None,None,1.5),(65,36,64.927793,0.3085,True,None,None,1.5)]},
    "Se": {"Z":34,"name":"硒","name_en":"Selenium","mass":78.96,"cat":"nonmetal","g":16,"p":4,"b":"p","val":6,"en":2.55,"r":120,"cr":120,"color":"#A0A040",
           "isotopes":[(74,40,73.922476,0.0089,True,None,None,0.0),(76,42,75.918214,0.0937,True,None,None,0.0),(77,43,76.919914,0.0763,True,None,None,0.5),(78,44,77.917222,0.2377,True,None,None,0.0),(80,46,79.916521,0.4961,True,None,None,0.0)]},
    "Sr": {"Z":38,"name":"锶","name_en":"Strontium","mass":87.62,"cat":"alkaline_earth","g":2,"p":5,"b":"s","val":2,"en":0.95,"r":195,"cr":195,"color":"#FFAB00",
           "isotopes":[(84,46,83.913430,0.0056,True,None,None,0.0),(86,48,85.909260,0.0986,True,None,None,0.0),(87,49,86.908877,0.0700,True,None,None,4.5),(88,50,87.905612,0.8258,True,None,None,0.0)]},
    "Y": {"Z":39,"name":"钇","name_en":"Yttrium","mass":88.9059,"cat":"transition_metal","g":3,"p":5,"b":"d","val":3,"en":1.22,"r":180,"cr":169,"color":"#80E0E0",
          "isotopes":[(89,50,88.905848,1.0,True,None,None,0.5)]},
    "Nb": {"Z":41,"name":"铌","name_en":"Niobium","mass":92.9064,"cat":"transition_metal","g":5,"p":5,"b":"d","val":5,"en":1.6,"r":146,"cr":164,"color":"#40C0C0",
           "isotopes":[(93,52,92.906373,1.0,True,None,None,4.5)]},
    "Ba": {"Z":56,"name":"钡","name_en":"Barium","mass":137.327,"cat":"alkaline_earth","g":2,"p":6,"b":"s","val":2,"en":0.89,"r":215,"cr":198,"color":"#00C000",
           "isotopes":[(130,74,129.906094,0.00106,True,None,None,0.0),(132,76,131.904153,0.00101,True,None,None,0.0),(134,78,133.904503,0.02417,True,None,None,0.0),(135,79,134.905672,0.07185,True,None,None,1.5),(136,80,135.904575,0.07865,True,None,None,0.0),(137,81,136.905821,0.11232,True,None,None,1.5),(138,82,137.905247,0.71698,True,None,None,0.0)]},
    "La": {"Z":57,"name":"镧","name_en":"Lanthanum","mass":138.905,"cat":"lanthanide","g":3,"p":6,"b":"f","val":3,"en":1.10,"r":195,"cr":207,"color":"#56E0E0",
           "isotopes":[(138,81,137.907112,0.00088,True,None,None,5.0),(139,82,138.90636,0.99911,True,None,None,3.5)]},
    "Te": {"Z":52,"name":"碲","name_en":"Tellurium","mass":127.6,"cat":"metalloid","g":16,"p":5,"b":"p","val":6,"en":2.1,"r":123,"cr":138,"color":"#808090",
           "isotopes":[(120,68,119.90402,0.0009,True,None,None,0.0),(122,70,121.90304,0.0255,True,None,None,0.0),(124,72,123.90282,0.0472,True,None,None,0.0),(125,73,124.90443,0.0707,True,None,None,0.5),(126,74,125.90331,0.1884,True,None,None,0.0),(128,76,127.90446,0.3174,True,None,None,0.0),(130,78,129.90622,0.3408,True,None,None,0.0)]},
}

def make_isotope(iso_tuple):
    A, N, mass, ab, stable, hl, decay, spin = iso_tuple
    return {
        "mass_number": A,
        "neutrons": N,
        "mass_da": mass,
        "abundance": ab,
        "is_stable": stable,
        "half_life_s": hl,
        "decay_mode": decay,
        "spin": spin
    }

def make_element(sym, info):
    return {
        "symbol": sym,
        "name": info["name"],
        "name_en": info["name_en"],
        "atomic_number": info["Z"],
        "atomic_mass": info["mass"],
        "category": info["cat"],
        "group": info["g"],
        "period": info["p"],
        "block": info["b"],
        "valence_electrons": info["val"],
        "electronegativity": info["en"],
        "atomic_radius_pm": info["r"],
        "covalent_radius_pm": info["cr"],
        "color": info["color"],
        "isotopes": [make_isotope(i) for i in info["isotopes"]]
    }

def main():
    elements = {}
    by_number = {}
    categories = {}

    for sym, info in ELEMENTS.items():
        data = make_element(sym, info)
        path = os.path.join(OUTPUT_DIR, f"{sym}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        elements[sym] = {"Z": info["Z"], "file": f"{sym}.json", "isotope_count": len(info["isotopes"])}
        by_number[str(info["Z"])] = sym
        cat = info["cat"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(sym)

    index = {
        "version": "1.0",
        "element_count": len(ELEMENTS),
        "isotope_count": sum(len(info["isotopes"]) for info in ELEMENTS.values()),
        "elements": elements,
        "by_number": by_number,
        "categories": categories
    }

    with open(os.path.join(OUTPUT_DIR, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"已生成 {len(ELEMENTS)} 个元素文件 + 索引")

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""缺口闭合贝叶斯网络：加载 BIF 并做后验推断（对接 pgmpy）。未安装 pgmpy 时打印网络结构。"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
BIF = os.path.join(HERE, "gap_closure_model.bif")

def structure():
    return {"nodes": ["G2","G3","G4","G5","C_gap","C_core","G13","G14","SC_chain","Formal_status"],
            "edges": [("G2","G3"),("G3","G4"),("G4","G5"),("C_gap","C_core"),
                      ("G13","SC_chain"),("G14","SC_chain"),
                      ("C_core","Formal_status"),("SC_chain","Formal_status")],
            "states": ["闭合","部分","未闭合"]}

def run():
    try:
        from pgmpy.readwrite import BIFReader
        m = BIFReader(BIF).get_model()
        from pgmpy.inference import VariableElimination
        inf = VariableElimination(m)
        print(inf.query(["Formal_status"], evidence={"G13":"闭合","G14":"闭合"}))
    except ImportError:
        print("pgmpy 未安装：pip install pgmpy。网络结构：")
        print(structure())

if __name__ == "__main__":
    run()

import streamlit as st
import networkx as nx
import dimod
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cyber Quantum PoC", page_icon="🛡️")

st.title("量子最適化：サイバー攻撃隔離シミュレータ")
st.markdown("""
### AI増殖時代のセグメンテーション
AIマルウェアの爆発的な増殖に対し、量子アニーリング（Max-Cut）を用いて
**「被害を最小化するネットワーク分断ライン」**を瞬時に算出します。
""")

# 設定パラメータ
num_nodes = st.sidebar.slider("サーバー台数 (AI増殖規模)", 5, 30, 15)
edge_prob = st.sidebar.slider("ネットワーク接続密度", 0.1, 0.5, 0.2)

if st.button("量子最適化による隔離を実行"):
    with st.spinner('量子アルゴリズム実行中...'):
        # 1. ネットワーク生成
        G = nx.erdos_renyi_graph(num_nodes, edge_prob, seed=42)
        
        # 2. QUBO構築
        Q = {}
        # 全てのノードを一旦QUBOに登録（KeyError防止）
        for node in G.nodes:
            Q[(node, node)] = 0
            
        for u, v in G.edges:
            Q[(u, u)] -= 1
            Q[(v, v)] -= 1
            Q[(u, v)] += 2

        # 3. 疑似量子アニーリング
        sampler = dimod.SimulatedAnnealingSampler()
        response = sampler.sample_qubo(Q, num_reads=20)
        best_solution = response.first.sample

        # 4. 可視化
        fig, ax = plt.subplots(figsize=(10, 7))
        # 修正ポイント：.get(node, 0) を使って、計算に含まれなかったノードもエラーにしない
        color_map = ['#FF4C4C' if best_solution.get(node, 0) == 1 else '#4C9AFF' for node in G.nodes]
        pos = nx.spring_layout(G, seed=42)
        
        nx.draw(G, pos, with_labels=True, node_color=color_map, 
                node_size=800, font_color='white', font_weight='bold', edge_color='#D3D3D3')
        
        st.pyplot(fig)
        st.success(f"計算完了: 通信を遮断すべき境界（Max-Cut）を特定しました。")
        st.info("赤色と青色のグループ間の線をすべて遮断することで、感染拡大を物理的に封じ込めます。")

import networkx as nx

def build_graph_and_calculate(images_data):
    """
    Принимает список словарей с ключами: id, name, type, tags.
    Возвращает словарь с результатами работы модели.
    """
    G = nx.DiGraph()
    
    # 1. Добавляем вершины
    for img in images_data:
        G.add_node(img['id'], **img)
        
    # 2. Строим связи на основе тегов
    for i in range(len(images_data)):
        for j in range(i + 1, len(images_data)):
            img1 = images_data[i]
            img2 = images_data[j]
            
            tags1 = set(t.strip() for t in img1['tags'].split(',') if t.strip())
            tags2 = set(t.strip() for t in img2['tags'].split(',') if t.strip())
            
            intersection = tags1.intersection(tags2)
            union = tags1.union(tags2)
            
            if intersection:
                weight = len(intersection) / len(union) if union else 0
                if img1['type'] == 0 and img2['type'] == 1:
                    G.add_edge(img1['id'], img2['id'], weight=weight)
                elif img1['type'] == 1 and img2['type'] == 0:
                    G.add_edge(img2['id'], img1['id'], weight=weight)

    # 3. Секвенция (топологическая сортировка с разрывом циклов)
    try:
        sorted_ids = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
        G.remove_edge(edges[0][0], edges[0][1])
        sorted_ids = list(nx.topological_sort(G))

    # 4. Извлечение целей
    goals = []
    for u, v, data in G.edges(data=True):
        goals.append({
            "from": G.nodes[u]["name"],
            "to": G.nodes[v]["name"],
            "weight": round(data['weight'], 2),
            "resources": ["время", "деньги"]
        })

    # 5. Когерентность (упрощенная проверка на конфликт ресурсов)
    conflicts = 0
    pairs = 0
    for i in range(len(goals)):
        for j in range(i + 1, len(goals)):
            pairs += 1
            if "деньги" in goals[i]["resources"] and "деньги" in goals[j]["resources"]:
                conflicts += 1

    K = 1 - (conflicts / pairs) if pairs > 0 else 1.0

    # 6. Приоритет
    for g in goals:
        importance = g["weight"]
        urgency = 0.5 
        dependency = 0.5
        P = 0.3 * urgency + 0.4 * importance + 0.2 * (1 - dependency) + 0.1 * K
        g["priority"] = round(P, 2)

    goals.sort(key=lambda x: x["priority"], reverse=True)

    return {
        "total_images": len(images_data),
        "sequence": sorted_ids,
        "goals": goals,
        "coherence_K": round(K, 2)
    }
import pandas as pd
import json

def create_root_node(name, describes):
    """创建树的根节点"""
    return {
        "name": name,
        "describes": describes,
        "children": []
    }

def add_node(nodes, comment_id, parent_id, name, describes):
    """向树中添加一个节点"""
    node = {"name": name, "describes": describes, "children": []}
    nodes[comment_id] = node
    parent_node = nodes.get(parent_id)
    if parent_node:
        parent_node["children"].append(node)

def build_tree(df, root):
    """基于DataFrame构建评论树"""
    nodes = {df.iloc[0]['目标评论ID']: root}
    for _, row in df.iterrows():
        add_node(nodes, row['评论ID'], row['目标评论ID'], row['用户昵称'], row['评论内容'])
    return nodes

def node_has_descendant_at_level(node, current_level, target_level):
    """检查节点是否有在目标层级或更深层级的子孙节点"""
    if current_level >= target_level:
        return True
    for child in node['children']:
        if node_has_descendant_at_level(child, current_level + 1, target_level):
            return True
    return False

def prune_tree(node, current_level, target_level):
    """根据层级修剪树，只保留到达目标层级的节点及其所有父节点和子节点"""
    node['children'] = [
        child for child in node['children']
        if node_has_descendant_at_level(child, current_level + 1, target_level)
    ]
    for child in node['children']:
        prune_tree(child, current_level + 1, target_level)

def save_tree_to_json(root, file_path):
    """将树结构保存到JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(root, f, ensure_ascii=False, indent=4)
    print("JSON file has been saved successfully.")

def main(filename,rootname,rootcontent,level):
    file_path = filename
    df = pd.read_excel(file_path)

    root = create_root_node(rootname, rootcontent)
    nodes = build_tree(df, root)

    target_level = level  # 设置目标层级
    prune_tree(root, 0, target_level)  # 从根节点开始修剪树

    save_tree_to_json(root, '评论树结构.json')

if __name__ == '__main__':
    # 设置文件位置
    file_path = 'demo.xlsx'

    # 设置初节点信息
    rootname = '末代赤佬'
    rootcontent = '我爸没给我买保护的，当初知道我谈女朋友以后送了我一张2000元的酒店代金券…………'

    # 设置层级信息
    level = 2

    main(file_path,rootname,rootcontent,level)

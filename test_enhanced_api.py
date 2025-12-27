"""测试增强的 API 功能"""

from src.api import generate_cif, generate_multiple_mofs
from pathlib import Path

print("=" * 70)
print("测试增强的 ToBaCCo API")
print("=" * 70)

# 获取可用的构建块
from src.utils.paths import TEMPLATES_DIR, NODES_DIR, EDGES_DIR

templates = [f.stem for f in TEMPLATES_DIR.glob("*.cif")][:2]
nodes = [f.stem for f in NODES_DIR.glob("*.cif")][:2]
edges = [f.stem for f in EDGES_DIR.glob("*.cif")][:2]

print(f"\n可用的构建块:")
print(f"  模板: {templates}")
print(f"  节点: {nodes}")
print(f"  边: {edges}")

# 测试 1: 单个字符串输入
print("\n" + "=" * 70)
print("测试 1: 单个字符串输入")
print("=" * 70)
try:
    result = generate_cif(
        template_name=templates[0],
        node_names=nodes[0],
        edge_names=edges[0],
        return_format='file',
        config={'CHARGES': False}
    )
    print(f"✓ 成功生成: {result['cifname']}")
    print(f"  文件路径: {result['file_path']}")
except Exception as e:
    print(f"✗ 错误: {e}")

# 测试 2: 列表输入
print("\n" + "=" * 70)
print("测试 2: 列表输入")
print("=" * 70)
try:
    result = generate_cif(
        template_name=[templates[0]],
        node_names=[nodes[0]],
        edge_names=[edges[0]],
        return_format='file',
        config={'CHARGES': False}
    )
    print(f"✓ 成功生成: {result['cifname']}")
except Exception as e:
    print(f"✗ 错误: {e}")

# 测试 3: 字典输入（节点）
print("\n" + "=" * 70)
print("测试 3: 字典输入（节点顶点映射）")
print("=" * 70)
try:
    result = generate_cif(
        template_name=templates[0],
        node_names={'V1': nodes[0]},
        edge_names=edges[0],
        return_format='file',
        config={'CHARGES': False}
    )
    print(f"✓ 成功生成: {result['cifname']}")
except Exception as e:
    print(f"✗ 错误: {e}")

# 测试 4: return_format='string'
print("\n" + "=" * 70)
print("测试 4: 返回格式 = 'string'")
print("=" * 70)
try:
    result = generate_cif(
        template_name=templates[0],
        node_names=nodes[0],
        edge_names=edges[0],
        return_format='string',
        config={'CHARGES': False}
    )
    if isinstance(result, str):
        print(f"✓ 返回字符串，长度: {len(result)} 字符")
        print(f"  前 100 个字符: {result[:100]}...")
    elif isinstance(result, tuple):
        print(f"✓ 返回元组（字符串 + 元数据）")
        print(f"  CIF 长度: {len(result[0])} 字符")
        print(f"  元数据键: {list(result[1].keys())}")
    else:
        print(f"✗ 意外的类型: {type(result)}")
except Exception as e:
    print(f"✗ 错误: {e}")

# 测试 5: return_format='json'
print("\n" + "=" * 70)
print("测试 5: 返回格式 = 'json'")
print("=" * 70)
try:
    result = generate_cif(
        template_name=templates[0],
        node_names=nodes[0],
        edge_names=edges[0],
        return_format='json',
        config={'CHARGES': False}
    )
    if isinstance(result, dict):
        print(f"✓ 返回 JSON 字典")
        print(f"  键: {list(result.keys())}")
        for key in result.keys():
            print(f"  '{key}' 包含:")
            print(f"    - cif_content: {len(result[key]['cif_content'])} 字符")
            if 'metadata' in result[key]:
                print(f"    - metadata: {list(result[key]['metadata'].keys())}")
    else:
        print(f"✗ 意外的类型: {type(result)}")
except Exception as e:
    print(f"✗ 错误: {e}")

# 测试 6: generate_multiple_mofs
print("\n" + "=" * 70)
print("测试 6: generate_multiple_mofs 函数")
print("=" * 70)
try:
    combinations = [
        {'template': templates[0], 'nodes': nodes[0], 'edges': edges[0]}
    ]
    if len(templates) > 1:
        combinations.append(
            {'template': templates[1], 'nodes': nodes[0], 'edges': edges[0]}
        )
    
    results = generate_multiple_mofs(
        combinations=combinations,
        return_format='file',
        config={'CHARGES': False}
    )
    print(f"✓ 成功生成 {len(results)} 个 MOF")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['cifname']}")
except Exception as e:
    print(f"✗ 错误: {e}")

# 测试 7: 多个模板输入
print("\n" + "=" * 70)
print("测试 7: 多个模板输入")
print("=" * 70)
if len(templates) > 1:
    try:
        result = generate_cif(
            template_name=templates[:2],  # 使用前两个模板
            node_names=nodes[0],
            edge_names=edges[0],
            return_format='file',
            config={'CHARGES': False}
        )
        if isinstance(result, list):
            print(f"✓ 成功生成 {len(result)} 个 MOF")
            for r in result:
                print(f"  - {r['cifname']}")
        else:
            print(f"✓ 成功生成 1 个 MOF: {result['cifname']}")
    except Exception as e:
        print(f"✗ 错误: {e}")
else:
    print("⊘ 跳过（模板数量不足）")

# 测试 8: 确定性电荷生成
print("\n" + "=" * 70)
print("测试 8: 确定性电荷生成（相同种子）")
print("=" * 70)
try:
    result1 = generate_cif(
        template_name=templates[0],
        node_names=nodes[0],
        edge_names=edges[0],
        return_format='file',
        random_seed=42,
        config={'CHARGES': True}
    )
    
    result2 = generate_cif(
        template_name=templates[0],
        node_names=nodes[0],
        edge_names=edges[0],
        return_format='file',
        random_seed=42,
        config={'CHARGES': True}
    )
    
    print(f"✓ 两次生成完成")
    print(f"  结果 1: {result1['cifname']}")
    print(f"  结果 2: {result2['cifname']}")
    print(f"  种子: {result1['metadata']['random_seed']}")
    
    # 检查 CIF 内容是否相同
    if result1['cif_content'] == result2['cif_content']:
        print(f"✓ CIF 内容完全相同（确定性验证成功）")
    else:
        print(f"✗ CIF 内容不同（确定性验证失败）")
        
except Exception as e:
    print(f"✗ 错误: {e}")

print("\n" + "=" * 70)
print("测试完成！")
print("=" * 70)

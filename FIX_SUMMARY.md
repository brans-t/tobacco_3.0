# 文件修复总结 / File Fix Summary

## 修复日期 / Fix Date
2024年12月28日 / December 28, 2024

---

## 问题描述 / Problem Description

### 文件
`examples/multiple_input_example.py`

### 错误信息
```
ValueError: No valid vertex assignment found. At least one vertex does not have 
a building block with the correct number of connection sites.
```

### 根本原因 / Root Cause
示例代码中使用了不兼容的节点-模板组合：
- `pcb` 模板需要 **4连接** 的节点
- 代码中错误地使用了 **6连接** 的节点 (`6c_Al_1`)

The example code used incompatible node-template combinations:
- `pcb` template requires **4-connected** nodes
- Code incorrectly used **6-connected** nodes (`6c_Al_1`)

---

## 修复方案 / Solution

### 修改前 / Before
```python
combinations = [
    {
        'template': 'pcb',
        'nodes': ['6c_Al_1'],      # ❌ 错误：6连接节点用于4连接模板
        'edges': ['1B_2CF3_Ch']
    },
    {
        'template': 'pcb',
        'nodes': ['6c_Al_1'],      # ❌ 错误
        'edges': ['2B_2Br_Ch']
    },
    # ... 更多错误组合
]
```

### 修改后 / After
```python
combinations = [
    {
        'template': 'pcb',
        'nodes': ['4c_Cd_1_Ch'],   # ✅ 正确：4连接节点用于4连接模板
        'edges': ['1B_2CF3_Ch']
    },
    {
        'template': 'pcb',
        'nodes': ['4c_Cd_1_Ch'],   # ✅ 正确
        'edges': ['2B_2Br_Ch']
    },
    {
        'template': 'pcb',
        'nodes': ['4c_Cd_1_Ch'],   # ✅ 正确
        'edges': ['2B_2NH2_Ch']
    },
    {
        'template': 'pcu',
        'nodes': ['6c_Al_1'],      # ✅ 正确：6连接节点用于6连接模板
        'edges': ['1B_2CF3_Ch']
    },
    {
        'template': 'pcu',
        'nodes': ['6c_Al_1'],      # ✅ 正确
        'edges': ['2B_2Br_Ch']
    },
    {
        'template': 'pcu',
        'nodes': ['6c_Al_1'],      # ✅ 正确
        'edges': ['2B_2NH2_Ch']
    }
]
```

---

## 关键知识点 / Key Points

### 节点-模板兼容性 / Node-Template Compatibility

#### 模板连接要求 / Template Connection Requirements
- **pcb**: 需要 4连接节点 (4-connected nodes)
- **pcu**: 需要 6连接节点 (6-connected nodes)
- **dia**: 需要 4连接节点 (4-connected nodes)
- **fcu**: 需要 12连接节点 (12-connected nodes)

#### 节点命名规则 / Node Naming Convention
节点文件名格式：`{连接数}c_{金属}_{编号}_{类型}.cif`

Node filename format: `{connectivity}c_{metal}_{number}_{type}.cif`

**示例 / Examples:**
- `4c_Cd_1_Ch` → 4连接的镉节点 (4-connected Cadmium node)
- `6c_Al_1` → 6连接的铝节点 (6-connected Aluminum node)
- `6c_Cu_1_Ch` → 6连接的铜节点 (6-connected Copper node)
- `12c_Ce_1_Ch` → 12连接的铈节点 (12-connected Cerium node)

### 如何避免此错误 / How to Avoid This Error

#### 1. 检查模板要求 / Check Template Requirements
```python
# 查看模板的连接要求
# Check template connectivity requirements
from src.utils.paths import get_template_path
# 读取模板文件查看顶点连接数
# Read template file to see vertex connectivity
```

#### 2. 匹配节点连接数 / Match Node Connectivity
```python
# 确保节点连接数与模板要求匹配
# Ensure node connectivity matches template requirements

# ✅ 正确示例 / Correct examples
generate_cif("pcb", "4c_Cd_1_Ch", "1B_2CF3_Ch")  # 4连接
generate_cif("pcu", "6c_Al_1", "1B_2CF3_Ch")     # 6连接

# ❌ 错误示例 / Wrong examples
generate_cif("pcb", "6c_Al_1", "1B_2CF3_Ch")     # 不匹配！
generate_cif("pcu", "4c_Cd_1_Ch", "1B_2CF3_Ch")  # 不匹配！
```

#### 3. 使用配置选项 / Use Configuration Options
```python
# 让 ToBaCCo 自动选择兼容的节点
# Let ToBaCCo automatically select compatible nodes
config = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': False  # 自动选择
}

result = generate_cif(
    template_name="pcb",
    node_names="4c_Cd_1_Ch",  # 提供候选节点
    edge_names="1B_2CF3_Ch",
    config=config
)
```

---

## 测试结果 / Test Results

### 修复前 / Before Fix
```
[ERROR] ValueError: No valid vertex assignment found.
```

### 修复后 / After Fix
```
[OK] Generated 6 MOFs!

  MOF 1: pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif
  MOF 2: pcb_V-4c_Cd_1_Ch_1-2B_2Br_Ch.cif
  MOF 3: pcb_V-4c_Cd_1_Ch_1-2B_2NH2_Ch.cif
  MOF 4: pcu_V-6c_Al_1_1-1B_2CF3_Ch.cif
  MOF 5: pcu_V-6c_Al_1_1-2B_2Br_Ch.cif
  MOF 6: pcu_V-6c_Al_1_1-2B_2NH2_Ch.cif

All Examples Complete!
```

✅ 所有6个MOF成功生成！/ All 6 MOFs generated successfully!

---

## 常见模板-节点组合 / Common Template-Node Combinations

### 推荐组合 / Recommended Combinations

| 模板 / Template | 连接数 / Connectivity | 推荐节点 / Recommended Nodes |
|----------------|---------------------|----------------------------|
| pcb | 4 | 4c_Cd_1_Ch, 4c_Zn_1_Ch |
| pcu | 6 | 6c_Al_1, 6c_Cu_1_Ch |
| dia | 4 | 4c_Cd_1_Ch, 4c_Zn_1_Ch |
| fcu | 12 | 12c_Ce_1_Ch |
| acsh | 12 | 12c_Ce_1_Ch |

### 测试组合 / Testing Combinations
```python
# 安全的测试组合 / Safe test combinations
safe_combinations = [
    ("pcb", "4c_Cd_1_Ch", "1B_2CF3_Ch"),
    ("pcu", "6c_Al_1", "1B_2CF3_Ch"),
    ("pcu", "6c_Cu_1_Ch", "1B_1TrU"),
    ("acsh", "12c_Ce_1_Ch", "1B_1TrU"),
]

for template, node, edge in safe_combinations:
    result = generate_cif(template, node, edge)
    print(f"✓ {template} + {node} + {edge}")
```

---

## 相关文档 / Related Documentation

### 查看更多信息 / For More Information
- **配置指南 / Configuration Guide**: `docs/CONFIGURATION.md`
- **API文档 / API Documentation**: `docs/API_DOCUMENTATION.md`
- **示例指南 / Examples Guide**: `examples/README.md`
- **完整手册 / Complete Manual**: `docs/tobacco_3.0_manual.pdf`

### 相关示例 / Related Examples
- `examples/quick_start.py` - 基本用法 / Basic usage
- `examples/single_input_example.py` - 单个MOF生成 / Single MOF generation
- `examples/multiple_input_example.py` - 批量生成 / Batch generation (已修复 / Fixed)

---

## 总结 / Summary

### 问题 / Problem
示例代码使用了不兼容的节点-模板组合导致生成失败。

Example code used incompatible node-template combinations causing generation failure.

### 解决方案 / Solution
修正节点-模板配对，确保连接数匹配。

Corrected node-template pairing to ensure connectivity matches.

### 结果 / Result
✅ 文件现在可以正常运行并成功生成6个MOF结构。

✅ File now runs successfully and generates 6 MOF structures.

### 经验教训 / Lessons Learned
1. 始终检查节点连接数与模板要求是否匹配
2. 节点文件名中的数字表示连接数（如 `4c_` = 4连接）
3. 使用 `USER_SPECIFIED_NODE_ASSIGNMENT: False` 可以让系统自动选择兼容节点

1. Always check node connectivity matches template requirements
2. Number in node filename indicates connectivity (e.g., `4c_` = 4-connected)
3. Use `USER_SPECIFIED_NODE_ASSIGNMENT: False` to let system auto-select compatible nodes

---

**修复完成 / Fix Completed:** 2024年12月28日 / December 28, 2024  
**状态 / Status:** ✅ 已解决 / Resolved  
**测试 / Tested:** ✅ 通过 / Passed

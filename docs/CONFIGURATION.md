# ToBaCCo 配置指南 / Configuration Guide

[English](#english-version) | [中文](#中文版本)

---

## English Version

### Overview

The `configuration.py` file contains all global settings that control how ToBaCCo generates MOF structures. These settings affect everything from output format to optimization parameters.

### Configuration Methods

#### Method 1: Global Configuration File
Edit `configuration.py` to set defaults for all generations:

```python
# configuration.py
CHARGES = True
SCALING_ITERATIONS = 3
RANDOM_SEED = 42
```

#### Method 2: API Parameter (Recommended)
Override configuration for specific generations:

```python
from src.api import generate_cif

config = {
    'CHARGES': True,
    'SCALING_ITERATIONS': 3,
    'RANDOM_SEED': 42
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    config=config
)
```

### Key Configuration Options

#### Input/Output Control

**INPUT_SOURCE** (String, default: `'auto'`)
- `'auto'`: Try JSON database first, fallback to CIF files (recommended)
- `'json'`: Load only from JSON databases (faster)
- `'cif'`: Load only from CIF files

**DEFAULT_RETURN_FORMAT** (String, default: `'file'`)
- `'file'`: Save to file and return path
- `'string'`: Return CIF content as string
- `'json'`: Return as JSON object with metadata

**WRITE_CIF** (Boolean, default: `True`)
- Write final CIF files to `output/cifs/`

**WRITE_CHECK_FILES** (Boolean, default: `False`)
- Write intermediate check files for debugging

#### Charge Generation

**CHARGES** (Boolean, default: `True`)
- Include atomic charges in output CIF files

**RANDOM_SEED** (Integer, default: `42`)
- Seed for deterministic charge generation
- Same seed produces identical charges
- Essential for reproducible research

**REMOVE_DUMMY_ATOMS** (Boolean, default: `True`)
- Remove dummy atoms (Fr) from final output

#### Structure Generation

**USER_SPECIFIED_NODE_ASSIGNMENT** (Boolean, default: `False`)
- `True`: Only use nodes specified in `node_names` parameter
- `False`: Consider all available nodes in database

**SCALING_ITERATIONS** (Integer, default: `1`)
- Number of unit cell optimization iterations
- Higher values improve optimization but increase time

**ALL_NODE_COMBINATIONS** (Boolean, default: `False`)
- Try all possible combinations of node assignments

**COMBINATORIAL_EDGE_ASSIGNMENT** (Boolean, default: `True`)
- Generate all possible edge assignment combinations

**ORIENTATION_DEPENDENT_NODES** (Boolean, default: `False`)
- Consider node orientation during placement

#### Geometric Parameters

**CONNECTION_SITE_BOND_LENGTH** (Float, default: `1.54` Å)
- Target bond length at connection sites

**BOND_TOL** (Float, default: `5.0` Å)
- Tolerance for bond distance detection

**MIN_CELL_LENGTH** (Float, default: `5.0` Å)
- Minimum unit cell length

**SYMMETRY_TOL** (Dictionary)
- Symmetry tolerance for different coordination numbers
- Format: `{coordination_number: tolerance}`

#### Optimization Parameters

**OPT_METHOD** (String, default: `'L-BFGS-B'`)
- Optimization method for unit cell scaling

**PRE_SCALE** (Float, default: `1.00`)
- Pre-scaling factor for unit cell

**FIX_UC** (Tuple, default: `(0,0,0,0,0,0)`)
- Fix unit cell parameters during optimization
- Format: `(a, b, c, alpha, beta, gamma)` where 1=fixed, 0=free

#### Structure Filtering

**SINGLE_METAL_MOFS_ONLY** (Boolean, default: `True`)
- Only generate structures with a single metal type

**MOFS_ONLY** (Boolean, default: `True`)
- Only generate MOF structures (require metal nodes)

**MERGE_CATENATED_NETS** (Boolean, default: `True`)
- Merge interpenetrated/catenated networks

### Common Configuration Scenarios

#### Quick Testing
```python
config = {
    'CHARGES': False,
    'SCALING_ITERATIONS': 1,
    'COMBINATORIAL_EDGE_ASSIGNMENT': False,
    'INPUT_SOURCE': 'auto'
}
```

#### High-Quality Production
```python
config = {
    'CHARGES': True,
    'RANDOM_SEED': 42,
    'SCALING_ITERATIONS': 5,
    'BOND_TOL': 3.0,
    'INPUT_SOURCE': 'json'
}
```

#### Reproducible Research
```python
config = {
    'RANDOM_SEED': 42,
    'CHARGES': True,
    'SCALING_ITERATIONS': 3,
    'INPUT_SOURCE': 'json'
}
```

### Quick Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `CHARGES` | bool | `True` | Include atomic charges |
| `RANDOM_SEED` | int | `42` | Seed for charge generation |
| `SCALING_ITERATIONS` | int | `1` | Optimization iterations |
| `USER_SPECIFIED_NODE_ASSIGNMENT` | bool | `False` | Use only specified nodes |
| `MIN_CELL_LENGTH` | float | `5.0` | Minimum cell length (Å) |
| `BOND_TOL` | float | `5.0` | Bond tolerance (Å) |
| `INPUT_SOURCE` | str | `'auto'` | Database source |
| `DEFAULT_RETURN_FORMAT` | str | `'file'` | Output format |

---

## 中文版本

### 概述

`configuration.py` 文件包含控制 ToBaCCo 生成 MOF 结构的所有全局设置。这些设置影响从输出格式到优化参数的所有内容。

### 配置方法

#### 方法 1: 全局配置文件
编辑 `configuration.py` 设置所有生成的默认值：

```python
# configuration.py
CHARGES = True
SCALING_ITERATIONS = 3
RANDOM_SEED = 42
```

#### 方法 2: API 参数（推荐）
为特定生成覆盖配置：

```python
from src.api import generate_cif

config = {
    'CHARGES': True,
    'SCALING_ITERATIONS': 3,
    'RANDOM_SEED': 42
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    config=config
)
```

### 主要配置选项

#### 输入/输出控制

**INPUT_SOURCE** (字符串，默认: `'auto'`)
- `'auto'`: 优先尝试 JSON 数据库，回退到 CIF 文件（推荐）
- `'json'`: 仅从 JSON 数据库加载（更快）
- `'cif'`: 仅从 CIF 文件加载

**DEFAULT_RETURN_FORMAT** (字符串，默认: `'file'`)
- `'file'`: 保存到文件并返回路径
- `'string'`: 返回 CIF 内容字符串
- `'json'`: 返回带元数据的 JSON 对象

**WRITE_CIF** (布尔值，默认: `True`)
- 将最终 CIF 文件写入 `output/cifs/`

**WRITE_CHECK_FILES** (布尔值，默认: `False`)
- 写入中间检查文件用于调试

#### 电荷生成

**CHARGES** (布尔值，默认: `True`)
- 在输出 CIF 文件中包含原子电荷

**RANDOM_SEED** (整数，默认: `42`)
- 确定性电荷生成的种子
- 相同种子产生相同电荷
- 对可重现研究至关重要

**REMOVE_DUMMY_ATOMS** (布尔值，默认: `True`)
- 从最终输出中移除虚拟原子 (Fr)

#### 结构生成

**USER_SPECIFIED_NODE_ASSIGNMENT** (布尔值，默认: `False`)
- `True`: 仅使用 `node_names` 参数中指定的节点
- `False`: 考虑数据库中所有可用节点

**SCALING_ITERATIONS** (整数，默认: `1`)
- 单元格优化迭代次数
- 更高的值改善优化但增加时间

**ALL_NODE_COMBINATIONS** (布尔值，默认: `False`)
- 尝试所有可能的节点分配组合

**COMBINATORIAL_EDGE_ASSIGNMENT** (布尔值，默认: `True`)
- 生成所有可能的边分配组合

**ORIENTATION_DEPENDENT_NODES** (布尔值，默认: `False`)
- 在放置期间考虑节点方向

#### 几何参数

**CONNECTION_SITE_BOND_LENGTH** (浮点数，默认: `1.54` Å)
- 连接位点的目标键长

**BOND_TOL** (浮点数，默认: `5.0` Å)
- 键距离检测的容差

**MIN_CELL_LENGTH** (浮点数，默认: `5.0` Å)
- 最小单元格长度

**SYMMETRY_TOL** (字典)
- 不同配位数的对称性容差
- 格式: `{配位数: 容差}`

#### 优化参数

**OPT_METHOD** (字符串，默认: `'L-BFGS-B'`)
- 单元格缩放的优化方法

**PRE_SCALE** (浮点数，默认: `1.00`)
- 单元格的预缩放因子

**FIX_UC** (元组，默认: `(0,0,0,0,0,0)`)
- 在优化期间固定单元格参数
- 格式: `(a, b, c, alpha, beta, gamma)` 其中 1=固定，0=自由

#### 结构过滤

**SINGLE_METAL_MOFS_ONLY** (布尔值，默认: `True`)
- 仅生成单一金属类型的结构

**MOFS_ONLY** (布尔值，默认: `True`)
- 仅生成 MOF 结构（需要金属节点）

**MERGE_CATENATED_NETS** (布尔值，默认: `True`)
- 合并互穿/链接的网络

### 常见配置场景

#### 快速测试
```python
config = {
    'CHARGES': False,
    'SCALING_ITERATIONS': 1,
    'COMBINATORIAL_EDGE_ASSIGNMENT': False,
    'INPUT_SOURCE': 'auto'
}
```

#### 高质量生产
```python
config = {
    'CHARGES': True,
    'RANDOM_SEED': 42,
    'SCALING_ITERATIONS': 5,
    'BOND_TOL': 3.0,
    'INPUT_SOURCE': 'json'
}
```

#### 可重现研究
```python
config = {
    'RANDOM_SEED': 42,
    'CHARGES': True,
    'SCALING_ITERATIONS': 3,
    'INPUT_SOURCE': 'json'
}
```

### 快速参考

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `CHARGES` | bool | `True` | 包含原子电荷 |
| `RANDOM_SEED` | int | `42` | 电荷生成种子 |
| `SCALING_ITERATIONS` | int | `1` | 优化迭代次数 |
| `USER_SPECIFIED_NODE_ASSIGNMENT` | bool | `False` | 仅使用指定节点 |
| `MIN_CELL_LENGTH` | float | `5.0` | 最小单元格长度 (Å) |
| `BOND_TOL` | float | `5.0` | 键容差 (Å) |
| `INPUT_SOURCE` | str | `'auto'` | 数据库源 |
| `DEFAULT_RETURN_FORMAT` | str | `'file'` | 输出格式 |

### 使用建议

1. **从简单开始**: 先使用默认设置，然后根据需要调整
2. **增加迭代次数**: 使用 `SCALING_ITERATIONS: 2-3` 获得更好的优化
3. **控制节点**: 设置 `USER_SPECIFIED_NODE_ASSIGNMENT: True` 以精确控制
4. **可重现性**: 始终设置 `RANDOM_SEED` 以获得可重现的结果
5. **单元格大小**: 如果单元格塌陷，调整 `MIN_CELL_LENGTH`

### 常见问题

**问：如何只使用我指定的节点？**  
答：设置 `USER_SPECIFIED_NODE_ASSIGNMENT: True`

**问：如何提高单元格优化质量？**  
答：增加 `SCALING_ITERATIONS` 的值（如 2-5）

**问：如何确保每次生成相同的电荷？**  
答：设置固定的 `RANDOM_SEED` 值

**问：如何禁用电荷分配？**  
答：设置 `CHARGES: False`

---

## See Also / 另见

- Main README: `README.md`
- API Documentation: `docs/API_DOCUMENTATION.md`
- Installation Guide: `docs/INSTALLATION.md`
- Migration Guide: `docs/MIGRATION_GUIDE.md`
- Examples: `examples/README.md`

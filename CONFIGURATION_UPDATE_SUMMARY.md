# Configuration Options Update Summary

## 概述 (Overview)

本次更新为 `generate_cif()` API 函数添加了配置选项的文档和示例，特别是 `USER_SPECIFIED_NODE_ASSIGNMENT` 和 `SCALING_ITERATIONS` 参数。

This update adds documentation and examples for configuration options in the `generate_cif()` API function, especially `USER_SPECIFIED_NODE_ASSIGNMENT` and `SCALING_ITERATIONS` parameters.

## 更新内容 (Changes Made)

### 1. 更新的文件 (Updated Files)

#### `examples/quick_start.py`
- 添加了配置选项示例
- 展示如何使用 `USER_SPECIFIED_NODE_ASSIGNMENT` 和 `SCALING_ITERATIONS`
- 包含其他常用配置选项的注释

#### `examples/README.md`
- 添加了配置选项部分
- 更新了示例 7，包含更多配置选项
- 添加了对 `advanced_config_example.py` 的引用

### 2. 新建的文件 (New Files)

#### `examples/advanced_config_example.py`
综合的配置选项演示脚本，包含 5 个示例：
1. 默认配置
2. 自定义缩放迭代次数
3. 用户指定节点分配
4. 组合配置选项
5. 自定义电荷和原子设置

#### `examples/CONFIG_OPTIONS.md`
详细的配置选项指南，包括：
- 所有主要配置选项的说明
- 使用场景和示例代码
- 完整的配置示例
- 参数说明和默认值

#### `CONFIGURATION_OPTIONS_SUMMARY.md`
快速参考文档，包括：
- 最重要的配置选项
- 快速示例
- 使用建议
- 配置方式对比

#### `配置选项说明.md`
中文配置选项说明文档，包括：
- 主要配置选项的中文说明
- 使用场景和示例
- 常见问题解答
- 完整示例代码

#### `test_config_options.py`
配置选项测试脚本，测试：
- `USER_SPECIFIED_NODE_ASSIGNMENT` 选项
- `SCALING_ITERATIONS` 选项
- 组合配置选项

## 主要配置选项 (Key Configuration Options)

### USER_SPECIFIED_NODE_ASSIGNMENT (bool)
- **默认值 (Default):** `False` (全局), `True` (API 模式)
- **功能 (Function):** 控制在顶点分配时考虑哪些节点
- **用法 (Usage):**
  ```python
  config = {'USER_SPECIFIED_NODE_ASSIGNMENT': True}
  result = generate_cif(..., config=config)
  ```

### SCALING_ITERATIONS (int)
- **默认值 (Default):** `1`
- **功能 (Function):** 单元格优化的迭代次数
- **用法 (Usage):**
  ```python
  config = {'SCALING_ITERATIONS': 3}
  result = generate_cif(..., config=config)
  ```

## 使用示例 (Usage Examples)

### 基本用法 (Basic Usage)

```python
from src.api import generate_cif

config = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': False,
    'SCALING_ITERATIONS': 1,
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config
)
```

### 高级用法 (Advanced Usage)

```python
from src.api import generate_cif

config = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': True,
    'SCALING_ITERATIONS': 3,
    'CHARGES': True,
    'REMOVE_DUMMY_ATOMS': True,
    'MIN_CELL_LENGTH': 10.0,
    'RANDOM_SEED': 42
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config
)
```

## 运行示例 (Running Examples)

```bash
# 快速开始示例 (Quick start example)
python examples/quick_start.py

# 高级配置示例 (Advanced configuration example)
python examples/advanced_config_example.py

# 测试配置选项 (Test configuration options)
python test_config_options.py
```

## 文档结构 (Documentation Structure)

```
.
├── examples/
│   ├── quick_start.py                    # 基本示例（已更新）
│   ├── advanced_config_example.py        # 高级配置示例（新建）
│   ├── CONFIG_OPTIONS.md                 # 配置选项详细文档（新建）
│   └── README.md                         # 示例说明（已更新）
├── CONFIGURATION_OPTIONS_SUMMARY.md      # 配置选项快速参考（新建）
├── 配置选项说明.md                        # 中文配置说明（新建）
├── test_config_options.py                # 配置选项测试（新建）
└── configuration.py                      # 全局配置文件（已存在）
```

## 其他可用配置选项 (Other Available Options)

除了 `USER_SPECIFIED_NODE_ASSIGNMENT` 和 `SCALING_ITERATIONS`，还有许多其他配置选项：

- `CHARGES` - 启用/禁用电荷分配
- `RANDOM_SEED` - 确定性电荷生成的种子
- `MIN_CELL_LENGTH` - 最小单元格长度
- `REMOVE_DUMMY_ATOMS` - 移除虚拟原子
- `CONNECTION_SITE_BOND_LENGTH` - 连接位点键长
- `BOND_TOL` - 键容差
- `OPT_METHOD` - 优化方法
- `FIX_UC` - 固定单元格参数
- `PRE_SCALE` - 预缩放因子
- `SINGLE_METAL_MOFS_ONLY` - 仅单金属 MOF
- `MOFS_ONLY` - 仅 MOF（不包括 COF）
- `COMBINATORIAL_EDGE_ASSIGNMENT` - 组合边分配

完整列表请参见 `configuration.py` 文件。

## 参考文档 (Reference Documentation)

- `configuration.py` - 所有配置选项及默认值
- `examples/CONFIG_OPTIONS.md` - 详细配置文档
- `CONFIGURATION_OPTIONS_SUMMARY.md` - 快速参考
- `配置选项说明.md` - 中文说明
- `examples/README.md` - 示例说明
- `CONFIGURATION_GUIDE.md` - 全局配置指南

## 总结 (Summary)

本次更新提供了：
1. ✅ 配置选项的完整文档
2. ✅ 实用的代码示例
3. ✅ 测试脚本
4. ✅ 中英文文档
5. ✅ 快速参考指南

用户现在可以轻松地：
- 了解所有可用的配置选项
- 通过示例学习如何使用
- 测试配置选项是否正常工作
- 根据需要自定义 MOF 生成过程

This update provides:
1. ✅ Complete documentation for configuration options
2. ✅ Practical code examples
3. ✅ Test scripts
4. ✅ Documentation in both English and Chinese
5. ✅ Quick reference guide

Users can now easily:
- Understand all available configuration options
- Learn how to use them through examples
- Test if configuration options work correctly
- Customize the MOF generation process as needed

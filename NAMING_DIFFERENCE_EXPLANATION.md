# CIF 文件命名差异说明 / CIF Filename Naming Difference Explanation

## 问题 / Question
为什么相同的输入，直接运行 `tobacco.py` 和运行 `multiple_input_example.py` (使用API) 得到的结果命名不一样？

Why do the same inputs produce different filenames when running `tobacco.py` directly versus using the API in `multiple_input_example.py`?

---

## 命名格式对比 / Naming Format Comparison

### tobacco.py 命名格式
```
{template}_{vnames}_{enames}{bond_check_code}.cif
```

**示例 / Example:**
```
pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif
```

### API (src/api.py) 命名格式
```
{template}_{vnames}_{enames}{bond_check_code}.cif
```

**示例 / Example:**
```
pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif
```

### 关键差异 / Key Difference
- **tobacco.py**: 使用 `v1`, `v2`, `v3` 等（小写v + 数字）
- **API**: 使用 `V`, `Er`, `Ti` 等（原始顶点类型名称）

---

## 详细分析 / Detailed Analysis

### tobacco.py 中的命名逻辑

#### 第1步：创建 v_set（带数字编号）
```python
# tobacco.py 第186行
v_set = [('v' + str(vname_dict[re.sub('[0-9]','',i[0])]), i[1]) for i in va]
v_set = sorted(list(set(v_set)), key=lambda x: x[0])
v_set = [v[0] + '-' + v[1] for v in v_set]
```

**vname_dict 映射表:**
```python
vname_dict = {'V':1, 'Er':2, 'Ti':3, 'Ce':4, 'S':5, ...}
```

**处理过程:**
1. 顶点类型 `'V'` → 查找 `vname_dict['V']` → 得到 `1`
2. 生成 `'v' + str(1)` → `'v1'`
3. 组合节点名称 → `'v1-4c_Cd_1_Ch'`

#### 第2步：生成文件名（使用 v_set）
```python
# tobacco.py 第354行
vnames = '_'.join([v.split('.')[0] for v in v_set])
# v_set = ['v1-4c_Cd_1_Ch']
# vnames = 'v1-4c_Cd_1_Ch'
```

**最终文件名:**
```
pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif
     ^^^ 小写v + 数字
```

---

### API (src/api.py) 中的命名逻辑

#### 第1步：创建 v_set（保留原始顶点类型）
```python
# src/api.py 第635行
v_set = [(re.sub('[0-9]','', i[0]), i[1]) for i in va]
v_set = sorted(list(set(v_set)), key=lambda x: x[0])
vnames = '_'.join([v[0] + '-' + v[1].replace('.cif', '') for v in v_set])
```

**处理过程:**
1. 顶点类型 `'V'` → 移除数字 → 保持 `'V'`
2. 直接使用原始顶点类型 → `'V'`
3. 组合节点名称 → `'V-4c_Cd_1_Ch'`

#### 第2步：生成文件名（使用原始顶点类型）
```python
# src/api.py 第644行
cifname = template_filename.replace('.cif', '') + '_' + vnames + '_' + enames + bond_check_code + '.cif'
# vnames = 'V-4c_Cd_1_Ch'
```

**最终文件名:**
```
pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif
    ^^^ 大写V（原始顶点类型）
```

---

## 代码对比 / Code Comparison

### tobacco.py
```python
# 使用 vname_dict 将顶点类型转换为数字
v_set = [('v' + str(vname_dict[re.sub('[0-9]','',i[0])]), i[1]) for i in va]
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#         将 'V' 转换为 'v1'

# 后续使用 v_set 生成文件名
vnames = '_'.join([v.split('.')[0] for v in v_set])
```

### src/api.py
```python
# 直接使用原始顶点类型（移除数字后）
v_set = [(re.sub('[0-9]','', i[0]), i[1]) for i in va]
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^
#         保持 'V' 不变

# 直接使用原始顶点类型生成文件名
vnames = '_'.join([v[0] + '-' + v[1].replace('.cif', '') for v in v_set])
```

---

## 命名示例对比 / Naming Examples Comparison

### 示例 1: pcb + 4c_Cd_1_Ch + 1B_2CF3_Ch

| 方法 / Method | 文件名 / Filename |
|--------------|------------------|
| tobacco.py | `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif` |
| API | `pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif` |

**差异**: `v1` vs `V`

### 示例 2: pcu + 6c_Al_1 + 2B_2Br_Ch

| 方法 / Method | 文件名 / Filename |
|--------------|------------------|
| tobacco.py | `pcu_v1-6c_Al_1_1-2B_2Br_Ch.cif` |
| API | `pcu_V-6c_Al_1_1-2B_2Br_Ch.cif` |

**差异**: `v1` vs `V`

### 示例 3: 多顶点类型模板（假设）

假设模板有两种顶点类型 `V` 和 `Er`:

| 方法 / Method | 文件名 / Filename |
|--------------|------------------|
| tobacco.py | `template_v1-node1_v2-node2_...` |
| API | `template_Er-node1_V-node2_...` |

**差异**: `v1`, `v2` vs `Er`, `V`

---

## 为什么会有这个差异？/ Why This Difference?

### 历史原因 / Historical Reason

**tobacco.py (原始实现)**
- 使用数字编号 (`v1`, `v2`, `v3`) 是为了简化文件名
- 避免使用特殊字符或复杂的顶点类型名称
- 保持文件名简短和一致

**API (重构版本)**
- 保留原始顶点类型名称 (`V`, `Er`, `Ti`) 更具描述性
- 更容易理解文件名对应的拓扑结构
- 与模板文件中的顶点类型名称保持一致

### 设计考虑 / Design Considerations

#### tobacco.py 的优点
✅ 文件名更短  
✅ 避免特殊字符  
✅ 数字编号简单明了  

#### API 的优点
✅ 更具描述性  
✅ 与模板文件一致  
✅ 更容易追溯到原始拓扑  
✅ 不需要查找 vname_dict 映射表  

---

## 实际影响 / Practical Impact

### 对用户的影响 / Impact on Users

#### 1. 文件名不同但内容相同
```bash
# tobacco.py 生成
pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif

# API 生成
pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif

# 两个文件的结构内容完全相同！
# The structure content is identical!
```

#### 2. 批处理脚本需要注意
如果你的脚本依赖特定的文件名格式，需要相应调整：

```python
# 旧脚本（假设使用 v1 格式）
files = glob.glob("*_v1-*.cif")

# 新脚本（兼容两种格式）
files = glob.glob("*_v1-*.cif") + glob.glob("*_V-*.cif")
```

#### 3. 文件管理
- 两种方法生成的文件可以共存
- 不会相互覆盖（文件名不同）
- 建议统一使用一种方法以保持一致性

---

## 如何统一命名？/ How to Unify Naming?

### 选项 1: 修改 API 使用数字编号

在 `src/api.py` 中添加 vname_dict 映射：

```python
# 在 src/api.py 顶部添加
vname_dict = {'V':1,'Er':2,'Ti':3,'Ce':4,'S':5,
              'H':6,'He':7,'Li':8,'Be':9,'B':10,
              'C':11,'N':12,'O':13,'F':14,'Ne':15,
              'Na':16,'Mg':17,'Al':18,'Si':19,'P':20,
              'Cl':21,'Ar':22,'K':23,'Ca':24,'Sc':24,
              'Cr':26,'Mn':27,'Fe':28,'Co':29,'Ni':30}

# 修改第635行
v_set = [('v' + str(vname_dict[re.sub('[0-9]','',i[0])]), i[1]) for i in va]
v_set = sorted(list(set(v_set)), key=lambda x: x[0])
v_set = [v[0] + '-' + v[1] for v in v_set]

# 修改第637行
vnames = '_'.join([v.split('.')[0] for v in v_set])
```

### 选项 2: 修改 tobacco.py 使用原始顶点类型

在 `tobacco.py` 中移除 vname_dict 映射：

```python
# 修改第186行
v_set = [(re.sub('[0-9]','', i[0]), i[1]) for i in va]
v_set = sorted(list(set(v_set)), key=lambda x: x[0])
vnames = '_'.join([v[0] + '-' + v[1].replace('.cif', '') for v in v_set])

# 修改第354行（直接使用 vnames，不需要额外处理）
# vnames 已经是正确格式
```

### 推荐方案 / Recommendation

**推荐使用 API 的命名方式（保留原始顶点类型）**

理由：
1. ✅ 更具描述性和可读性
2. ✅ 与模板文件保持一致
3. ✅ 不需要维护额外的映射表
4. ✅ 更容易理解和调试
5. ✅ 符合现代软件设计原则

---

## 总结 / Summary

### 命名差异的根本原因
- **tobacco.py**: 使用 `vname_dict` 将顶点类型转换为数字编号 (`v1`, `v2`, ...)
- **API**: 直接使用原始顶点类型名称 (`V`, `Er`, `Ti`, ...)

### 两种命名方式的对比

| 特性 / Feature | tobacco.py | API |
|---------------|------------|-----|
| 顶点表示 | `v1`, `v2`, `v3` | `V`, `Er`, `Ti` |
| 文件名长度 | 较短 | 稍长 |
| 可读性 | 需要查映射表 | 直观易懂 |
| 与模板一致性 | 不一致 | 一致 |
| 维护成本 | 需要维护映射表 | 无需额外维护 |

### 实际建议 / Practical Advice

1. **对于新项目**: 使用 API 方法（保留原始顶点类型）
2. **对于现有项目**: 保持当前方法以避免混淆
3. **批处理脚本**: 使用通配符兼容两种格式
4. **文档说明**: 在文档中明确说明使用的命名方式

### 重要提示 / Important Note

⚠️ **文件名不同，但结构内容完全相同！**

两种方法生成的 MOF 结构在原子坐标、键连接、单元格参数等方面完全一致，只是文件名的命名约定不同。

The filenames are different, but the structure content is identical! Both methods generate MOF structures with the same atomic coordinates, bond connectivity, and unit cell parameters - only the filename convention differs.

---

## 相关文件 / Related Files

- `tobacco.py` - 原始命令行接口（使用数字编号）
- `src/api.py` - API接口（使用原始顶点类型）
- `examples/multiple_input_example.py` - API使用示例

---

**文档创建日期 / Document Created:** 2024年12月28日 / December 28, 2024  
**ToBaCCo 版本 / Version:** 3.0

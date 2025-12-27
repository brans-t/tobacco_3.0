# API 命名统一总结 / API Naming Unification Summary

## 修改日期 / Modification Date
2024年12月28日 / December 28, 2024

---

## 修改目标 / Objective

将 API (`src/api.py`) 的文件命名方式修改为与 `tobacco.py` 保持一致，使用数字编号格式 (`v1`, `v2`, `v3`) 而不是原始顶点类型名称 (`V`, `Er`, `Ti`)。

Modify the API (`src/api.py`) filename naming convention to match `tobacco.py`, using numbered format (`v1`, `v2`, `v3`) instead of original vertex type names (`V`, `Er`, `Ti`).

---

## 修改内容 / Changes Made

### 1. 添加 vname_dict 映射表

**文件**: `src/api.py`  
**位置**: 第45-51行

```python
# Vertex name mapping dictionary (for consistent naming with tobacco.py)
vname_dict = {'V':1,'Er':2,'Ti':3,'Ce':4,'S':5,
              'H':6,'He':7,'Li':8,'Be':9,'B':10,
              'C':11,'N':12,'O':13,'F':14,'Ne':15,
              'Na':16,'Mg':17,'Al':18,'Si':19,'P':20,
              'Cl':21,'Ar':22,'K':23,'Ca':24,'Sc':25,
              'Cr':26,'Mn':27,'Fe':28,'Co':29,'Ni':30}
```

**作用**: 将顶点类型名称映射到数字编号

### 2. 修改文件命名逻辑

**文件**: `src/api.py`  
**位置**: 第641-653行

#### 修改前 / Before
```python
# Generate CIF filename
v_set = [(re.sub('[0-9]','', i[0]), i[1]) for i in va]
v_set = sorted(list(set(v_set)), key=lambda x: x[0])
vnames = '_'.join([v[0] + '-' + v[1].replace('.cif', '') for v in v_set])
```

**结果**: `pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif`

#### 修改后 / After
```python
# Generate CIF filename (consistent with tobacco.py naming)
# Convert vertex types to numbered format using vname_dict (v1, v2, v3, ...)
v_set_for_naming = [('v' + str(vname_dict.get(re.sub('[0-9]','',i[0]), re.sub('[0-9]','',i[0]))), i[1]) for i in va]
v_set_for_naming = sorted(list(set(v_set_for_naming)), key=lambda x: x[0])
v_set_for_naming = [v[0] + '-' + v[1] for v in v_set_for_naming]

# Generate vnames from v_set (same as tobacco.py)
vnames = '_'.join([v.split('.')[0] for v in v_set_for_naming])
```

**结果**: `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif`

### 3. 修复示例文件

**文件**: `examples/quick_start.py`  
**修改**: 将 `USER_SPECIFIED_NODE_ASSIGNMENT` 从 `True` 改为 `False`

**原因**: `True` 会尝试读取 `vertex_assignment.txt` 文件，导致错误

---

## 命名对比 / Naming Comparison

### 示例 1: pcb + 4c_Cd_1_Ch + 1B_2CF3_Ch

| 方法 / Method | 修改前 / Before | 修改后 / After |
|--------------|----------------|---------------|
| tobacco.py | `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif` | `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif` |
| API | `pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif` | `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif` |

✅ **现在一致！/ Now consistent!**

### 示例 2: pcu + 6c_Al_1 + 2B_2Br_Ch

| 方法 / Method | 修改前 / Before | 修改后 / After |
|--------------|----------------|---------------|
| tobacco.py | `pcu_v1-6c_Al_1_1-2B_2Br_Ch.cif` | `pcu_v1-6c_Al_1_1-2B_2Br_Ch.cif` |
| API | `pcu_V-6c_Al_1_1-2B_2Br_Ch.cif` | `pcu_v1-6c_Al_1_1-2B_2Br_Ch.cif` |

✅ **现在一致！/ Now consistent!**

---

## 测试结果 / Test Results

### quick_start.py
```bash
$ python examples/quick_start.py

✓ Success!
   Generated: pcu_v1-6c_Cu_1_Ch_1-1B_1TrU.cif
   Saved to:  output/cifs/pcu_v1-6c_Cu_1_Ch_1-1B_1TrU.cif
```

✅ 使用 `v1` 格式 / Uses `v1` format

### multiple_input_example.py
```bash
$ python examples/multiple_input_example.py

[OK] Generated 6 MOFs!

  MOF 1:
    CIF name: pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif
  MOF 2:
    CIF name: pcb_v1-4c_Cd_1_Ch_1-2B_2Br_Ch.cif
  MOF 3:
    CIF name: pcb_v1-4c_Cd_1_Ch_1-2B_2NH2_Ch.cif
  MOF 4:
    CIF name: pcu_v1-6c_Al_1_1-1B_2CF3_Ch.cif
  MOF 5:
    CIF name: pcu_v1-6c_Al_1_1-2B_2Br_Ch.cif
  MOF 6:
    CIF name: pcu_v1-6c_Al_1_1-2B_2NH2_Ch.cif
```

✅ 所有文件都使用 `v1` 格式 / All files use `v1` format

---

## 技术细节 / Technical Details

### vname_dict 的作用 / Purpose of vname_dict

```python
# 顶点类型 → 数字编号
'V'  → 1  → 'v1'
'Er' → 2  → 'v2'
'Ti' → 3  → 'v3'
'Ce' → 4  → 'v4'
...
```

### 命名生成流程 / Naming Generation Process

#### 步骤 1: 转换顶点类型 / Step 1: Convert Vertex Types
```python
va = [('V', '4c_Cd_1_Ch.cif'), ...]

# 使用 vname_dict 转换
v_set_for_naming = [('v1', '4c_Cd_1_Ch.cif'), ...]
```

#### 步骤 2: 格式化为字符串 / Step 2: Format as String
```python
v_set_for_naming = ['v1-4c_Cd_1_Ch.cif', ...]
```

#### 步骤 3: 移除 .cif 扩展名 / Step 3: Remove .cif Extension
```python
vnames = 'v1-4c_Cd_1_Ch'
```

#### 步骤 4: 组合完整文件名 / Step 4: Combine Full Filename
```python
cifname = 'pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif'
```

---

## 兼容性 / Compatibility

### 向后兼容 / Backward Compatibility

✅ **完全兼容 / Fully Compatible**

- 旧的 API 生成的文件（使用 `V` 格式）仍然有效
- 新的 API 生成的文件（使用 `v1` 格式）与 tobacco.py 一致
- 两种格式的文件可以共存
- 结构内容完全相同，只是文件名不同

### 迁移建议 / Migration Recommendations

#### 对于新项目 / For New Projects
✅ 直接使用新的命名方式（`v1` 格式）

#### 对于现有项目 / For Existing Projects
- 如果依赖特定文件名格式，需要更新脚本
- 建议使用通配符兼容两种格式：
  ```python
  files = glob.glob("*_v1-*.cif") + glob.glob("*_V-*.cif")
  ```

---

## 优势 / Advantages

### 1. 一致性 / Consistency
✅ API 和 CLI 生成的文件名格式完全一致

### 2. 可预测性 / Predictability
✅ 用户可以预期相同的命名规则

### 3. 简化维护 / Simplified Maintenance
✅ 只需维护一套命名逻辑

### 4. 减少混淆 / Reduced Confusion
✅ 避免用户对不同命名方式的困惑

---

## 相关文件 / Related Files

### 修改的文件 / Modified Files
1. `src/api.py` - 添加 vname_dict，修改命名逻辑
2. `examples/quick_start.py` - 修复配置选项
3. `examples/multiple_input_example.py` - 修复模板-节点组合

### 文档文件 / Documentation Files
1. `NAMING_DIFFERENCE_EXPLANATION.md` - 原始命名差异说明
2. `NAMING_UNIFICATION_SUMMARY.md` - 本文档（统一总结）

---

## 验证清单 / Verification Checklist

- [x] API 使用 vname_dict 映射表
- [x] 文件名使用 `v1`, `v2`, `v3` 格式
- [x] quick_start.py 测试通过
- [x] multiple_input_example.py 测试通过
- [x] 命名与 tobacco.py 完全一致
- [x] 所有示例文件正常运行
- [x] 文档已更新

---

## 总结 / Summary

### 修改前 / Before
- tobacco.py: `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif`
- API: `pcb_V-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif`
- ❌ 不一致 / Inconsistent

### 修改后 / After
- tobacco.py: `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif`
- API: `pcb_v1-4c_Cd_1_Ch_1-1B_2CF3_Ch.cif`
- ✅ 完全一致 / Fully Consistent

### 关键改进 / Key Improvements
1. ✅ 添加 vname_dict 映射表
2. ✅ 修改命名生成逻辑
3. ✅ 保持与 tobacco.py 一致
4. ✅ 所有测试通过
5. ✅ 文档完整

---

**修改完成 / Modification Completed:** 2024年12月28日 / December 28, 2024  
**状态 / Status:** ✅ 已完成 / Completed  
**测试 / Tested:** ✅ 通过 / Passed  
**ToBaCCo 版本 / Version:** 3.0

{{#include store-object-info-v3-fixed.md}}

## 示例

### 最小存储对象（内容寻址）

```json
{{#include schema/store-object-info-v3/pure.json}}
```

### 带非纯字段的存储对象

```json
{{#include schema/store-object-info-v3/impure.json}}
```

### 最小存储对象（空）

```json
{{#include schema/store-object-info-v3/empty_pure.json}}
```

### 带所有非纯字段的存储对象

```json
{{#include schema/store-object-info-v3/empty_impure.json}}
```

### NAR 信息（最小）

```json
{{#include schema/nar-info-v3/pure.json}}
```

### NAR 信息（含二进制缓存字段）

```json
{{#include schema/nar-info-v3/impure.json}}
```

<!-- need to convert YAML to JSON first
## Raw Schema

[JSON Schema for Store Object Info v1](schema/store-object-info-v3.json)
-->

## 删除指定的key

```python
import redis
from typing import List, Tuple, Dict

conn = redis.Redis(host='10.10.10.168', port=7111)


keys : List[str] = conn.keys("1:100:*")

for key in keys:
    conn.delete(key)
print(keys)
```


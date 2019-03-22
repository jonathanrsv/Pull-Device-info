# Pull-Device-info
Script para extrair informações técnicas de smartphones com base no nome do modelo. 

## Usage

Defina uma lista de dispositivos no formato CSV com o nome do modelo, exemplo:


*devices_list.csv* 
---
| 	|
| --------------|
| SM-G610M     	|
| SM-G570M     	|
| iPhone 6S    	|
| Moto G       	|
| Moto Z2 Play 	|

---

```python
from pull_device_info import pull_device_info

pull_device_info("devices_list.csv", "output_file.csv")

```


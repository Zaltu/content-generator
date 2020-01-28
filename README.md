# Genesis
Generate various kinds of content (generally text) based on parameters. AIGIS plugin.

Very important to note that due to the way the Faker module was developped, this entire module is inherently __not__ thread-safe.

### Quicktsart
```python
from genesis import Genesis
g = Genesis()
print(g.name())
```

# Dual Modes
Genesis has two levels of functionality, normal and *hardcore*.  
Harcore involves AI text generation, which has significantly higher requirements than normal. For this reason, there are two different sets of requirements.

Genesis objects are created in normal mode by default. To begin in hardcore more, use instead:
```python
from genesis import Genesis
g = Genesis(include_ai=True)
```


# Requirements
Normal:
- __*python3.7*__
    - Faker

Hardcore:
- __*python3.7*__
    - torch==1.4.0
    - transformers==2.3.0
    - Faker
- Linux (tested on Ubuntu 1.19.1 and CentOS 7.4)
- \>15GB free hard drive space
- __*32GB RAM*__


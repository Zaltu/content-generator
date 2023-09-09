# Genesis
Generate various kinds of content (generally text) based on parameters. AIGIS plugin.

### Quicktsart
```python
from genesis import Genesis
g = Genesis()
print(g.name())
```

# Dual Modes
Genesis has two levels of functionality, normal and *hardcore*.  
Harcore involves AI text generation, which requires manual installation and management of [alpaca.cpp](https://github.com/antimatter15/alpaca.cpp). For this reason, there are two different sets of requirements.

Genesis objects are created in normal mode by default. To begin in hardcore mode, use instead:
```python
from genesis import Genesis
g = Genesis(include_ai=True)
```


# Requirements
Normal:
- __*python>=3.7*__
    - Faker
    - lorem

Hardcore:
- __*python3.10*__
    - Faker
    - lorem
- Linux (tested on Ubuntu 22.04)
- Compiled "`chat`" from [alpaca.cpp](https://github.com/antimatter15/alpaca.cpp), renamed/symlinked to `alpaca-chat` (and a model binary) slapped in the `genesis` folder.



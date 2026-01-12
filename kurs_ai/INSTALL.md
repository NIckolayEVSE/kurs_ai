# Установка необходимых библиотек

## Проблема: ModuleNotFoundError

Если вы получили ошибку `ModuleNotFoundError: No module named 'seaborn'` или другие подобные ошибки, нужно установить необходимые библиотеки.

## Способ 1: Установка через requirements.txt (рекомендуется)

```bash
pip install -r requirements.txt
```

или

```bash
pip3 install -r requirements.txt
```

## Способ 2: Установка всех библиотек одной командой

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

или

```bash
pip3 install pandas numpy matplotlib seaborn scikit-learn
```

## Способ 3: Установка по отдельности

Если возникают проблемы, установите библиотеки по одной:

```bash
pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn
pip install scikit-learn
```

## Опциональные библиотеки

Для полной функциональности notebook (CatBoost и нейронные сети) установите:

```bash
pip install catboost
pip install tensorflow
```

**Примечание:** Эти библиотеки опциональны. Notebook будет работать без них, просто пропустит соответствующие модели.

## Проверка установки

После установки проверьте, что все библиотеки установлены:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import __version__ as sklearn_version

print("✓ Все библиотеки установлены успешно!")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Scikit-learn: {sklearn_version}")
```

## Если используете conda

```bash
conda install pandas numpy matplotlib seaborn scikit-learn
```

## Если используете Jupyter в виртуальном окружении

1. Активируйте виртуальное окружение:
   ```bash
   source venv/bin/activate  # для Linux/Mac
   # или
   venv\Scripts\activate  # для Windows
   ```

2. Установите библиотеки:
   ```bash
   pip install -r requirements.txt
   ```

3. Убедитесь, что Jupyter использует правильное окружение:
   ```bash
   python -m ipykernel install --user --name=your_env_name
   ```

## Решение проблем

### Проблема: Permission denied
Используйте `--user` флаг:
```bash
pip install --user pandas numpy matplotlib seaborn scikit-learn
```

### Проблема: pip не найден
Установите pip:
```bash
python -m ensurepip --upgrade
```

### Проблема: Устаревший pip
Обновите pip:
```bash
pip install --upgrade pip
```

## После установки

После установки всех библиотек:
1. Перезапустите Jupyter kernel (Kernel → Restart)
2. Выполните ячейку с импортами заново
3. Продолжайте выполнение notebook


#!/usr/bin/env python3
"""
Автоматическая проверка Jupyter notebook
Проверяет синтаксис, структуру, зависимости и готовность к выполнению
"""
import json
import sys
import os
import re
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{'='*80}{Colors.END}\n")

def check_notebook_structure(notebook_path):
    """Проверка структуры notebook"""
    print_header("1. ПРОВЕРКА СТРУКТУРЫ NOTEBOOK")
    
    if not os.path.exists(notebook_path):
        print_error(f"Файл {notebook_path} не найден!")
        return None
    
    print_success(f"Файл найден: {notebook_path}")
    file_size = os.path.getsize(notebook_path) / 1024
    print_info(f"Размер файла: {file_size:.2f} KB")
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print_error(f"Неверный JSON формат: {e}")
        return None
    except Exception as e:
        print_error(f"Ошибка при чтении файла: {e}")
        return None
    
    print_success("JSON формат корректен")
    
    if 'cells' not in nb:
        print_error("Отсутствует ключ 'cells'")
        return None
    
    cells = nb['cells']
    code_cells = [c for c in cells if c.get('cell_type') == 'code']
    markdown_cells = [c for c in cells if c.get('cell_type') == 'markdown']
    
    print_success(f"Найдено ячеек: {len(cells)}")
    print_info(f"  - Код: {len(code_cells)}")
    print_info(f"  - Markdown: {len(markdown_cells)}")
    
    return nb

def check_python_syntax(nb):
    """Проверка синтаксиса Python"""
    print_header("2. ПРОВЕРКА СИНТАКСИСА PYTHON")
    
    cells = nb['cells']
    syntax_errors = []
    total_code_lines = 0
    
    for i, cell in enumerate(cells):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            if source.strip():
                total_code_lines += len(source.split('\n'))
                try:
                    compile(source, f'<cell {i}>', 'exec')
                except SyntaxError as e:
                    syntax_errors.append((i, e))
                except Exception as e:
                    # Игнорируем другие ошибки (например, импорты)
                    pass
    
    print_info(f"Всего строк кода: {total_code_lines}")
    
    if syntax_errors:
        print_error(f"Найдено синтаксических ошибок: {len(syntax_errors)}")
        for cell_num, error in syntax_errors[:5]:
            print_error(f"  Ячейка {cell_num}: {error.msg} (строка {error.lineno})")
        return False
    else:
        print_success("Синтаксис Python корректен")
        return True

def check_imports_and_dependencies(nb):
    """Проверка импортов и зависимостей"""
    print_header("3. ПРОВЕРКА ИМПОРТОВ И ЗАВИСИМОСТЕЙ")
    
    all_code = ' '.join([
        ''.join(cell.get('source', []))
        for cell in nb['cells']
        if cell.get('cell_type') == 'code'
    ])
    
    # Извлекаем все импорты
    import_pattern = r'(?:from|import)\s+([\w.]+)'
    imports = set(re.findall(import_pattern, all_code))
    
    print_info(f"Найдено импортов: {len(imports)}")
    
    # Ключевые библиотеки
    required_libs = {
        'pandas': 'pd',
        'numpy': 'np',
        'matplotlib': 'plt',
        'seaborn': 'sns',
        'sklearn': 'scikit-learn',
    }
    
    optional_libs = {
        'catboost': 'CatBoost',
        'tensorflow': 'TensorFlow',
    }
    
    print("\nОбязательные библиотеки:")
    for lib, pip_name in required_libs.items():
        if lib in imports or any(lib in imp for imp in imports):
            # Проверяем, установлена ли библиотека
            try:
                __import__(lib)
                print_success(f"  {lib} ({pip_name}) - установлена")
            except ImportError:
                print_error(f"  {lib} ({pip_name}) - НЕ установлена")
                print_info(f"    Установите: pip install {pip_name}")
    
    print("\nОпциональные библиотеки:")
    for lib, pip_name in optional_libs.items():
        if lib in imports or any(lib in imp for imp in imports):
            try:
                __import__(lib)
                print_success(f"  {lib} ({pip_name}) - установлена")
            except ImportError:
                print_warning(f"  {lib} ({pip_name}) - не установлена (опционально)")
                print_info(f"    Установите: pip install {pip_name}")

def check_key_elements(nb):
    """Проверка наличия ключевых элементов"""
    print_header("4. ПРОВЕРКА КЛЮЧЕВЫХ ЭЛЕМЕНТОВ")
    
    all_code = ' '.join([
        ''.join(cell.get('source', []))
        for cell in nb['cells']
        if cell.get('cell_type') == 'code'
    ])
    
    checks = {
        'Загрузка данных (read_csv)': 'read_csv' in all_code,
        'Анализ данных (.info, .describe)': '.info()' in all_code and '.describe()' in all_code,
        'Обработка пропусков': 'isnull' in all_code or 'fillna' in all_code,
        'Регулярные выражения': 'import re' in all_code or 're.' in all_code,
        'Кодирование (LabelEncoder)': 'LabelEncoder' in all_code,
        'Кодирование (OneHotEncoder)': 'OneHotEncoder' in all_code,
        'Визуализация (matplotlib/seaborn)': 'plt.' in all_code or 'sns.' in all_code,
        'Отбор признаков': 'VarianceThreshold' in all_code or 'SelectKBest' in all_code or 'RFE' in all_code,
        'Разбиение данных (train_test_split)': 'train_test_split' in all_code,
        'Нормализация (StandardScaler)': 'StandardScaler' in all_code,
        'KNN модель': 'KNeighborsClassifier' in all_code,
        'Дерево решений': 'DecisionTreeClassifier' in all_code,
        'Случайный лес': 'RandomForestClassifier' in all_code,
        'CatBoost': 'CatBoostClassifier' in all_code,
        'Нейронные сети': 'keras' in all_code or 'tensorflow' in all_code,
        'Подбор параметров (GridSearchCV)': 'GridSearchCV' in all_code,
        'Метрики оценки': 'accuracy_score' in all_code and 'f1_score' in all_code,
        'Прогноз для новых данных': 'predict' in all_code,
    }
    
    passed = 0
    total = len(checks)
    
    for check_name, result in checks.items():
        if result:
            print_success(check_name)
            passed += 1
        else:
            print_error(check_name)
    
    print(f"\nПройдено проверок: {passed}/{total} ({passed*100//total}%)")
    return passed == total

def check_dataset_file():
    """Проверка наличия файла датасета"""
    print_header("5. ПРОВЕРКА ФАЙЛА ДАТАСЕТА")
    
    dataset_path = '/Users/nickolay/Downloads/Aircraft_Incident_Dataset.csv'
    
    if os.path.exists(dataset_path):
        size_mb = os.path.getsize(dataset_path) / (1024 * 1024)
        print_success(f"Датасет найден: {dataset_path}")
        print_info(f"Размер: {size_mb:.2f} MB")
        
        # Проверяем, что это CSV файл
        try:
            import pandas as pd
            # Пробуем прочитать первые строки
            df_sample = pd.read_csv(dataset_path, nrows=5)
            print_success(f"Файл читается корректно (pandas)")
            print_info(f"Столбцов: {len(df_sample.columns)}")
            print_info(f"Первые строки загружены успешно")
        except Exception as e:
            print_warning(f"Не удалось прочитать файл pandas: {e}")
        
        return True
    else:
        print_error(f"Датасет не найден: {dataset_path}")
        print_info("Убедитесь, что файл находится по указанному пути")
        return False

def check_code_quality(nb):
    """Базовая проверка качества кода"""
    print_header("6. ПРОВЕРКА КАЧЕСТВА КОДА")
    
    all_code = '\n'.join([
        ''.join(cell.get('source', []))
        for cell in nb['cells']
        if cell.get('cell_type') == 'code'
    ])
    
    # Проверяем наличие комментариев
    code_lines = [line for line in all_code.split('\n') if line.strip()]
    comment_lines = [line for line in code_lines if line.strip().startswith('#')]
    comment_ratio = len(comment_lines) / len(code_lines) * 100 if code_lines else 0
    
    print_info(f"Строк кода: {len(code_lines)}")
    print_info(f"Строк с комментариями: {len(comment_lines)}")
    print_info(f"Процент комментариев: {comment_ratio:.1f}%")
    
    if comment_ratio > 10:
        print_success("Достаточное количество комментариев")
    else:
        print_warning("Мало комментариев в коде")
    
    # Проверяем наличие print для вывода
    if 'print(' in all_code:
        print_success("Используются print для вывода результатов")
    else:
        print_warning("Мало print statements для вывода результатов")
    
    # Проверяем обработку ошибок
    if 'try:' in all_code or 'except' in all_code:
        print_success("Используется обработка ошибок (try/except)")
    else:
        print_warning("Нет обработки ошибок")

def main():
    """Главная функция"""
    print_header("АВТОМАТИЧЕСКАЯ ПРОВЕРКА NOTEBOOK")
    
    notebook_path = 'aircraft_incident_ml.ipynb'
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    # Проверка структуры
    nb = check_notebook_structure(notebook_path)
    if nb is None:
        print_error("Не удалось загрузить notebook. Проверка прервана.")
        return 1
    
    # Проверка синтаксиса
    syntax_ok = check_python_syntax(nb)
    
    # Проверка импортов
    check_imports_and_dependencies(nb)
    
    # Проверка ключевых элементов
    elements_ok = check_key_elements(nb)
    
    # Проверка датасета
    dataset_ok = check_dataset_file()
    
    # Проверка качества кода
    check_code_quality(nb)
    
    # Итоговый отчет
    print_header("ИТОГОВЫЙ ОТЧЕТ")
    
    results = {
        'Структура notebook': True,
        'Синтаксис Python': syntax_ok,
        'Ключевые элементы': elements_ok,
        'Файл датасета': dataset_ok,
    }
    
    for check, result in results.items():
        if result:
            print_success(check)
        else:
            print_error(check)
    
    all_passed = all(results.values())
    
    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!{Colors.END}")
        print(f"{Colors.GREEN}Notebook готов к использованию.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ{Colors.END}")
        print(f"{Colors.YELLOW}Исправьте ошибки перед использованием.{Colors.END}\n")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nПроверка прервана пользователем.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


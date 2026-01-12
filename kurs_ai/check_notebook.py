#!/usr/bin/env python3
"""
Скрипт для проверки корректности Jupyter notebook
"""
import json
import sys
import os

def check_notebook(notebook_path):
    """Проверяет структуру и синтаксис notebook"""
    print("=" * 80)
    print("ПРОВЕРКА NOTEBOOK")
    print("=" * 80)
    
    # Проверка существования файла
    if not os.path.exists(notebook_path):
        print(f"❌ ОШИБКА: Файл {notebook_path} не найден!")
        return False
    
    print(f"✓ Файл найден: {notebook_path}")
    
    # Чтение notebook
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ ОШИБКА: Неверный JSON формат: {e}")
        return False
    except Exception as e:
        print(f"❌ ОШИБКА при чтении файла: {e}")
        return False
    
    print("✓ JSON формат корректен")
    
    # Проверка структуры
    if 'cells' not in nb:
        print("❌ ОШИБКА: Отсутствует ключ 'cells'")
        return False
    
    cells = nb['cells']
    print(f"✓ Найдено ячеек: {len(cells)}")
    
    # Подсчет типов ячеек
    code_cells = sum(1 for cell in cells if cell.get('cell_type') == 'code')
    markdown_cells = sum(1 for cell in cells if cell.get('cell_type') == 'markdown')
    
    print(f"  - Код: {code_cells}")
    print(f"  - Markdown: {markdown_cells}")
    
    # Проверка наличия кода
    if code_cells == 0:
        print("⚠ ПРЕДУПРЕЖДЕНИЕ: Нет ячеек с кодом!")
    
    # Проверка синтаксиса Python кода
    print("\nПроверка синтаксиса Python кода...")
    syntax_errors = []
    
    for i, cell in enumerate(cells):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            if source.strip():
                try:
                    compile(source, f'<cell {i}>', 'exec')
                except SyntaxError as e:
                    syntax_errors.append((i, e))
    
    if syntax_errors:
        print(f"❌ Найдено синтаксических ошибок: {len(syntax_errors)}")
        for cell_num, error in syntax_errors[:5]:  # Показываем первые 5
            print(f"  Ячейка {cell_num}: {error}")
        return False
    else:
        print("✓ Синтаксис Python корректен")
    
    # Проверка наличия ключевых элементов
    print("\nПроверка ключевых элементов...")
    
    all_code = ' '.join([
        ''.join(cell.get('source', []))
        for cell in cells
        if cell.get('cell_type') == 'code'
    ])
    
    checks = {
        'pandas': 'pd.' in all_code or 'import pandas' in all_code,
        'sklearn': 'sklearn' in all_code or 'from sklearn' in all_code,
        'train_test_split': 'train_test_split' in all_code,
        'загрузка данных': 'read_csv' in all_code,
        'модели': any(m in all_code for m in ['KNeighborsClassifier', 'DecisionTreeClassifier', 
                                              'RandomForestClassifier', 'CatBoostClassifier']),
    }
    
    for check_name, result in checks.items():
        status = "✓" if result else "❌"
        print(f"  {status} {check_name}")
    
    # Проверка пути к датасету
    dataset_path = '/Users/nickolay/Downloads/Aircraft_Incident_Dataset.csv'
    if os.path.exists(dataset_path):
        print(f"\n✓ Датасет найден: {dataset_path}")
        size_mb = os.path.getsize(dataset_path) / (1024 * 1024)
        print(f"  Размер: {size_mb:.2f} MB")
    else:
        print(f"\n⚠ ПРЕДУПРЕЖДЕНИЕ: Датасет не найден: {dataset_path}")
    
    print("\n" + "=" * 80)
    print("ПРОВЕРКА ЗАВЕРШЕНА")
    print("=" * 80)
    
    return len(syntax_errors) == 0

if __name__ == '__main__':
    notebook_path = 'aircraft_incident_ml.ipynb'
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    success = check_notebook(notebook_path)
    sys.exit(0 if success else 1)


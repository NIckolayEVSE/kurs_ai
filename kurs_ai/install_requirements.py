#!/usr/bin/env python3
"""
Скрипт для установки всех необходимых библиотек для notebook
"""
import subprocess
import sys

def install_package(package):
    """Устанавливает пакет через pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 80)
    print("УСТАНОВКА НЕОБХОДИМЫХ БИБЛИОТЕК")
    print("=" * 80)
    
    # Обязательные библиотеки
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'scikit-learn': 'scikit-learn',
    }
    
    # Опциональные библиотеки
    optional_packages = {
        'catboost': 'catboost',
        'tensorflow': 'tensorflow',
    }
    
    print("\n1. Установка обязательных библиотек:")
    print("-" * 80)
    
    failed = []
    for name, package in required_packages.items():
        print(f"Установка {name}...", end=" ")
        if install_package(package):
            print("✓ Успешно")
        else:
            print("✗ Ошибка")
            failed.append(name)
    
    print("\n2. Установка опциональных библиотек:")
    print("-" * 80)
    
    for name, package in optional_packages.items():
        print(f"Установка {name}...", end=" ")
        if install_package(package):
            print("✓ Успешно")
        else:
            print("⚠ Пропущено (опционально)")
    
    print("\n" + "=" * 80)
    if failed:
        print(f"⚠ Некоторые библиотеки не установлены: {', '.join(failed)}")
        print("Попробуйте установить вручную:")
        for name in failed:
            print(f"  pip install {required_packages[name]}")
    else:
        print("✓ Все обязательные библиотеки установлены!")
    print("=" * 80)

if __name__ == '__main__':
    main()


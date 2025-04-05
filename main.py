import pathlib
import re
import argparse
import sys

DEFAULT_STRUCTURE_FILENAME = "structure_definition.txt"

def create_project_structure(structure_string: str, base_dir: str):
    base_path = pathlib.Path(base_dir).resolve()
    if structure_string.startswith('\ufeff'):
        structure_string = structure_string[1:]
    lines = structure_string.strip().splitlines()

    indent_to_path_map = { -1: base_path }

    print(f"Создание структуры в: {base_path}")

    for line_number, line in enumerate(lines):
        line = line.replace('\t', '    ')

        stripped_line = line.lstrip()
        if not stripped_line or stripped_line.startswith('#'):
            continue

        name_part_match = re.search(r'[^│├──└─ ].*$', stripped_line)
        if not name_part_match:
            continue

        name_part = name_part_match.group(0)

        try:
            content_indent = line.index(name_part)
        except ValueError:
             content_indent = len(line) - len(line.lstrip(' '))
             print(f"Предупреждение (строка {line_number+1}): Не удалось точно определить отступ для '{name_part.strip()}'.")


        name_cleaned = name_part.split('#', 1)[0]
        name = name_cleaned.strip().rstrip('/')

        if not name or name == '.':
             continue

        parent_indent = -1
        for indent_val in sorted(indent_to_path_map.keys(), reverse=True):
            if indent_val < content_indent:
                parent_indent = indent_val
                break

        parent_path = indent_to_path_map.get(parent_indent)

        if parent_path is None:
             print(f"Ошибка (строка {line_number+1}): Не удалось найти родителя для '{name}' (отступ {content_indent}). Используется база.")
             parent_path = base_path
        elif not parent_path.is_dir(): # Доп. проверка родителя
             print(f"Ошибка (строка {line_number+1}): Родитель '{parent_path.relative_to(base_path)}' для '{name}' не папка. Пропуск.")
             continue

        current_path = parent_path / name

        original_content_stripped_trailing = name_part.split('#', 1)[0].rstrip()
        ends_with_slash = original_content_stripped_trailing.endswith('/')

        is_dir = ends_with_slash or ('.' not in name or (name.startswith('.') and '.' not in name[1:]))
        if name.startswith('.') and '.' in name[1:]:
            is_dir = False

        try:
            if is_dir:
                current_path.mkdir(parents=True, exist_ok=True)
                print(f"  + Папка:  {current_path.relative_to(base_path)}")
                indent_to_path_map[content_indent] = current_path # Обновляем карту
                indents_to_clear = [i for i in indent_to_path_map if i > content_indent]
                for i in indents_to_clear:
                    del indent_to_path_map[i]
            else:
                current_path.parent.mkdir(parents=True, exist_ok=True)
                current_path.touch(exist_ok=True)
                print(f"  - Файл:   {current_path.relative_to(base_path)}")

        except OSError as e:
             common_win_errors = {123: "Неверный синтаксис имени файла", 267: "Неверно задано имя папки"}
             win_error_msg = ""
             if sys.platform == "win32" and hasattr(e, 'winerror') and e.winerror in common_win_errors:
                 win_error_msg = f" (WinError {e.winerror}: {common_win_errors[e.winerror]})"
             print(f"Ошибка создания '{current_path.relative_to(base_path)}'{win_error_msg}: Проверьте имя '{name}'. Ошибка: {e}")

        except Exception as e:
            print(f"Непредвиденная ошибка для {current_path.relative_to(base_path)}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Создает структуру папок и файлов по текстовому описанию.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'structure_file_path',
        nargs='?',
        default=None,
        help=f"Путь к файлу с описанием структуры.\nЕсли не указан, используется '{DEFAULT_STRUCTURE_FILENAME}' в каталоге скрипта."
    )
    parser.add_argument(
        '-d', '--directory',
        default=".",
        help="Каталог, в котором будет создана структура (по умолчанию: текущий каталог)."
    )

    args = parser.parse_args()

    input_file_path = args.structure_file_path
    output_directory = args.directory

    if input_file_path is None:
        script_dir = pathlib.Path(__file__).parent.resolve()
        input_file_path = script_dir / DEFAULT_STRUCTURE_FILENAME
        print(f"Файл структуры не указан, используется по умолчанию: {input_file_path}")
    else:
        input_file_path = pathlib.Path(input_file_path).resolve()
        print(f"Используется файл структуры: {input_file_path}")

    try:
        with open(input_file_path, 'r', encoding='utf-8-sig') as f:
            project_structure_string = f.read()
            if not project_structure_string.strip():
                print(f"Ошибка: Файл структуры '{input_file_path}' пуст.")
                sys.exit(1)
    except FileNotFoundError:
        print(f"Ошибка: Файл структуры не найден по пути '{input_file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка чтения файла структуры '{input_file_path}': {e}")
        sys.exit(1)

    create_project_structure(project_structure_string, output_directory)

    print("\nСтруктура проекта успешно создана!")
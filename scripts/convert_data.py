import os
import pprint

def parse_spring_data(file_path, cities_data):
    """
    解析春季数据文件并更新 cities_data 字典。
    (使用 GBK 编码)
    """
    try:
        # 使用 GBK 编码
        with open(file_path, 'r', encoding='gbk') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                try:
                    year, city, temp_var, precip = line.split('\t')
                    if city not in cities_data:
                        cities_data[city] = {'spring': {'tempVariation': [], 'precipitation': []},
                                             'summer': {'avgTemp': [], 'effectiveTemp': []},
                                             'autumn': {'sunshineHours': [], 'avgTemp': [], 'precipitation': []}}
                    cities_data[city]['spring']['tempVariation'].append(float(temp_var))
                    cities_data[city]['spring']['precipitation'].append(float(precip))
                except ValueError as e:
                    print(f"跳过格式错误的行 {file_path}: {line} - 错误: {e}")
    except FileNotFoundError:
        print(f"错误: 文件未找到 {file_path}")
    except Exception as e:
        print(f"处理 {file_path} 时发生错误: {e}")

def parse_summer_data(file_path, cities_data):
    """
    解析夏季数据文件并更新 cities_data 字典。
    (使用 UTF-16 编码)
    """
    try:
        # 将 encoding='gbk' 修改为 encoding='utf-16'
        with open(file_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.split('\t')
                    year = parts[0]
                    city = parts[1]
                    avg_temp = parts[2].strip()
                    eff_temp = parts[3].strip()

                    if city not in cities_data:
                         cities_data[city] = {'spring': {'tempVariation': [], 'precipitation': []},
                                              'summer': {'avgTemp': [], 'effectiveTemp': []},
                                              'autumn': {'sunshineHours': [], 'avgTemp': [], 'precipitation': []}}
                    cities_data[city]['summer']['avgTemp'].append(float(avg_temp))
                    cities_data[city]['summer']['effectiveTemp'].append(float(eff_temp))
                except ValueError as e:
                    print(f"跳过格式错误的行 {file_path}: {line} - 错误: {e}")
                except IndexError as e:
                    print(f"跳过格式错误的行 (IndexError) {file_path}: {line} - 错误: {e}")
    except FileNotFoundError:
        print(f"错误: 文件未找到 {file_path}")
    except Exception as e:
        print(f"处理 {file_path} 时发生错误: {e}")


def parse_autumn_data(file_path, cities_data):
    """
    解析秋季数据文件并更新 cities_data 字典。
    (使用 GBK 编码)
    """
    try:
        # 使用 GBK 编码
        with open(file_path, 'r', encoding='gbk') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.split('\t')
                    year = parts[0]
                    city = parts[1]
                    sunshine = parts[2].strip()
                    avg_temp = parts[3].strip()
                    precip = parts[4].strip()

                    if city not in cities_data:
                         cities_data[city] = {'spring': {'tempVariation': [], 'precipitation': []},
                                              'summer': {'avgTemp': [], 'effectiveTemp': []},
                                              'autumn': {'sunshineHours': [], 'avgTemp': [], 'precipitation': []}}
                    cities_data[city]['autumn']['sunshineHours'].append(float(sunshine))
                    cities_data[city]['autumn']['avgTemp'].append(float(avg_temp))
                    cities_data[city]['autumn']['precipitation'].append(float(precip))
                except ValueError as e:
                    print(f"跳过格式错误的行 {file_path}: {line} - 错误: {e}")
                except IndexError as e:
                    print(f"跳过格式错误的行 (IndexError) {file_path}: {line} - 错误: {e}")

    except FileNotFoundError:
        print(f"错误: 文件未找到 {file_path}")
    except Exception as e:
        print(f"处理 {file_path} 时发生错误: {e}")

def main():
    """
    主函数，用于协调数据解析和打印。
    """
    # 定义文件名
    spring_file = '宁夏五市1980-2022春分到清明数据（插补后）.txt'
    summer_file = '宁夏五市1980-2022立夏到小满数据（插补后）.txt'
    autumn_file = '宁夏五市1980-2022小暑到立秋数据（插补后）.txt'

    # 初始化主数据字典
    cities = {}

    print(f"正在处理 {spring_file}...")
    parse_spring_data(spring_file, cities)
    print(f"正在处理 {summer_file}...")
    parse_summer_data(summer_file, cities)
    print(f"正在处理 {autumn_file}...")
    parse_autumn_data(autumn_file, cities)

    print("\n--- 提取的数据 ---")
    # 使用 pprint 更清晰地打印字典
    pprint.pprint(cities)
    print("--- 数据结束 ---")

if __name__ == "__main__":
    main()
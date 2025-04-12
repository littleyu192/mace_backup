import os
import re

def scientific_to_float(value):
    """
    将科学计数法值转换为具有 10 位小数的浮点数格式。
    """
    match = re.match(r"([-+]?\d+\.?\d*)\*\^([-+]?\d+)", value)
    if match:
        base, exponent = match.groups()
        return f"{float(base) * (10 ** int(exponent)):.10f}"
    else:
        return value

def convert_xyz_to_etxyz(input_folder, output_file):
    # 创建一个列表用于存储所有输出行
    output_lines = []

    # 遍历文件夹中的所有 .xyz 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".xyz"):
            input_file = os.path.join(input_folder, filename)
            
            with open(input_file, 'r') as file:
                lines = file.readlines()
            
            # 第一行：原子计数
            atom_count = int(lines[0].strip())
            
            # 第二行：原始属性行
            properties = lines[1].strip().split()
            
            # 定义属性名称
            property_names = [
                "tag", "index", "A", "B", "C", "mu", "alpha", "homo", "lumo",
                "gap", "r2", "zpve", "U0", "U", "H", "G", "Cv"
            ]
            
            # 将属性格式化为 属性名称=属性值
            formatted_properties = []
            for name, value in zip(property_names, properties):
                if name == "tag":
                    formatted_properties.append(f'{name}="{value}"')
                elif name in ["homo", "lumo", "gap", "zpve", "U0", "U", "H", "G"]:
                    formatted_properties.append(f'{name}={float(value) * 27.211386024367243}')
                else:
                    formatted_properties.append(f'{name}={value}')
            
            # 构造新的第二行
            new_second_line = "Properties=species:S:1:pos:R:3 " + " ".join(formatted_properties) + ' pbc="F F F"'
            
            # 添加第一行和修改后的第二行
            output_lines.append(lines[0])  # 原子计数
            output_lines.append(new_second_line + '\n')
            
            # 处理第 3 到 na+2 行：删去最后一个值
            for i in range(2, 2 + atom_count):
                line_parts = lines[i].strip().split()
                converted_line = " ".join(scientific_to_float(x) for x in line_parts[:-1])  # 删除最后一个值并转换
                output_lines.append(converted_line + '\n')

    # 将所有输出内容写入目标文件
    with open(output_file, 'w') as file:
        file.writelines(output_lines)

# 使用脚本
input_folder = "dsC7O2H10nsd.xyz"  # 输入文件夹路径
output_file = "output.xyz"  # 输出文件路径
convert_xyz_to_etxyz(input_folder, output_file)


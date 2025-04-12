def convert_xyz_format(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    output_lines = []
    i = 0
    while i < len(lines):
        # 读取每个分子的原子计数行和能量行
        atom_count = lines[i].strip()
        energy = lines[i + 1].strip()
        new_second_line = f"energy={energy} Properties=species:S:1:pos:R:3:forces:R:3"
        
        # 添加修改后的行到输出列表
        output_lines.append(atom_count + '\n')
        output_lines.append(new_second_line + '\n')
        
        # 复制剩余的原子信息行
        for j in range(int(atom_count)):
            output_lines.append(lines[i + 2 + j])
        
        # 跳到下一个分子
        i += 2 + int(atom_count)
    
    # 写入输出文件
    with open(output_file, 'w') as file:
        file.writelines(output_lines)

input_file = 'paracetamol_input.xyz'
output_file = 'paracetamol.xyz'
convert_xyz_format(input_file, output_file)

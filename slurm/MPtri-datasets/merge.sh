output_file="train.xyz"
rm -f $output_file
touch $output_file
traj_path="mptrj-gga-ggapu"
k=0

for i in {0..2000000..1}; do
    input_file="${traj_path}/mp-${i}.extxyz"
    if [ -f "$input_file" ]; then
        cat "$input_file" >> "$output_file"
        k=$((k+1))
        # 在k为1000的倍数时输出一次
        if [ $((k%1000)) -eq 0 ]; then
            echo "Merged $k files into $output_file"
        fi
    fi
done

for i in {5327,11882,14327,14772}; do
    input_file="${traj_path}/mvc-${i}.extxyz"
    if [ -f "$input_file" ]; then
        cat "$input_file" >> "$output_file"
        k=$((k+1))
    fi
done

echo "Merged $k files into $output_file"

from runner2xyz import load_type, print_xyz

# 读取数据
data = load_type('input.data')

# 输出 xyz
print_xyz(data, folder='./xyz', outfile='output.xyz', shift_energy_peratom=0)
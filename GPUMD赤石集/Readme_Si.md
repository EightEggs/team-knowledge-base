# NEP 机器学习势训练范例：晶体硅

> Ref. : https://doi.org/10.1063/5.0200833
>
> Version 2025/07/18, by zqchen & xtyu

可选：AIMD+微扰 / MD+微扰 / AIMD+MD+微扰

## 所需文件

注：本文档涉及的软件、脚本不一定为最优，读者可根据习惯进行调整

### DFT计算

AIMD + 单点计算：

`INCAR` / `KPOINTS` / `POSCAR` / `POTCAR` / `dft_sbatch.sh`（提交文件可更改名称，如 `run.sh`）

### GPUMD计算

`train.xyz` / `nep.in` / `nep.exe` /(`text.xyz`,可选)

### MD计算

`in.Si` （计算设定文件，约等于`INCAR`） / `lammps_sbatch.sh` / `Si.data` （结构文件，约等于`POSCAR`）/ `Si.tersoff` (势函数，约等于`POTCAR`)

## 结构获取

> https://next-gen.materialsproject.org/materials

根据材料，选取合适构型，可下载 `.cif` 文件或者 `POSCAR`文件

后续以 `.cif` 文件为例，进行讲解

## 晶胞阵列

（超胞Supercell）：Materials Studio or MATLAB ...

以Materials Studio为例：

① 保证 `.cif` 文件在英文目录下，导入MS（若英文路径仍无法导入，可在MS安装路径或其他英文路径导入）

② 依次点击`Build`-`Symmetry`-`Supercell`，修改参数进行超胞

③ 完成后进行导出，选择 `.cif` 格式

## POSCAR构建

方式：手动/MATLAB/Python...

以手动为例：

### 构建8原子POSCAR（初始单位晶胞）

① 打开MP下载的 `.cif`

② 复制`_cell_length`部分的晶矢（a,b,c）与原子位置部分的各原子分数坐标（x,y,z）

③ 新建文件，命名为`POSCAR`

④ `POSCAR`文件：第1行为名称，可随意命名，此处命名为Si8；第2行为晶矢缩放大小，默认为1.0；3-5行为步骤②复制的晶矢，分别为a,b,c；第6行为原子种类，此处为Si（若为多元素体系，则不同元素间用空格隔开）；第7行为各元素原子数目，此处为8（若为多元素体系，则需同元素写法一致，各元素原子数目用空格隔开，顺序与元素种类相同）；第8行为坐标类型，此处因复制的.cif文件中的分数坐标，因此为Direct，后续通过脚本更改为笛卡尔坐标（Cartesian）；第9行往后，为各原子位置坐标信息，此处为步骤②复制的.cif文件中的分数坐标（若为多元素体系，则原子顺序需与原子元素类型相对应）

⑤ 使用`OVITO`检查`POSCAR`构型是否正确

⑥ 64原子`POSCAR`操作类似

## POSCAR 原子坐标类型变换

脚本：`POSCAR_dire2cart.m`

以上步生成的8原子`POSCAR`文件为例：

① `POSCAR`重命名为`POSCAR.ori` (可任意更改)

② 运行 `.m` 文件，生成POSCAR_ini文件，即更改为笛卡尔坐标

## 手动批量生成结构（微扰+应变）

脚本：`generate_perturbed_POSCARs.m` / `generate_perturbed_normal_distribution_POSCARs.m` (Matlab运行)

① 随机微扰

i.  将 `.m` 文件与POSCAR.ini文件（重命名为POSCAR）放到同一目录下，在命令行窗口键入“`generate_perturbed_POSCARs('POSCAR','Si', 50, 0.03, 0.1);`” 运行(按需修改“（）”内部参数，分别为输入文件名称、文件夹前缀名称、生成结构的数量、晶格向量扰动比例、原子坐标扰动最大值)

ii. 运行后在当前目录下生成num_P个文件夹，各文件夹内均包含一个POSCAR文件

② 正态微扰（推荐使用：`ref.`: https://doi.org/10.1103/PhysRevB.111.085413）

i.  将 `.m` 文件与`POSCAR.ini`文件（重命名为POSCAR）放到同一目录下，在命令行窗口键入“`generate_perturbed_normal_distribution_POSCARs('POSCAR','Si', 50, 0.03, 0.1);`” 运行(按需修改“（）”内部参数，分别为输入文件名称、文件夹前缀名称、生成结构的数量、晶格向量扰动比例、原子坐标扰动标准差)

ii. 运行后在当前目录下生成num_P个文件夹，各文件夹内均包含一个`POSCAR`文件

## 生成POTCAR

① 登入集群

② 键入`cat /data3/home/SHARED/VASP/PAWPBE.54/Al/POTCAR /data3/home/SHARED/VASP/PAWPBE.54/C/POTCAR /data3/home/SHARED/VASP/PAWPBE.54/H/POTCAR /data3/home/SHARED/VASP/PAWPBE.54/Mo/POTCAR /data3/home/SHARED/VASP/PAWPBE.54/Se/POTCAR  > POTCAR` 

其中，“`/data3/home/SHARED/VASP/PAWPBE.54/Al/POTCAR`”为一个元素的POTCAR信息，更改位置为“Al”元素位置，修改为目标元素
如为多元素体系，则如②表示的内容，即多次键入单元素内容，并用空格间隔，最后的“` > POTCAR`”为指定将前述内容写入POTCAR

## 修改dft_sbatch.sh文件内容（按需）

① 打开`dft_sbatch.sh`文件，前6行结构入下：

#!/bin/bash
#SBATCH -J job_name
#SBATCH -n 32
#SBATCH -N 1
#SBATCH -A fem
#SBATCH -p fem

② 修改`job_name`为任务名称，如“`Si_perturbed_50`”（可通过后续`rename_sbatch.m`脚本批量修改）

③ 修改`#SBATCH -n 32`为`#SBATCH -n 16`，即修改为`16核`运行（按需修改），需对应节点核数：`normal 16；fem 32; dft 96`

④ 保持`#SBATCH -N 1`不变

⑤ 修改`#SBATCH -A fem`为`#SBATCH -A normal`，即修改为`normal`队列运行（按需修改），需与③调用核数一致：`normal 16；fem 32; dft 96`

⑥ 修改`#SBATCH -p fem`为`#SBATCH -p normal`，与③、⑤保持一致


## 批量复制

脚本：`copy_files.bat` 

(Windows双击运行)

以手动批量结构为例：

① 将`.bat`文件放入批量文件夹所在目录，保证目录中同时存在 INCAR、KPOINTS、POTCAR、dft_sbatch.sh 文件

② 双击运行，运行后可检查各文件夹中是否为5个文件：INCAR、KPOINTS、POSCAR、POTCAR、dft_sbatch.sh

可修改`.bat`文件（1，1，50）的50，替换为所要循环复制的次数（一般等于文件夹数量）

可修改`.bat`文件 "`folder=Si_%%i`"部分，改为需识别文件夹的统一前缀，以便识别

## 批量重命名

脚本：`rename_sbatch.m`

（Matlab运行）

对各文件夹中的`dft_sbatch.sh`文件的第一行名称进行修改，以区分提交的任务

可按需修改`numJobs`的值

可按需修改`sprintf（'', ）`中的值，改为需识别文件夹的统一前缀，以便识别

## DFT计算

### AIMD/单点计算

① 登入集群

### 单个提交

进入目标文件夹，在终端键入`sbatch dft_sbatch.sh`提交，并键入`squeue`或者 `squeue -u username` 查看队列情况

### 批量提交

脚本：`submit_dynamic_log.sh` （Slurm集群运行）

进入批量文件夹所在目录并运行脚本：
后台运行：
依次运行
`chmod +x submit_dynamic_log.sh`
`nohup ./submit_dynamic_log.sh > out.log 2>&1 &`
运行后会显示 [1] 3006， 后面的数字即为PID

脚本状态查看（是否在运行）：
`ps aux | grep submit_dynamic_log.sh`

终止脚本：

① 直接终止
`pkill -f submit_dynamic_log.sh`

② 查看 PID 后终止
`ps aux | grep submit_dynamic_log.sh`
`kill <PID>`

## MD计算

① 登入集群

② 进入目标文件夹，在终端键入`sbatch lammps_sbatch.sh`提交，并键入`squeue`或者 `squeue -u username` 查看队列情况

## MD输出转POSCAR

脚本：`dump2POSCAR.m` （Matlab运行）

按需修改：

`type_to_element = containers.Map({1}, {'Si'});` （dump文件中所包含原子类型数量）

`num_files = 100;` （生成文件夹数目/处理dump文件数目）

`interval = 100;` （dump文件输出间隔）

`folder_name = sprintf('Si_MD_%d', i);` （输出文件夹名称）

## 构建train.xyz（方法不唯一）

train.xyz结构可参考：
> https://github.com/brucefan1983/GPUMD/blob/master/doc/nep/input_files/train_test_xyz.rst

`train.xyz`文件第一行为原子数，第二行为元素种类，第三行为晶矢，第四行往后为原子坐标

① 登入集群并进入批量单点计算文件夹所在目录，此处以手动微扰结构的训练集单点计算结果为例

② 依次运行以下命令(需在集群个人文件夹中安装Python环境)：

`python3 batch_extract_vasp.py`

(按需修改“用户可修改部分”：文件夹前缀、后缀范围)

`python3 output_train_xyz.py`

(按需修改“用户修改区域”：文件夹前缀、后缀范围、config_type前缀)

③ 获得手动微扰结构的训练集单点计算结果构成的`train.xyz`文件

④ 同理，获取AIMD/MD抽样结构的单点计算`train.xyz`文件

⑤ 将两个traing.xyz文件合并为一个`train.xyz`文件（直接打开其中一个`train.xyz`文件，将其他`train.xyz`文件内容复制到其末尾即可）

## GPUMD计算

① 登录A6000塔式服务器

② 进入`D:\GPUMD-4.2\src`，复制`nep.exe`到`D:\个人文件夹\计算文件夹`

③ 进入`D:\个人文件夹\计算文件夹`，复制`train.xyz`到`D:\个人文件夹\计算文件夹`，并编写`nep.in`文件

`nep.in` 文件编写参考：
> https://github.com/brucefan1983/GPUMD/blob/master/doc/nep/input_files/nep_in.rst
基本可以默认，需修改的参数主要有：
i.  `type number_of_atom_types list_of_chemical_species`；
ii. `cutoff radial_cutoff angular_cutoff`

④ 保证`D:\个人文件夹\计算文件夹`中的存在nep.in、train.xyz、nep.exe文件，双击`nep.exe`运行程序，开始训练

⑤ 训练完成后，在`D:\个人文件夹\计算文件夹`中生成energy_train.out、force_train.out、loss.out、nep.restart、nep.txt、stress_train.out、virial_train.out文件，其中`nep.txt`为训练所得势函数，后续可用于GPUMD/MD模拟

⑥ 检查可靠性与精度：

i.  验证训练集精度

运行 `plot_nep_results.py` （需安装Python环境），输出对角线图+RMSE与loss图

ii. 对比训练集与验证集数据相似度（越靠近对角线越精确，RMSE越小越好）

⑦ 迭代训练 or 结束训练

**迭代训练：具体参考《分子动力学模拟》（樊哲勇）—— 5.3.2章节

## 附录

#Linux基本操作命令：

`squeue` #查看任务列表
`cd folder_name` #进入文件夹
`cd ..`#进入上一级文件夹
`pwd` #显示当前工作目录
`ls` #列出当前目录下文件
`cat file_name` #查看文件内容
`mkdir dir_name` #创建目录
`rmdir dir_name` #删除目录
`rm file_name` #删除文件
`cp` #复制文件
...

## 参考数据集获取

> https://materials.colabfit.org/browse/datasets?utm_source=chatgpt.com
> https://gitlab.com/brucefan1983/nep-data/-/tree/main?ref_type=heads

上述网站提供部分文献公开数据集，可根据需求下载使用。
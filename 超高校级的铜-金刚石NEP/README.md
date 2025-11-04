# NEP训练总结
## 1.Kpoints与Incar设置问题
Kpoints在大胞中不宜设置过大，否则会导致算力需求急剧提升
### K-points设置
参考来源：https://blog.shishiruqi.com/2019/04/25/kpoints/
**方法一：取倒数**
![alt text](image.png)
**方法二：VASPKIT**
![alt text](image-1.png)
![alt text](image-2.png)
目前积累的经验来看 kpoints才是决定vasp计算时间的主导因素
**方法三：
### ENCUT
取ENMAX即可（SB言论） 但最好参考具体体系的机器学习势文章
## 2.DFT计算精度验证
### 能量
计算原子归一化能量
E_per_atom = TOTEN/N_atomsET > ~0.001–0.005 eV/atom（1–5 meV/atom）不可接受
需要做KPOINTS收敛性测试（也并非必要 参考相近体系文献中ENCUT/KPOINTS也可以）
## 3.NEP精度验证
### 分组验证
对于包含多个组分的大训练集（Cu，Diamond，Cu/Diamond-hetero）最好单独训练对应的NEP 并验证其基本性质（晶格常数 https://periodictable.com/index.html 用于对照lattice constant的网站 ，声子色散-查文章），作为参考
否则合成为大数据集后训练，构型数量多，训练耗时长，还有可能计算错误
### 需要计算的基本性质
包括RMSE（E，F，V），R?，热导率，径向分布函数，能量体积曲线，晶格常数
#### RMSE(E,f,V)
#### 误差分布
![alt text](image-3.png)
#### 本征热导率计算
#### 径向分布函数
#### 声子色散（声子谱）
1. 结构优化
创建文件夹 mkdir 1.relaxation
**参考：https://zhuanlan.zhihu.com/p/631882073**
准备好POSCAR（Material Project直接下载POSCAR）/KPOINTS（原胞设大点感觉无所谓 我设定为Monk 12 12 12）/POTCAR/dft_sbatch.sh
运行vaspkit 101 LR 其自动生成的INCAR如下
![alt text](image-7.png)
把自动生成的INCAR改为如下格式
+ ENCUT 按照ENMAX设定
+ EDIFFG -0.001 精度更高 适合声子谱计算
+ ISMEAR 根据材料类型设定
![alt text](image-6.png)
提交计算
查看生成的CONTCAR 与 https://periodictable.com/index.html 中的晶格常数进行对比 
2. 力常数矩阵计算
**参考：https://www.huasuankeji.com/news/?p=323044** (华算) **https://liyihang1024.github.io/2023/11/09/** （一一风荷举）
VASP-Phonopy%E8%AE%A1%E7%AE%97%E5%A3%B0%E5%AD%90%E8%B0%B1/
有两种办法 一种是**DFPT-密度泛函微扰理论/线性响应方法** 一种是**有限位移法** 这里介绍DPFT方法
>+ **创建文件夹 mkdir 2.force_constants_dpft**
>+ **复制1.relaxation中的CONTCAR POTCAR 到2.force_constants_dpft，新建INCAR KPOINTS**
>+ **mv CONTCAR POSCAR-unitcell**
>+ **安装Phonopy #用conda很好装**
>+ **生成超胞 phonopy -d –dim=”2 2 2″ -c POSCAR-unitcell # dim代表晶胞大小**
>+ **cp SPOSCAR POSCAR**
>+ **INCAR设置如下**
ISMEAR =  0            (Gaussian smearing)
SIGMA  =  0.05         (Smearing value in eV)
IBRION =  8            (determines the Hessian matrix using DFPT)
EDIFF  =  1E-08        (SCF energy convergence; in eV)
PREC   =  Accurate     (Precision level)
ENCUT  =  400          (Cut-off energy for plane wave basis set, in eV)
IALGO  =  38           (Davidson block iteration scheme)
LREAL  = .FALSE.       (Projection operators: false)
LWAVE  = .FLASE.       (Write WAVECAR or not)
LCHARG = .FLASE.       (Write CHGCAR or not)
ADDGRID= .TRUE.        (Increase grid; helps GGA convergence)
NSW    = 1
NELM   = 100
NELMDL = -5
>+ **KPOINTS设置如下**
A
0
M
3  3  3 #晶胞扩了 小一点弄得快
0  0  0
>+ **提交vasp计算** 获取vasprun.xml
>+ phonopy –fc vasprun.xml 获取力常数矩阵文件 **FORCE_CONSTANTS**
3. 声子色散计算（声子谱）
新建文件夹 mkdir 3.phonon_dispersion 把2.force_constants_dpft中的vasprun.xml，POSCAR-unitcell都复制过来
把POSCAR-unitcell改名为POSCAR
vaspkit 03 305 3
生成KPATH.phonopy
https://seekpath.materialscloud.io/compute/process_structure/ 把POSCAR-unitcell传上去 看VASP KPOINTS input for LDA/GGA 与生产的KPATH.phonopy 对比
![alt text](image-8.png) 
mv KPATH.phonopy band.conf
其后对band.conf进行修改 保留需要的参数 计算色散的标准设置如下：
![alt text](image-9.png)
phonopy -c POSCAR band.conf -p -s 生成phonopy.yaml、band.yaml和band.pdf文件
phonopy-bandplot --gnuplot > PBAND.dat   # 可导入Origin画图、phonopy-bandplot --gnuplot > phonon.out  
#### 能量-体积曲线
#### 代表性构型的晶格常数
## 4.绘图相关
https://github.com/tang070205/tools 提供了许多NEP相关的工具
+ plot_nep_results.py 
用来画RMSE和Loss 且可以自动无视**无virial结构**进行绘图
![alt text](image-4.png)
![alt text](image-5.png)

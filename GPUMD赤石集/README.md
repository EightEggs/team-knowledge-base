# n2p2数据集转nep数据集流程简记
 ## 步骤1：runner格式简介
 n2p2软件包使用runner格式作为输入文件格式，其单帧构造如下：
 ***
 >begin
comment `<comment>`
lattice `<ax> <ay> <az>`
lattice `<bx> <by> <bz>`
lattice `<cx> <cy> <cz>`
atom `<x1> <y1> <z1> <e1> <c1> <n1> <fx1> <fy1> <fz1>`
atom `<x2> <y2> <z2> <e2> <c2> <n2> <fx2> <fy2> <fz2>`
...
atom `<xn> <yn> <zn> <en> <cn> <nn> <fxn> <fyn> <fzn>`
energy `<energy>`
charge `<charge>`
end
***
二者所使用描述符形式存在区别，n2p2（Behler–Parinello 风格 NN）用的是**原子中心对称函数** （radial/angular symmetry functions）作为描述符 + 每种元素/交互的 NN，NEP（GPUMD 的 Neuroevolution Potential）用的是基于 **Chebyshev/Legendre** 的基函数展开因此无法逐字逐句一一映射。
>:memo: **GPT提供的解释，以上我不懂**

 ## 步骤2：runner格式转换xyz
 GPUMD开发者——渤海大学樊哲勇提供了一系列xyz转换脚本：
 https://github.com/brucefan1983/GPUMD/tree/master/tools/Format_Conversion
 在这里我们使用runner2xyz
 https://github.com/brucefan1983/GPUMD/tree/master/tools/Format_Conversion/runner2xyz

该脚本使用流程如下
***
>**1.打开命令行**
Windows 下可以用 cmd 或 PowerShell
**2.切换到脚本所在目录**
cd "D:\科研文档\p8.Polarization_interface\Polarization"
**3.创建输出文件夹**
脚本会把 XYZ 文件输出到 名为xyz的文件夹，如果不存在，需要先创建：
mkdir xyz
**4.运行脚本**
python runner2xyz.py training-set_final.data output.xyz 0
参数说明：
training-set_final.data → 输入训练文件
output.xyz → 输出 XYZ 文件名
0 → 每原子能量平移（不需要平移就写 0）
**5.结果**
***
>:memo: **以上脚本包含准确单位换算。能量大于绝对值属正常现象，因cp2k单位是Ha，换成eV会很大。**

 ## 步骤3：能量平移矫正
 ### 探索方案1：深圳大学陈浙锐Energy-Reference-Aligner.py脚本 :x:
 #### 1.尝试在windows服务器上运行

>:warning:**项目开发者在linux编写。该脚本windows就算能运了也会有换行符错误，读结构完全读不出来**

 ###### python程序包Calorine安装报错
 >unistd.h”: No such file or directory error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2 [end of output] 
 note: This error originates from a subprocess, and is likely not a problem with pip. 
 ERROR: Failed building wheel for calorine Failed to build calorine error: failed-wheel-build-for-install × Failed to build installable wheels for some pyproject.toml based projects 
 ╰─> calorine

 Caroline的C++ 源文件包含了 <unistd.h>，这是一个 POSIX（类 Unix）头文件，在 Linux / macOS 上存在，但 在 Windows 的 MSVC 编译器下不存在，因此用 Visual Studio 的 cl.exe 编译会失败（这是 pip 在本机尝试编译扩展时触发的）。另外 PyPI 上当前是源码分发，pip 需要在本机编译扩展而没有预编译的 Windows wheel，所以 pip 会尝试调用本机编译器并失败。
>:memo:**GPT提供的解释。于师兄曾通过conda在windows服务器上安装并运行caoline，具体原理不详**


 #### 2.尝试在linux服务器上运行
 >:warning:**课题组集群只有python3.7，此脚本要求python3.8**:sweat_smile:
  ###### 服务器安装报错
  >`/data3/home/zqchen/.local/lib/python3.7/site-packages/pandas/compat/__init__.py:120: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError. warnings.warn(msg) Traceback (most recent call last): File "Energy-Reference-Aligner.py", line 70, in <module> from calorine.calculators import CPUNEP ModuleNotFoundError: No module named 'calorine.calculators'`

1.Could not import the lzma module：说明你当前这套 Python 是“从源码编译但在编译时缺少 lzma 开发库（liblzma-dev）”或 Python 安装不完整；这会引起 pandas 的警告但通常不是导致 calorine 导入失败的直接原因。
2.ModuleNotFoundError: No module named 'calorine.calculators'：说明当前 Python 环境中安装的 calorine 包要么没有安装完整（某些模块缺失），要么你用的 Python 不是安装 calorine 的那个 Python（路径/环境问题），或者安装出了错误。calorine 本身确实含有 calorine.calculators 模块（文档可证）。
>:memo:**GPT提供的解释**

### 探索方案2：python工具包NepTrainKit
 下载链接：
 https://github.com/aboys-cb/NepTrainKit?tab=GPL-3.0-1-ov-file
 >:memo:**运行要求python 3.10**
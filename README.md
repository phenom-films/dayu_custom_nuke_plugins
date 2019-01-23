# dayu_custom_nuke_plugins
[![python](https://img.shields.io/badge/python-2.7-blue.svg)]()
[![github license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/phenom-films/dayu_custom_nuke_plugins/blob/master/license)

# 简介
此项目是一个nuke 的工具集管理系统，使用和配置都非常的简单，用户只需要将自己的工具脚本，放到对应的文件层级下，即可nuke中看到

项目中nuke 文件夹下，四个文件夹分别对应着不同的功能：
 * callbacks: 用来放置回调脚本，参考项目中`nuke/callbacks/Write_OnCreate.py` 文件，文件命名格式 节点名_回调事件.py。放置在此文件夹下的文件，会自动注册为nuke回调
 * main_menu: 在此文件夹下放置的脚本，gizimo等节点，会出现在nuke主窗口的菜单栏上，菜单层级和文件夹层级一致，每层文件夹会被自动显示成为一层菜单
 * nodes: 在此文件夹下放置的脚本，gizimo等节点，会出现在nuke 左侧边的工具栏上，同上，以文件夹层级为菜单层级
 * views: 此文件夹下放置 LUT型文件，将LUT文件放置在此文件夹下，将会自动出现在nuke 监看窗口的色彩选择栏中
 
用户管理自己的工具只需要将工具脚本，gizimo节点等文件，放到对应的文件夹下，或者建立子文件夹来分门别类。放置完成后，启动nuke,便可以在dayu_toolkit菜单
中看到自己放置的工具,需要注意的是：
* 菜单名和文件夹或文件的名字一致
* 在文件的同级下，放置一个同名的的png图像文件可自动识别为菜单图标（文件夹同）
* 在文件的同级下，放置一个同名的.hotkey 文件，里面写入组合快捷键，便可以为菜单设置快捷键（参考 `nuke/nodes/dayu_utils_utils/quick_open_file.hotkey`）
# 两种启动方式
## windows 平台
### 快捷启动
直接双击 `nuke_launcher.bat`
快速启动nuke(启动的为系统中最新版本的nukex)，工具集文件夹为此项目目录下nuke 文件夹
    
### 自主配置
分为两步
* 拷贝项目中的nuke 文件夹到任意目录下，在系统中添加环境变量 MY_CUSTOM_FITMENT，指定为自己拷贝后的文件夹路径(如 `D:/work/nuke` )
* 将项目中 fitment/nuke_fitment 文件夹拷贝到任意目录下，在系统中添加环境变量 NUKE_PATH (若已经存在，在已有的值后追加)，指定为拷贝后的nuke_fitment 文件夹的路径(如 `D:/work/nuke_fitment` )
* 上述两个环境变量配置完成后，启动机器上任意版本的nuke,可以发现工具集出现在主菜单和左侧菜单栏中
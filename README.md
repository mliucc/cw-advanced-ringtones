# Class Widgets 铃声自定义
**插件正在开发中，请等待后续开发完成后上架插件广场！**
## 简介
cw-ring-personality，一个可以为Class Widgets提供**高度自定义铃声**的插件
## 计划实现的功能
- [x] 上课铃、下课铃、预备铃、午休铃、放学铃
- [ ] 自定义其他铃声
- [x] 通过修改main.py进行配置
- [x] 通过修改config.json进行配置
- [ ] 通过修改config.json进行配置
- [ ] 通过设置UI进行配置
## 如何使用（暂时无法使用）
- **安装插件**  在Class Widgets插件广场下载插件（暂未上架）
- **更换音频**  打开Class Widgets主程序所在目录，转到./plugin/cw-ring_personality/plugin_audio，按照下面对应关系更换音频，要求为**wav格式** <br>
  >上课铃→attend_class.wav <br> 下课铃→finish_class.wav <br> 预备铃→prepare_class.wav <br> 午休铃→noon.wav <br> 放学铃→finish_school.wav
- **配置铃声**  使用notepad或其他文本读写软件打开**Class Widgets主程序所在目录下的config.ini**，并将**插件目录下的config.ini**中的内容复制进**主程序的config.ini**，再**根据注释内容**修改配置文件进行配置
- **启动插件**  打开Class Widgets设置页面，在**铃声页签**将程序自带通知铃声声音改至最小（**请务必确认该步骤完成，否则将同时响2个铃声**）；在**插件页签**将“铃声自定义”打开即可食用

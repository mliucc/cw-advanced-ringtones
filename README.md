# Class Widgets 铃声自定义
## 简介
cw-ring-personalize，一个可以为Class Widgets提供**高度自定义铃声**的插件
## 计划实现的功能
- [x] 上课铃、下课铃、预备铃、午休铃、放学铃
- [ ] 自定义其他铃声
- [x] 通过修改main.py进行配置
- [ ] 通过修改config.json进行配置
- [ ] 通过设置UI进行配置
## 如何使用
- **安装插件**  在Class Widgets插件广场下载插件（暂未上架）
- **更换音频**  打开Class Widgets主程序所在目录，转到./plugin/cw-ring_personalize/plugin_audio，按照下面对应关系更换音频，要求为**wav格式** <br>
  >上课铃→attend_class.wav <br> 下课铃→finish_class.wav <br> 预备铃→prepare_class.wav <br> 午休铃→noon.wav <br> 放学铃→finish_school.wav
- **配置午休铃**  使用notepad或其他文本读写软件打开main.py，在#修改午休铃#**两条同名注释**之间的区域**依照注释提示**修改配置
- **启动插件**  打开Class Widgets设置页面，在**铃声页签**将程序自带通知铃声声音改至最小（**请务必确认该步骤完成，否则将同时响2个铃声**）；在**插件页签**将“铃声自定义”打开即可食用

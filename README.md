# Class Widgets 高级铃声
## 简介
cw-advanced-ringtones，一个可以为Class Widgets提供**高级铃声**的插件
## 计划/已经实现的功能
- [x] 支持早读铃、上课铃、下课铃、预备铃、午休铃、放学铃
- [ ] 自定义其他铃声类型
- [x] 通过修改config.json进行配置
- [ ] 通过设置UI进行配置
## 如何使用
- **安装插件**  在Class Widgets插件广场下载插件
- **更换音频**  打开Class Widgets主程序所在目录，转到./plugin/cw-advanced-ringtones/plugin_audio，按照下面对应关系更换音频，要求为**wav格式** <br>
  >早读铃→attend_school.wav<br> 上课铃→attend_class.wav <br> 下课铃→finish_class.wav <br> 预备铃→prepare_class.wav <br> 午休铃→noon.wav <br> 放学铃→finish_school.wav
- **配置铃声**  在**主程序插件页签**将“高级自定义铃声”打开，转到./plugin/cw-advanced-ringtones，打开**config.json**，按照下面提示进行配置： 
   > > 更改铃声大小："volume": ***1~100间的一个整数，数字越大音量越大***（默认为75）
   > 
   > > 午休铃声配置："noon_cfg": 
   > > > 午休铃声类型："noon_type": "***0或1, 0为原下课铃（即打铃后进入课间），1为原上课铃（即打铃后进入下一节课）***",
   > >  
   > > > 午休铃声对应课程："noon_class": "***主程序显示通知上的课程名称***"
   >  
   > > 早读铃声配置："attend_school_cfg": **与上述午休铃声配置同理**
- **启动插件**  打开Class Widgets设置页面，在**铃声页签**将程序自带通知铃声声音改至最小（**请务必确认该步骤完成，否则将可能出现重复响铃的问题**），并设置一个另外的课程表、时间线进行测试，符合用户需求后即可食用

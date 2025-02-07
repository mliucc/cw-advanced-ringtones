# Class Widgets 高级铃声
> [!WARNING]
> 1.本插件目前无法检测来自其他插件的通知，如需使用该类型插件，请**使用本插件的通知模块**或卸载本插件并调整主程序铃声音量以解决问题 <br>
> 2.由于插件迭代需求，更新需要重置配置文件，请在更新前备份config.json，并在更新后修改重命名example.json，后续版本将会解决该问题

> [!IMPORTANT]
> 由于人手原因及功能复杂度，插件未经过广泛测试，请确保投入使用前使用一套单独的时间线、课程表进行测试，如有问题请及时[提交issue反馈](https://github.com/mliucc/cw-advanced-ringtones/issues)
## 简介
一个可以为Class Widgets提供**高级铃声与通知**的插件
## 计划/已经实现的功能
- [x] 支持早读铃、上课铃、下课铃、预备铃、午休铃、放学铃
- [x] 支持自定义铃声配置（测试2个铃声通过，理论支持铃声数量无限)
- [x] 支持发送自定义通知
- [x] 通过修改config.json进行配置
- [ ] 通过设置UI进行配置
## 使用指南
- **安装插件**  在Class Widgets插件广场下载插件
- **更换音频**  打开Class Widgets主程序所在目录，转到./plugin/cw-advanced-ringtones/plugin_audio，按照下面对应关系添加或更换音频，要求为**wav格式** <br>
  >早读铃→attend_school.wav<br> 上课铃→attend_class.wav <br> 下课铃→finish_class.wav <br> 预备铃→prepare_class.wav <br> 午休铃→noon.wav <br> 放学铃→finish_school.wav <br> 其他自定义铃声→ringtone***序号[^1]***.wav
- **配置铃声**  进入./plugin/cw-advanced-ringtones目录，打开**config.json**，按照下面提示进行配置： 
   > 更改铃声大小："volume": ***1~100间的一个整数，数字越大音量越大***（默认为75）
   >
   > 午休铃声配置："noon_cfg": 
   > > 铃声开关："noon_switch": "***0或1, 0为关闭铃声，1为开启铃声***"
   > >
   > > 铃声类型："noon_type": "***0或1, 0为原下课铃（即打铃后进入课间），1为原上课铃（即打铃后进入下一节课）***"
   > >
   > > 铃声对应课程："noon_class": "***主程序显示通知上的课程名称***"
   > > ![铃声课程示例](img/ring_class.png)
   >
   > 早读铃声配置："attend_school_cfg": **与上述午休铃声配置同理**
   >
   > 自定义铃声配置[^2]："extra_ringtones"："ringtone***序号[^1]***_cfg": **与上述午休铃声配置同理**
- **配置通知**  进入./plugin/cw-advanced-ringtones目录，打开**config.json的"notifications"模块**，按照下面提示进行配置： 
   > 通知开关："notification***序号[^1]***_switch": ***0或1, 0为关闭通知，1为开启通知***
   > 
   > 通知铃声："notification***序号[^1]***_ring": ***输入./plugin/cw-advanced-ringtones/plugin_audio目录下的文件名（\*.wav）***
   > 
   > 通知类别："notification***序号[^1]***_state": ***0或1或3或4，0为下课铃，1为上课铃，3为预备铃，4为其他通知***
   > 
   > 通知持续时长："notification***序号[^1]***_duration": ***通知窗口在屏幕上显示的时长，单位为毫秒ms***
   > 
   > 通知时间："notification***序号[^1]***_time": ***发送通知的时间，格式为mm:ss（如07:30；11:46；17:05）***
   > 
   > 通知课程："notification***序号[^1]***_lesson": ***如图，"notification_state"为0或1或3时需要修改***
   > ![state为0或1或3时示例](img/notification_1.png)
   >
   > 通知主标题："notification***序号[^1]***_content": ***如图，仅"notification_state"为4时需要修改***
   >
   > 通知副标题："notification***序号[^1]***_content": ***如图，仅"notification_state"为4时需要修改***
   >
   > 通知内容："notification***序号[^1]***_content": ***如图，仅"notification_state"为4时需要修改***
   > ![state为4时示例](img/notification_4.png)

- **启动插件**  打开Class Widgets设置页面，设置一个另外的课程表、时间线进行测试，符合用户需求后即可食用

[^1]: 序号：**从1开始，每次增加1的整数**（自定义铃声与通知之间不能混用），如ringtone1，ringtone2（铃声）；notification1，notification2（通知）
[^2]: 配置：插件**自带2段铃声配置与通知配置**，如需增加，请**复制自带部分并修改序号[^1]**，并保证序号[^1]及配置的格式与**已有部分完全相同**
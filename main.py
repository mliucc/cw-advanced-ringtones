#高级铃声插件v1.1.3-b2
#1.添加自定义通知支持
#2.修改自定义铃声配置读取逻辑
#3.添加对于早读、午休铃声的开关
#4.修复若干bug

from sys import *
from loguru import logger
from .ClassWidgets.base import PluginBase, PluginConfig  # 导入CW的基类

from datetime import datetime
import pygame
import os
import conf

mainconfig = conf.read_conf('Audio', 'volume')

class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法
        #json配置文件装载
        default_config = {
            "version": "1.1.3-b2",
            "volume": "75",
            "noon_cfg": {
                "noon_switch": "0",
                "noon_type": "None",
                "noon_class": "None"
            },
            "attend_school_cfg": {
                "attend_school_switch": "0",
                "attend_school_type": "None",
                "attend_school_class": "None"
            },
            "file": {
                "prepare_class": "prepare_class.wav",
                "attend_class": "attend_class.wav",
                "finish_class": "finish_class.wav",
                "attend_school": "attend_school.wav",
                "noon": "noon.wav",
                "finish_school": "finish_school.wav",
                "default": "default.wav"
            },
            "extra_ringtones": {
                "ringtone_quanlity": "0",
                "ringtone_file": {
                    "ringtone1": "ringtone1.wav",
                    "ringtone2": "ringtone2.wav"
                },
                "ringtone1_cfg": {
                    "ringtone1_switch": "0",
                    "ringtone1_type": "None",
                    "ringtone1_class": "None"
                },
                "ringtone2_cfg": {
                    "ringtone2_switch": "0",
                    "ringtone2_type": "None",
                    "ringtone2_class": "None"
                }
            },
            "notifications": {
                "notification_quanlity": "0",
                "notification1_cfg": {
                    "notification1_switch": "0",
                    "notification1_ring": "ringtone1",
                    "notification1_state": "None",
                    "notification1_time": "None",
                    "notification1_lesson": "None",
                    "notification1_message": "None",
                    "notification1_duration": "None"
                }
            }
        }
        self.cfg = PluginConfig(self.PATH, 'config.json')  # 实例化配置类
        self.cfg.load_config(default_config)  # 加载配置

        #通知模块初始化
        self.notified_times = set()  # 用于记录已经发送通知的时间点
        self.current_date = datetime.now().date()  # 记录当前日期

    def execute(self):  # 自启动执行部分
        conf.write_conf('Audio', 'volume',0) #设置主程序通知音量为0
        global playsound,prepare_class,attend_class,finish_class,attend_school,noon,finish_school,default,noon_type,noon_class,attend_school_type,attend_school_class,vol,extring_file,extring_cfg,notifi_cfg,notification

        #------------------------------------------------------铃声模块-----------------------------------------------------------
        #预设铃声文件读取
        prepare_class = self.cfg['file']['prepare_class']
        attend_class = self.cfg['file']['attend_class']
        finish_class = self.cfg['file']['finish_class']
        finish_school = self.cfg['file']['finish_school']
        default = self.cfg['file']['default']

        if int(self.cfg['noon_cfg']['noon_switch']) == 1:
            noon = self.cfg['file']['noon']
            logger.success('高级铃声插件提示：午休铃声已启用')
        if int(self.cfg['attend_school_cfg']['attend_school_switch']) == 1:
            attend_school = self.cfg['file']['attend_school']
            logger.success('高级铃声插件提示：早读铃声已启用')
        
        #自定义铃声文件读取与配置
        extring_file = {}
        extring_cfg = {}
        if int(self.cfg['extra_ringtones']['ringtone_quanlity']) > 0:
            for i in range(int(self.cfg['extra_ringtones']['ringtone_quanlity'])):
                i = i + 1
                extring_filename = f'extring_{i}'
                extring_type = f'extring{i}_type'
                extring_class = f'extring{i}_class'
                #判定铃声是否启用，若启用则加载文件与配置
                if int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_switch']) == 1:
                    extring_file[extring_filename] = self.cfg['extra_ringtones']['ringtone_file'][f'ringtone{i}']
                    extring_cfg[extring_type] = int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_type'])
                    extring_cfg[extring_class] = self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_class']
                    logger.success(f'高级铃声插件提示：自定义铃声{i}已启用')
                else:
                    logger.error(f'高级铃声插件提示：自定义铃声{i}已禁用')
            logger.info('高级铃声插件提示：当前共启用' + self.cfg['extra_ringtones']['ringtone_quanlity'] + '个自定义铃声，请确认该数量与实际启用自定义铃声数量（即config.json中extra_ringtones中ringtone_quanlity数字与各ringtone_cfg中ringtone_switch值为1的数量）一致')
        elif int(self.cfg['extra_ringtones']['ringtone_quanlity']) == 0:
            logger.info('高级铃声插件提示：当前未启用自定义铃声模块')
        else: 
            logger.error('高级铃声插件提示：自定义铃声数量错误，请检查config.json中ringtone_quanlity数字是否为正整数')

        #预设铃声配置
        noon_type = int(self.cfg['noon_cfg']['noon_type'])       #午休铃对应通知类型
        noon_class = self.cfg['noon_cfg']['noon_class']      #午休铃对应课程
        attend_school_type = int(self.cfg['attend_school_cfg']['attend_school_type'])       #早读铃对应通知类型
        attend_school_class = self.cfg['attend_school_cfg']['attend_school_class']      #早读铃对应课程

        vol = int(self.cfg['volume'])    #铃声音量

        #播放铃声
        global playsound 
        pygame.mixer.init()
        def playsound(filename):
            try:
                file_path = os.path.join(self.PATH, 'plugin_audio', filename)
                pygame.mixer.music.load(file_path)
                volume = vol / 100
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play()
            except Exception as e:
                logger.error(f'高级铃声插件读取预设音频文件出错：{e}')

        #------------------------------------------------------通知模块-----------------------------------------------------------
        #通知配置读取
        notifi_cfg = {}
        if int(self.cfg['notifications']['notification_quanlity']) > 0:
            for i in range(int(self.cfg['notifications']['notification_quanlity'])):
                i = i + 1
                notifi_ring = f'notifi{i}_ring'
                notifi_state = f'notifi{i}_state'
                notifi_time = f'notifi{i}_time'
                notifi_lesson = f'notifi{i}_lesson'
                notifi_message = f'notifi{i}_message'
                notifi_duration = f'notifi{i}_duration'

                #判定通知是否启用，若启用则加载配置
                if int(self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_switch']) == 1:
                    notifi_cfg[notifi_ring] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_ring']
                    notifi_cfg[notifi_state] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_state']
                    notifi_cfg[notifi_time] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_time']
                    notifi_cfg[notifi_lesson] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_lesson']
                    notifi_cfg[notifi_message] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_message']
                    notifi_cfg[notifi_duration] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_duration']
                    logger.success(f'高级铃声插件提示：通知{i}已启用，将在' + notifi_cfg[notifi_time] + '时通知，类型序号为' + notifi_cfg[notifi_state] + '，内容为' + notifi_cfg[notifi_message] + '，持续时长为' + notifi_cfg[notifi_duration] + ' ms ，铃声为' + notifi_cfg[notifi_ring])
                else:
                    logger.info(f'高级铃声插件提示：通知{i}已禁用')
            logger.info('高级铃声插件提示：当前共启用' + self.cfg['notifications']['notification_quanlity'] + '个通知，请确认该数量与实际启用通知数量（即config.json中notifications中notifi_quanlity数字与各notifi_cfg中notifi_switch值为1的数量）一致')
        elif int(self.cfg['notifications']['notification_quanlity']) == 0:
            logger.info('高级铃声插件提示：当前未启用通知模块')
        else: 
            logger.error('高级铃声插件提示：通知数量错误，请检查config.json中notifi_quanlity数字是否为正整数')
    
    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        self.cfg.update_config()  # 更新配置
        #------------------------------------------------------铃声模块-----------------------------------------------------------
        #判定主程序是否发送通知
        if self.method.is_get_notification():
            custom_ringtone_played = False
            i = 1
            #自定义铃声
            if int(self.cfg['extra_ringtones']['ringtone_quanlity']) > 0:    #判定启用自定义铃声
                while not custom_ringtone_played and i <= int(self.cfg['extra_ringtones']['ringtone_quanlity']):
                    try:
                        #播放铃声
                        if int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_switch']) == 1 and self.cw_contexts['Notification']['state'] == extring_cfg[f'extring{i}_type'] and self.cw_contexts['Notification']['lesson_name'] == extring_cfg[f'extring{i}_class']:
                            playsound(extring_file[f'extring_{i}'])
                            custom_ringtone_played = True
                            logger.info(f'高级铃声插件播放铃声：自定义铃声{i}')
                    except Exception as e:
                        logger.error(f'高级铃声插件播放自定义铃声{i}出错：{e}')
                    i = i + 1
                
            #预设铃声(急需重构的shit山)
            if not custom_ringtone_played:
                if self.cw_contexts['Notification']['state'] == 2:    #判定放学
                    try:
                        playsound(finish_school)
                        logger.info('插件cw-advanced-ringtones播放铃声：放学')
                    except Exception as e:
                        logger.error(f'插件cw-advanced-ringtones播放 放学 铃声出错：{e}')
                elif self.cw_contexts['Notification']['state'] == attend_school_type and self.cw_contexts['Notification']['lesson_name'] == attend_school_class:    #判定早读
                    try:
                        playsound(attend_school)
                        logger.info('插件cw-advanced-ringtones播放铃声：早读')
                    except Exception as e:
                        logger.error(f'插件cw-advanced-ringtones播放 早读 铃声出错：{e}')
                elif self.cw_contexts['Notification']['state'] == noon_type and self.cw_contexts['Notification']['lesson_name'] == noon_class:    #判定午休
                    try:
                        playsound(noon)
                        logger.info('插件cw-advanced-ringtones播放铃声：午休')
                    except Exception as e:
                        logger.error(f'插件cw-advanced-ringtones播放 午休 铃声出错：{e}')
                else:    #判定普通铃声
                    if self.cw_contexts['Notification']['state'] == 0:    #判定下课
                        try:
                            playsound(finish_class)
                            logger.info('插件cw-advanced-ringtones播放铃声：下课')
                        except Exception as e:
                            logger.error(f'插件cw-advanced-ringtones播放 下课 铃声出错：{e}')
                    elif self.cw_contexts['Notification']['state'] == 1:    #判定上课
                        try:
                            playsound(attend_class)
                            logger.info('插件cw-advanced-ringtones播放铃声：上课')
                        except Exception as e:
                            logger.error(f'插件cw-advanced-ringtones播放 上课 铃声出错：{e}')
                    elif self.cw_contexts['Notification']['state'] == 3:    #判定预备
                        try:
                            playsound(prepare_class)
                            logger.info('插件cw-advanced-ringtones播放铃声：准备上课')
                        except Exception as e:
                            logger.error(f'插件cw-advanced-ringtones播放 预备 铃声出错：{e}')
                    elif self.cw_contexts['Notification']['state'] == 4:    #判定其他通知
                        try:
                            playsound(default)
                            logger.info('插件cw-advanced-ringtones检测到其他通知，将使用默认铃声')
                        except Exception as e:
                            logger.error(f'插件cw-advanced-ringtones检测到 其他 通知，播放 默认 铃声出错：{e}')
                    else:
                        logger.error('插件cw-advanced-ringtones检测到未知通知，将不播放铃声，请检查主程序的日志以排查问题')
        
        #------------------------------------------------------通知模块-----------------------------------------------------------
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        today = now.date()
        # 如果日期变化（即到了第二天），清空已通知的时间点
        if today != self.current_date:
            self.notified_times.clear()
            self.current_date = today  # 更新当前日期
        try:
            for i in range(int(self.cfg['notifications']['notification_quanlity'])):
                i = i + 1
                if current_time == notifi_cfg[f'notifi{i}_time'] and current_time not in self.notified_times:
                    if int(notifi_cfg[f'notifi{i}_state']) == 4: 
                        self.method.send_notification(
                            state=int(notifi_cfg[f'notifi{i}_state']),
                            title='高级铃声插件通知',
                            content=notifi_cfg[f'notifi{i}_message'],
                            duration=int(notifi_cfg[f'notifi{i}_duration']) 
                        )
                    elif int(notifi_cfg[f'notifi{i}_state']) == 3:
                        self.method.send_notification(
                            state=int(notifi_cfg[f'notifi{i}_state']),
                            duration=int(notifi_cfg[f'notifi{i}_duration']), 
                        )
                    else:
                        self.method.send_notification(
                            state=int(notifi_cfg[f'notifi{i}_state']),
                            lesson_name = notifi_cfg[f'notifi{i}_lesson'],
                            duration=int(notifi_cfg[f'notifi{i}_duration']) 
                        )
                    self.notified_times.add(current_time)
                    playsound(notifi_cfg[f'notifi{i}_ring'])
                    logger.info(f'高级铃声插件发送通知：{notifi_cfg[f"notifi{i}_message"]}')
        except NameError:
            pass
        except Exception as e:
                logger.error(f'高级铃声插件发送通知出错：{e}')        


#高级铃声插件v1.1.3-b4
from sys import *
from loguru import logger
from .ClassWidgets.base import PluginBase, PluginConfig  # 导入CW的基类

from datetime import datetime
import pygame
import os
import conf

class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法
        global default_config
        #json配置文件装载
        default_config = {
            "version": "1.1.3-b4",
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
                    "notification1_ring": "ringtone1.wav",
                    "notification1_state": "None",
                    "notification1_time": "None",
                    "notification1_duration": "None",
                    "notification1_lesson": "None",
                    "notification1_title": "None",
                    "notification1_subtitle": "None",
                    "notification1_content": "None"
                }
            }
        }
        self.cfg = PluginConfig(self.PATH, 'config.json')  # 实例化配置类
        self.cfg.load_config(default_config)  # 加载配置

        #通知模块初始化
        self.notified_times = set()  # 用于记录已经发送通知的时间点
        self.current_date = datetime.now().date()  # 记录当前日期

    def execute(self):  # 自启动执行部分
        
        global is_latest_version
        plugin_version = default_config['version']
        config_version = self.cfg['version']
        if plugin_version == config_version:
            is_latest_version = True
            logger.success('高级铃声插件 版本校验完成.')
        else:
            is_latest_version = False
            logger.error('高级铃声插件 版本校验错误，为保证主程序正常运行，插件将不进行加载.')
        #判定config.json版本是否与插件版本相同
        if is_latest_version:
            conf.write_conf('Audio', 'volume',0) #设置主程序通知音量为0
            global playsound,prepare_class,attend_class,finish_class,attend_school,noon,finish_school,default,noon_type,noon_class,attend_school_type,attend_school_class,vol,extring_file,extring_cfg,notifi_cfg,notification,ringtone_quanlity,ringtone_enabled_quanlity,notifi_quanlity,notifi_enabled_quanlity
            #------------------------------------------------------铃声模块-----------------------------------------------------------
            #预设铃声文件读取与配置
            prepare_class = self.cfg['file']['prepare_class']
            attend_class = self.cfg['file']['attend_class']
            finish_class = self.cfg['file']['finish_class']
            finish_school = self.cfg['file']['finish_school']
            default = self.cfg['file']['default']

            if int(self.cfg['noon_cfg']['noon_switch']) == 1:
                noon = self.cfg['file']['noon']
                noon_type = int(self.cfg['noon_cfg']['noon_type'])       #午休铃对应通知类型
                noon_class = self.cfg['noon_cfg']['noon_class']      #午休铃对应课程
                logger.success('高级铃声插件提示：午休铃声已启用.')
            if int(self.cfg['attend_school_cfg']['attend_school_switch']) == 1:
                attend_school = self.cfg['file']['attend_school']
                attend_school_type = int(self.cfg['attend_school_cfg']['attend_school_type'])       #早读铃对应通知类型
                attend_school_class = self.cfg['attend_school_cfg']['attend_school_class']      #早读铃对应课程
                logger.success('高级铃声插件提示：早读铃声已启用.')
        
            #自定义铃声文件读取与配置
            extring_file = {}
            extring_cfg = {}
            ringtone_enabled_quanlity = 0
            ringtone_quanlity = 0
            for key, value in self.cfg['extra_ringtones'].items():
                if "cfg" in key:
                    ringtone_quanlity += 1
            for j in range(ringtone_quanlity):
                j=  j + 1
                if int(self.cfg['extra_ringtones'][f'ringtone{j}_cfg'][f'ringtone{j}_switch']) == 1:
                    ringtone_enabled_quanlity += 1
            if ringtone_quanlity > 0:
                for i in range(ringtone_quanlity):
                    i = i + 1
                    #判定铃声是否启用，若启用则加载文件与配置
                    if int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_switch']) == 1:
                        extring_file[f'extring_{i}'] = self.cfg['extra_ringtones']['ringtone_file'][f'ringtone{i}']
                        extring_cfg[f'extring{i}_type'] = int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_type'])
                        extring_cfg[f'extring{i}_class'] = self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_class']
                        logger.success(f'高级铃声插件提示：自定义铃声{i}已启用.')
                    else:
                        logger.info(f'高级铃声插件提示：自定义铃声{i}已禁用.')
                logger.info('高级铃声插件提示：当前共启用' + str(ringtone_enabled_quanlity) + '个自定义铃声.')
            elif ringtone_quanlity == 0:
                logger.info('高级铃声插件提示：当前未启用自定义铃声模块.')
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
                    logger.error(f'高级铃声插件读取预设音频文件出错：{e}.')

            #------------------------------------------------------通知模块-----------------------------------------------------------
            #通知配置读取
            notifi_cfg = {}
            notifi_enabled_quanlity = 0
            notifi_quanlity = 0
            for key, value in self.cfg['notifications'].items():
                if "cfg" in key:
                    notifi_quanlity += 1
            for j in range(notifi_quanlity):
                j =  j + 1
                if int(self.cfg['notifications'][f'notification{j}_cfg'][f'notification{j}_switch']) == 1:
                    notifi_enabled_quanlity += 1

            if notifi_enabled_quanlity > 0:
                for i in range(notifi_quanlity):
                    i = i + 1
                    #判定通知是否启用，若启用则加载配置
                    if int(self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_switch']) == 1:
                        notifi_cfg[f'notifi{i}_ring'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_ring']
                        notifi_cfg[f'notifi{i}_state'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_state']
                        notifi_cfg[f'notifi{i}_time'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_time']
                        notifi_cfg[f'notifi{i}_duration'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_duration']
                        notifi_cfg[f'notifi{i}_lesson'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_lesson']
                        notifi_cfg[f'notifi{i}_title'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_title']
                        notifi_cfg[f'notifi{i}_subtitle'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_subtitle']
                        notifi_cfg[f'notifi{i}_content'] = self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_content']
                        logger.success(f'高级铃声插件提示：通知{i}已启用.')
                    else:
                        logger.info(f'高级铃声插件提示：通知{i}已禁用.')
                logger.info('高级铃声插件提示：当前共启用' + str(notifi_enabled_quanlity) + '个通知.')
            elif int(notifi_enabled_quanlity) == 0:
                logger.info('高级铃声插件提示：当前未启用通知模块.')
    
    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        self.cfg.update_config()  # 更新配置
        try:
            if is_latest_version:
                #------------------------------------------------------铃声模块-----------------------------------------------------------
                #判定主程序是否发送通知
                if self.method.is_get_notification():
                    custom_ringtone_played = False
                    #自定义铃声
                    if ringtone_enabled_quanlity > 0:
                        for i in range(ringtone_quanlity):
                            try:
                                #播放铃声
                                if int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_switch']) == 1 and self.cw_contexts['Notification']['state'] == extring_cfg[f'extring{i}_type'] and self.cw_contexts['Notification']['lesson_name'] == extring_cfg[f'extring{i}_class']:
                                    playsound(extring_file[f'extring_{i}'])
                                    custom_ringtone_played = True
                                    logger.info(f'高级铃声插件播放铃声：自定义铃声{i}.')
                            except Exception as e:
                                logger.error(f'高级铃声插件播放自定义铃声{i}出错：{e}.')
                            i = i + 1
                
                    #预设铃声
                    if not custom_ringtone_played:
                        if self.cw_contexts['Notification']['state'] == 2:    #判定放学
                            try:
                                playsound(finish_school)
                                logger.info('插件cw-advanced-ringtones播放铃声：放学.')
                            except Exception as e:
                                logger.error(f'插件cw-advanced-ringtones播放 放学 铃声出错：{e}.')
                        elif self.cw_contexts['Notification']['state'] == attend_school_type and self.cw_contexts['Notification']['lesson_name'] == attend_school_class and int(self.cfg['attend_school_cfg']['attend_school_switch']) == 1:    #判定早读
                            try:
                                playsound(attend_school)
                                logger.info('插件cw-advanced-ringtones播放铃声：早读.')
                            except Exception as e:
                                logger.error(f'插件cw-advanced-ringtones播放 早读 铃声出错：{e}.')
                        elif self.cw_contexts['Notification']['state'] == noon_type and self.cw_contexts['Notification']['lesson_name'] == noon_class and int(self.cfg['noon_cfg']['noon_switch']) == 1:    #判定午休
                            try:
                                playsound(noon)
                                logger.info('插件cw-advanced-ringtones播放铃声：午休.')
                            except Exception as e:
                                logger.error(f'插件cw-advanced-ringtones播放 午休 铃声出错：{e}.')
                        else:    #判定普通铃声
                            if self.cw_contexts['Notification']['state'] == 0 and conf.read_conf('Toast', 'finish_class') == 1:    #判定下课
                                try:
                                    playsound(finish_class)
                                    logger.info('插件cw-advanced-ringtones播放铃声：下课.')
                                except Exception as e:
                                    logger.error(f'插件cw-advanced-ringtones播放 下课 铃声出错：{e}.')
                            elif self.cw_contexts['Notification']['state'] == 1 and conf.read_conf('Toast', 'attend_class') == 1:    #判定上课
                                try:
                                    playsound(attend_class)
                                    logger.info('插件cw-advanced-ringtones播放铃声：上课.')
                                except Exception as e:
                                    logger.error(f'插件cw-advanced-ringtones播放 上课 铃声出错：{e}.')
                            elif self.cw_contexts['Notification']['state'] == 3 and conf.read_conf('Toast', 'prepare_class') == 1:    #判定预备
                                try:
                                    playsound(prepare_class)
                                    logger.info('插件cw-advanced-ringtones播放铃声：准备上课.')
                                except Exception as e:
                                    logger.error(f'插件cw-advanced-ringtones播放 预备 铃声出错：{e}.')
                            elif self.cw_contexts['Notification']['state'] == 4:    #判定其他通知
                                try:
                                    playsound(default)
                                    logger.info('插件cw-advanced-ringtones检测到其他通知，将使用默认铃声.')
                                except Exception as e:
                                    logger.error(f'插件cw-advanced-ringtones检测到 其他 通知，播放 默认 铃声出错：{e}.')
                            else:
                                logger.error('插件cw-advanced-ringtones检测到未知通知，将不播放铃声，请检查日志以排查问题.')
        
                #------------------------------------------------------通知模块-----------------------------------------------------------
                now = datetime.now()
                current_time = now.strftime('%H:%M')
                today = now.date()
                # 如果日期变化（即到了第二天），清空已通知的时间点
                if today != self.current_date:
                    self.notified_times.clear()
                    self.current_date = today  # 更新当前日期
                try:
                    if notifi_enabled_quanlity > 0:
                        for i in range(notifi_quanlity):
                            i = i + 1
                            if int(self.cfg['notifications'][f'notification{i}_cfg'][f'notification{i}_switch']) == 1:
                                if current_time == notifi_cfg[f'notifi{i}_time'] and current_time not in self.notified_times:
                                    if int(notifi_cfg[f'notifi{i}_state']) == 4: 
                                        self.method.send_notification(
                                            state = int(notifi_cfg[f'notifi{i}_state']),
                                            title = '高级铃声插件通知',
                                            subtitle = notifi_cfg[f'notifi{i}_subtitle'],
                                            content = notifi_cfg[f'notifi{i}_content'],
                                            duration = int(notifi_cfg[f'notifi{i}_duration']) 
                                        )
                                    elif int(notifi_cfg[f'notifi{i}_state']) == 0 or int(notifi_cfg[f'notifi{i}_state']) == 1 or int(notifi_cfg[f'notifi{i}_state']) == 3:
                                        self.method.send_notification(
                                            state = int(notifi_cfg[f'notifi{i}_state']),
                                            lesson_name = notifi_cfg[f'notifi{i}_lesson'],
                                            duration = int(notifi_cfg[f'notifi{i}_duration']) 
                                        )
                                    self.notified_times.add(current_time)
                                    playsound(notifi_cfg[f'notifi{i}_ring'])
                                    logger.info(f'高级铃声插件发送通知{i}.')
                except NameError:
                    pass
                except Exception as e:
                    logger.error(f'高级铃声插件发送通知出错：{e}.')        
        except NameError:
            pass


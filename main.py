#高级铃声插件v1.1.2
#1.每次启动时自动设置主程序通知音量为0
#2.新增自定义铃声配置，默认为2个铃声，理论支持铃声数量无限

from loguru import logger
from .ClassWidgets.base import PluginBase, PluginConfig  # 导入CW的基类


import pygame
import os
import conf

mainconfig = conf.read_conf('Audio', 'volume')

class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法
        #json配置文件装载
        default_config = {
            "version": "1.1.1",
            "volume": "75",
            "noon_cfg": {
                "noon_type": "1",
                "noon_class": "午自习"
            },
            "attend_school_cfg": {
                "attend_school_type": "1",
                "attend_school_class": "进班"
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
            }
        }
        self.cfg = PluginConfig(self.PATH, 'config.json')  # 实例化配置类
        self.cfg.load_config(default_config)  # 加载配置
        
        

    def execute(self):  # 自启动执行部分
        conf.write_conf('Audio', 'volume',0) #设置主程序通知音量为0
        global playsound,prepare_class,attend_class,finish_class,attend_school,noon,finish_school,default,noon_type,noon_class,attend_school_type,attend_school_class,vol,extring_file,extring_cfg
        
        #预设铃声文件读取
        prepare_class = self.cfg['file']['prepare_class']
        attend_class = self.cfg['file']['attend_class']
        finish_class = self.cfg['file']['finish_class']
        attend_school = self.cfg['file']['attend_school']
        noon = self.cfg['file']['noon']
        finish_school = self.cfg['file']['finish_school']
        default = self.cfg['file']['default']
        #自定义铃声文件读取
        logger.info('高级铃声插件提示：当前共启用' + self.cfg['extra_ringtones']['ringtone_quanlity'] + '个自定义铃声，请确认该数量与实际启用自定义铃声数量（即config.json中extra_ringtones中ringtone_quanlity数字与各ringtone_cfg中ringtone_switch值为1的数量）一致')
        extring_file = {}
        extring_cfg = {}
        for i in range(int(self.cfg['extra_ringtones']['ringtone_quanlity'])):
            i = i + 1
            extring_filename = f'extring_{i}'
            extring_type = f'extring{i}_type'
            extring_class = f'extring{i}_class'
            #判定铃声是否启用，若启用则加载文件与配置
            exec(f'''
if int(self.cfg['extra_ringtones']['ringtone{i}_cfg']['ringtone{i}_switch']) == 1:
    extring_file[extring_filename] = self.cfg['extra_ringtones']['ringtone_file']['ringtone{i}']
    extring_cfg[extring_type] = int(self.cfg['extra_ringtones']['ringtone{i}_cfg']['ringtone{i}_type'])
    extring_cfg[extring_class] = self.cfg['extra_ringtones']['ringtone{i}_cfg']['ringtone{i}_class']
    logger.success('高级铃声插件提示：自定义铃声{i}已启用')
else:
    logger.error('高级铃声插件提示：自定义铃声{i}已禁用，请关闭程序后修改config.json中ringtone_quanlity数字与本处提示启用的铃声数量一致！')
            ''')

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

    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        self.cfg.update_config()  # 更新配置
        #判定主程序是否发送通知
        if self.method.is_get_notification():
            custom_ringtone_played = False
            i = 1
            custom_ringtone_played = False
            while not custom_ringtone_played and i <= int(self.cfg['extra_ringtones']['ringtone_quanlity']):
                try:
#自定义铃声
                    if int(self.cfg['extra_ringtones'][f'ringtone{i}_cfg'][f'ringtone{i}_switch']) == 1 and self.cw_contexts['Notification']['state'] == extring_cfg[f'extring{i}_type'] and self.cw_contexts['Notification']['lesson_name'] == extring_cfg[f'extring{i}_class']:
                        playsound(extring_file[f'extring_{i}'])
                        custom_ringtone_played = True
                        logger.info(f'高级铃声插件播放铃声：自定义铃声{i}')
                except Exception as e:
                    logger.error(f'高级铃声插件播放自定义铃声{i}出错：{e}')
                i = i + 1
                
#预设铃声
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

                


#高级铃声插件v1.0.1

#待实现功能：
#config.json存储铃声配置
#QtDesigner 设置UI
#自定义其他铃声

from PyQt5 import uic
from loguru import logger
from datetime import datetime
from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig  # 导入CW的基类


import pygame
import os
import conf
from conf import base_directory



class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法
        global playsound,prepare_class,attend_class,finish_class,noon,finish_school,default,noon_type,noon_class,vol

        #铃声文件名(请在config.ini内配置)
        prepare_class = conf.read_conf('File','prepare_class')
        attend_class = conf.read_conf('File','attend_class')
        finish_class = conf.read_conf('File','finish_class')
        noon = conf.read_conf('File','noon')
        finish_school = conf.read_conf('File','finish_school')
        default = conf.read_conf('File','default')
        print(attend_class)
        #配置铃声区域(请在config.ini内配置)
        noon_type = conf.read_conf('Noon','noon_type')       #午餐铃或午自习铃对应通知类型（见config.ini）
        noon_class = conf.read_conf('Noon','noon_class')      #午餐铃或午自习铃对应课程(见config.ini)
        vol = ('Volume','volume')    #铃声音量（见config.ini)
        #配置铃声区域(请在config.ini内配置)


    def execute(self):  # 自启动执行部分
        global playsound
        
        #播放铃声
        pygame.mixer.init()
        def playsound(filename):
            try:
                print(base_directory)
                file_path = os.path.join(base_directory, 'plugins', 'cw-ring-personality', 'plugin_audio', filename)
                pygame.mixer.music.load(file_path)
                volume = vol / 100
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play()
            except Exception as e:
                logger.error(f'插件cw-ring-personality读取音频文件出错：{e}')

    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        #判定主程序是否发送通知
        if self.method.is_get_notification():
            if self.cw_contexts['Notification']['state'] == 2:    #判定放学
                try:
                    playsound(finish_school)
                    logger.info('插件cw-ring-personality播放铃声：放学')
                except Exception as e:
                    logger.error(f'插件cw-ring-personality播放 放学 铃声出错：{e}')
            elif self.cw_contexts['Notification']['state'] == noon_type and self.cw_contexts['Notification']['lesson_name'] == noon_class:    #判定午休
                try:
                    playsound(noon)
                    logger.info('插件cw-ring-personality播放铃声：午休')
                except Exception as e:
                    logger.error(f'插件cw-ring-personality播放 午休 铃声出错：{e}')
            else:    #判定普通铃声
                if self.cw_contexts['Notification']['state'] == 0:    #判定下课
                    try:
                        playsound(finish_class)
                        logger.info('插件cw-ring-personality播放铃声：下课')
                    except Exception as e:
                        logger.error(f'插件cw-ring-personality播放 下课 铃声出错：{e}')
                elif self.cw_contexts['Notification']['state'] == 1:    #判定上课
                    try:
                        playsound(attend_class)
                        logger.info('插件cw-ring-personality播放铃声：上课')
                    except Exception as e:
                        logger.error(f'插件cw-ring-personality播放 上课 铃声出错：{e}')
                elif self.cw_contexts['Notification']['state'] == 3:    #判定预备
                    try:
                        playsound(prepare_class)
                        logger.info('插件cw-ring-personality播放铃声：准备上课')
                    except Exception as e:
                        logger.error(f'插件cw-ring-personality播放 预备 铃声出错：{e}')
                elif self.cw_contexts['Notification']['state'] == 4:    #判定其他通知
                    try:
                        playsound(default)
                        logger.infof('插件cw-ring-personality检测到其他通知，将使用默认铃声')
                    except Exception as e:
                        logger.error(f'插件cw-ring-personality检测到 其他 通知，播放 默认 铃声出错：{e}')
                else:
                    logger.info('插件cw-ring-personality检测到未知通知，将不播放铃声，请检查主程序的日志以排查问题')
                    


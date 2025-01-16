#高级铃声插件v1.0.1

from PyQt5 import uic
from loguru import logger
from datetime import datetime
from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig  # 导入CW的基类


import pygame
import os
import conf
from conf import base_directory

#铃声文件名
prepare_class = 'prepare_class.wav'
attend_class = 'attend_class.wav'
finish_class = 'finish_class.wav'
noon = 'noon.wav'
finish_school = 'finish_school.wav'

#配置铃声区域
noon_type = 0       #午餐铃或午自习铃对应通知类型（0为课间，1为上课）
noon_class = '午自习'      #午餐铃或午自习铃对应课程(如上一项为1则在''内填写该活动名称；如上一项为0则在''内填写下面一个活动的活动名称，且上一节课、该课间与下一节课同一节点内)
vol = 75
#配置铃声区域


class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法


    def execute(self):  # 自启动执行部分
        global playsound
        #播放铃声
        pygame.mixer.init()
        def playsound(filename):
            try:
                file_path = os.path.join(base_directory, 'plugins', 'cw-ring-personalize-no-setting-test', 'plugin_audio', filename)
                pygame.mixer.music.load(file_path)
                volume = 75 / 100
                #可在上面修改音量（如将“75”换为“90”以增大音量）
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play()
            except Exception as e:
                logger.error(f'插件“高级铃声无设置版测试”读取音频文件出错：{e}')

    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        #判定主程序是否发送通知
        if self.method.is_get_notification():
            if self.cw_contexts['Notification']['state'] == 2:    #判定是否放学
                playsound(finish_school)
                logger.info('插件cw-ring-personalize播放铃声：放学')
            elif self.cw_contexts['Notification']['state'] == noon_type and self.cw_contexts['Notification']['lesson_name'] == noon_class:    #判定是否午休
                playsound(noon)
                logger.info('插件cw-ring-personalize播放铃声：午休')
            else:
                if self.cw_contexts['Notification']['state'] == 0:
                    playsound(finish_class)
                    logger.info('插件cw-ring-personalize播放铃声：下课')
                elif self.cw_contexts['Notification']['state'] == 1:
                    playsound(attend_class)
                    logger.info('插件cw-ring-personalize播放铃声：上课')
                elif self.cw_contexts['Notification']['state'] == 3:
                    playsound(prepare_class)
                    logger.info('插件cw-ring-personalize播放铃声：准备上课')
                else:
                    logger.info('插件cw-ring-personalize检测到其他通知，不进行打铃')
                    


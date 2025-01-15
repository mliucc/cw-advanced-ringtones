#高级铃声无设置版测试

from PyQt5 import uic
from loguru import logger
from datetime import datetime
from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig  # 导入CW的基类


import pygame
import os
import conf
from conf import base_directory

prepare_class = 'prepare_class.wav'
attend_class = 'attend_class.wav'
finish_class = 'finish_class.wav'
noon = 'noon.wav'
finish_school = 'finish_school.wav'

#播放午餐铃或午自习铃
noon_type = 0       #午餐铃或午自习铃对应通知类型（0为课间，1为上课）
noon_class = '午自习'      #午餐铃或午自习铃对应课程(如上一项为1则在''内填写该活动名称；如上一项为0则在''内填写下面一个活动的活动名称，且上一节课、该课间与下一节课同一节点内)

#音频播放


class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法


    def execute(self):  # 自启动执行部分
        global playsound
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
        if self.method.is_get_notification(): 
            if self.cw_contexts['Notification']['state'] == 2:
                print('1')
                playsound(finish_school)
            elif self.cw_contexts['Notification']['state'] == noon_type and self.cw_contexts['Notification']['lesson_name'] == noon_class:
                print('2')
                playsound(noon)
            elif noon_type == 0 and self.cw_contexts['Notification']['state'] == 1:
                print('3')
                playsound(attend_class)
            elif noon_type == 1 and self.cw_contexts['Notification']['state'] == 0:
                print('4')
                playsound(finish_class)
            elif self.cw_contexts['Notification']['state'] == 3:
                print('5')
                playsound(prepare_class)
            elif noon_type == 0 and self.cw_contexts['Notification']['state'] == 0 and self.cw_contexts['Notification']['lesson_name'] != noon_class:
                print('6')
                playsound(finish_class)
            elif noon_type == 1 and self.cw_contexts['Notification']['state'] == 1 and self.cw_contexts['Notification']['lesson_name'] != noon_class:
                print('7')
                playsound(attend_class)



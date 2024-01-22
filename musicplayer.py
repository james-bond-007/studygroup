import pygame
from pygame import mixer
from pygame.locals import USEREVENT
import os
import random
import time
import datetime


class MusicPlayer:
    def __init__(self, my_config):
        self.config = my_config
        self.music_folder = self.config.get_config("music_folder")
        self.STOP_EVENT = USEREVENT + 1  # 音乐停止事件
        self.paths = [os.path.join(self.music_folder, item) for item in os.listdir(self.music_folder) if
                      item.endswith(".mp3")]

    def play_music(self, up_or_down=1):
        paths = self.paths
        if up_or_down == 1:
            # shuffle and add a special track at the beginning
            random.shuffle(self.paths)
            paths.insert(0, f"{os.getcwd()}{os.sep}src{os.sep}下课.mp3")
            play_duration = self.config.get_config("down_play_duration")
        else:
            paths = [f"{os.getcwd()}{os.sep}src{os.sep}上课.mp3"]
            play_duration = self.config.get_config("up_play_duration")

        if len(paths) > 0:
            cur = 0
            start_time = datetime.datetime.now()
            mixer.init()
            pygame.init()
            mixer.music.set_endevent(USEREVENT + 1)
            mixer.music.set_volume(0.85)
            mixer.music.load(paths[cur].encode("utf-8"))  # 加载，支持中文文件名
            mixer.music.play()  # 播放
            print("播放音乐")
            # Wait for the music to finish
            while (datetime.datetime.now() - start_time).seconds < play_duration:
                time.sleep(1)
                event = pygame.event.poll()
                if event.type == self.STOP_EVENT:
                    cur += 1
                    if cur != len(paths):
                        mixer.music.load(paths[cur].encode("utf-8"))
                        mixer.music.play()
                    else:
                        break
            pygame.quit()


if __name__ == '__main__':
    # This would be instantiated and used in the main part of your program
    import config as co

    config = co.Configuration('config.yaml')
    music_player = MusicPlayer(config)
    music_player.play_music(1)

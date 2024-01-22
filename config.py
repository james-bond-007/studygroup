import os
from tkinter import filedialog
import tkinter as tk
import yaml


class Configuration:
    def __init__(self, config_file):
        self.config_file = config_file
        """读取yaml数据"""
        with open(self.config_file, encoding='utf-8') as f:
            self.config = yaml.safe_load(f.read())
        # Check if the music folder exists, if not, open the directory selection dialog
        self.set_music_folder()
        self.set_class_time()

    def set_class_time(self):
        self.config['class_time'] = []
        self.config['after_class_time'] = []
        for rule in self.config["str_rules"]:
            # Split the line into two parts: the time and the class name
            index, time, class_name = rule.split("|")
            # print(time)
            # Split the time into two parts: the start time and the end time
            start_time, end_time = time.split("-")

            # Add the start time to the up class times list
            self.config['class_time'].append(start_time.strip())

            # Add the end time to the down class times list
            self.config['after_class_time'].append(end_time.strip())

    def set_music_folder(self):
        while not self.config["music_folder"] or not os.path.exists(self.config["music_folder"]):
            print("Music folder not found. Please select a folder containing music.")
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes("-topmost", True)  # Set topmost to True to bring the window to the front
            folder_selected = filedialog.askdirectory(title="Select Music Folder")

            if folder_selected:
                self.set_config("music_folder", folder_selected)
                self.save_config()
            else:
                # 用户取消选择，可以进行相应处理
                print("用户取消选择")
            root.destroy()
            root.quit()

    def get_config(self, key):
        return self.config.get(key, None)

    def set_config(self, key, value):
        # Set the configuration value if the key exists
        if key in self.config:
            original_value = self.config[key]
            self.config[key] = value
            print(f"Updated '{key}' from {original_value} to {value}")
        else:
            print(f"Key '{key}' does not exist in the configuration. Unable to set value.")

    def save_config(self):
        # Save the modified configuration to the YAML file
        """向yaml文件写入数据"""
        with open(self.config_file, encoding='utf-8', mode='w') as f:
            return yaml.dump(self.config, stream=f, allow_unicode=True)


if __name__ == '__main__':
    config = Configuration("config.yaml")
    import pprint
    pprint.pprint(config.config)

    # Example: Set and save a configuration value
    config.set_config("title_name", "网络云自习")
    config.save_config()

    # Example: Attempt to set a value for a non-existing key
    config.set_config("non_existing_key", "Some Value")
    config.save_config()

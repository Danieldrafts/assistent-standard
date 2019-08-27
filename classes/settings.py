import configparser
import reprlib

class Settings:
    def __init__(self, file_name = "settings.ini"):
        self._enviroment_file = file_name
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read(self._enviroment_file)

    @property
    def enviroment_file(self):
        return self._enviroment_file

    @enviroment_file.setter
    def enviroment_file(self, file_name):
        self._enviroment_file = file_name

    def get_sections(self):
        return self.config.sections()

    def get_configurations(self):
        return self.config

    def get_section_settings(self, section):
        settings = {}
        try:
            for setting in self.config[section]:
                settings[setting] = self.config[section][setting]
            return settings
        except Exception as identifier:
            print("--->>> Could not find configuration <<---")
            return False
    
    def edit_configuration_section(self, section, settings):
        try:
            for change in settings:
                self.replace_single_setting(section, change, settings[change])
            input("Changes have been made successfully")
        except exception as error:
            input("--->>> An error occurred when the changes were being made\n {} <<<---".format(error))

    def delete_configuration_section(self, section):
        self.config.remove_section(section)
        with open(self._enviroment_file, 'w') as configFile:
                self.config.write(configFile)
        input("{} Deleted".format(section))

    def replace_single_setting(self, section, setting, value):
        self.config.set(section, setting, value)
        with open(self._enviroment_file, 'w') as configFile:
                self.config.write(configFile)

    @staticmethod
    def view_configurations_static():
        print(self.config)
    
    def write_new_setting(self, setting_section_name, settings):
        try:
            self.config[setting_section_name] = settings
            with open(self._enviroment_file, 'w') as configFile:
                self.config.write(configFile)
            return input("\n ---------------------------\n Configuration created successfully!\n")
        except Exception as error:
            print("--->>> Error when write the settings in Configuration File: <<<---")
    
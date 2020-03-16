import yaml
import requirements

import pysoup.utils


class Parser(object):

    def __init__(self):
        pass

    def parse_file(self, path):
        with open(path, 'rb') as f:
            yaml_data = f.read()
        return self.parse(yaml_data)

    def parse(self, string):
        return yaml.load(string)

    def dump_to_file(self, configuration, path):
        yaml_data = self.dump(configuration)
        with open(path, 'wb') as f:
            f.write(yaml_data)

    def dump(self, configuration):
        yaml_string = ''
        for key in ['name', 'author', 'version', 'repository', 'dependencies']:
            if configuration.has_key(key):
                yaml_string += yaml.dump({key: configuration[key]}, default_flow_style=False)
        return yaml_string

    def parse_pip_requirements(self, path):
        target_config = {'dependencies': {}}

        with open(path, 'rb') as f:
            requirements_list = f.read()

        for requirement in requirements.parse(requirements_list):
            soup_requirement_name = requirement.name

            if requirement.specs:
                soup_version = pysoup.utils.version_notation_pip_to_soup(''.join(requirement.specs[0]))
            else:
                soup_version = '*'

            target_config['dependencies'][soup_requirement_name] = soup_version

        return target_config

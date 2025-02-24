from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import yaml

class ReplaceVariablesProcessor(InlineProcessor):
    def __init__(self, pattern, variables, md=None):
        self.variables = variables
        super(ReplaceVariablesProcessor, self).__init__(pattern, md)

    def handleMatch(self, m, data):
        key = m.group(1)
        if key in self.variables:
            return self.variables[key], m.start(0), m.end(0)
        return None, None, None

class ReplaceVariablesExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'variables' : [{}, "varibles to replace"],
            'yaml_file': ['', "Path to the YAML file containing variables"],
        }
        super(ReplaceVariablesExtension, self).__init__(**kwargs)

    def load_variables_from_yaml(self, yaml_file):
        if yaml_file:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                return {}
        return {}

    def extendMarkdown(self, md):
        yaml_file = self.getConfig('yaml_file')
        variables = self.getConfig('variables').copy()
        
        variables_yaml = self.load_variables_from_yaml(yaml_file)
        if 'replace_variables' in variables_yaml:
            variables.update(variables_yaml['replace_variables'])
        else:
            variables.update(variables_yaml)

        META_VAR_PATTERN = r'\{\{(.*?)\}\}'  # like {{xxxx}}
        md.inlinePatterns.register(ReplaceVariablesProcessor(META_VAR_PATTERN, variables, md), 'meta-var', 175)

def makeExtension(**kwargs):
    return ReplaceVariablesExtension(**kwargs)

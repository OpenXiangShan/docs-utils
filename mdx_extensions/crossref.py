from markdown import Markdown, Extension
from markdown.inlinepatterns import NOIMG, InlineProcessor

import re
import xml.etree.ElementTree as etree
from typing import Any

class CrossRefInlineProcessor(InlineProcessor):
    RE_ONEREF = re.compile(r'^(?P<prefix>[^@]*)@(?P<type>[\w]+):(?P<tag>[\w-]+)$')

    types = ['fig', 'eq', 'tbl', 'lst', 'sec']
    prefixes = {}
    group_delim = '; '
    ref_delim = ', '
    enable_ref_group = False
    enable_ref_number = False
    remove_ref_types = []
    
    def __init__(self, pattern: str, md: Markdown, config: dict[str, Any]):
        super().__init__(pattern, md)
        self.applyConfig(config)
        
    def applyConfig(self, config: dict[str, Any]):
        for one_type in self.types:
            if one_type == 'eq':
                config_name = f'eqnPrefix'
            else:
                config_name = f'{one_type}Prefix'

            this_prefix = config[config_name]

            if isinstance(this_prefix, list):
                self.prefixes[one_type] = this_prefix
            elif isinstance(this_prefix, str):
                self.prefixes[one_type] = [this_prefix, this_prefix]
            else:
                raise TypeError(f"{one_type}Prefix must be a string or a list")

        self.ref_delim = config['refDelim']
        if not isinstance(self.ref_delim, str):
            raise TypeError("refDelim must be a string")

        self.group_delim = config['groupDelim']
        if not isinstance(self.group_delim, str):
            raise TypeError("groupDelim must be a string")

        self.enable_ref_group = config['enable_ref_group']
        if not isinstance(self.enable_ref_group, bool):
            raise TypeError("enable_ref_group must be a boolean")

        self.enable_ref_number = config['enable_ref_number']
        if not isinstance(self.enable_ref_number, bool):
            raise TypeError("enable_ref_number must be a boolean")

        self.remove_ref_types = config['remove_ref_types']
        if not isinstance(self.remove_ref_types, list):
            raise TypeError("remove_ref_types must be a list")


    def handleOneRef(self, text: str) -> tuple[str, str, str, int, bool]:
        m = self.RE_ONEREF.match(text)
        if not m:
            return '', '', '', 0, False
        
        ref_type = m.group('type')
        prefix = m.group('prefix').strip()
        tag = m.group('tag')
        id = f'{ref_type}:{tag}'
        num = 0 # For future use

        if ref_type not in self.types:
            return '', '', '', 0, False
        
        return ref_type, prefix, id, num, True


    def getPrefixText(self, prefix: str, ref_type: str, isPlural: bool) -> str:
        if prefix == '':
            if isPlural > 1:
                return self.prefixes[ref_type][1] + ' '
            else:
                return self.prefixes[ref_type][0] + ' '
        elif prefix == '-':
            return ''
        else:
            return prefix.strip() + ' '


    def makeLinkTag(self, href: str, text: str) -> etree.Element:
        el = etree.Element('a')
        el.set('href', href.strip())
        el.text = text.strip()
        return el


    def handleMatch(self, m, data):
        origin_refs = m.group(1).split(';')

        refs = {}

        for ref in origin_refs:
            ref_type, prefix, id, num, handled = self.handleOneRef(ref.strip())
            if not handled:
                return None, None, None
            
            if ref_type not in refs:
                refs[ref_type] = {}
            if prefix not in refs[ref_type]:
                refs[ref_type][prefix] = []

            refs[ref_type][prefix].append((id, num))

        span = etree.Element('span')
        first_el = etree.Element('span')
        first_el.tail = ''
        last_el = first_el

        for ref_type, prefix_refs in refs.items():
            if ref_type in self.remove_ref_types:
                continue

            for prefix, refs in prefix_refs.items():

                if self.enable_ref_group:
                    last_el.tail += self.getPrefixText(prefix, ref_type, len(refs) > 1)

                for id, num in refs:
                    link_text = []
                    if not self.enable_ref_group:
                        prefix_text = self.getPrefixText(prefix, ref_type, 0)
                        link_text.append(f'{prefix_text}')
                    if self.enable_ref_number:
                        link_text.append(f'{num}')

                    last_el = self.makeLinkTag(f'#{id}', ' '.join(link_text))

                    last_el.tail = self.ref_delim
                    span.append(last_el)
                
                last_el.tail = self.group_delim

        last_el.tail = ''
        span.text = first_el.tail

        return span, m.start(0), m.end(0)


class CrossRefExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'enable_ref_group' : [
                False,
                'If true, the references will be grouped by their types, e.g., "figs. 1, 2, 3";'
                'if false, the references will be separated by their types, e.g., "fig. 1, fig. 2, fig. 3"'
            ],
            'enable_ref_number' : [
                False, 
                'If true, the references will include their numbers, e.g., "fig. 1"'
                'If false, the references will not include their numbers, e.g., "fig."'
            ],
            'figPrefix': [
                ['fig.', 'figs.'],
                'Prefix for figure references'
            ],
            'eqnPrefix': [
                ['eq.', 'eqns.'],
                'Prefix for equation references'
            ],
            'tblPrefix': [
                ['tbl.', 'tbls.'],
                'Prefix for table references'
            ],
            'lstPrefix': [
                ['lst.', 'lsts.'],
                'Prefix for listing references'
            ],
            'secPrefix': [
                ['sec.', 'secs.'],
                'Prefix for section references'
            ],
            'refDelim': [
                ', ',
                'Delimiter for multiple references'
            ],
            'groupDelim': [
                ', ',
                'Delimiter for multiple reference groups'
            ],
            'remove_ref_types': [
                [],
                'List of types of references to be removed'
            ]
        }
        super().__init__(**kwargs)


    def extendMarkdown(self, md):
        CROSSREF_RE = NOIMG + r'\[([^\]]*)\]'
        md.inlinePatterns.register(CrossRefInlineProcessor(CROSSREF_RE, md, self.getConfigs()), 'crossref', 124)


def makeExtension(**kwargs):
    return CrossRefExtension(**kwargs)

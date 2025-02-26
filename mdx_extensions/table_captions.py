from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.extensions.attr_list import AttrListTreeprocessor, AttrListExtension

from typing import Any
from markdown import Markdown
from xml.etree.ElementTree import Element

class TableCaptionTreeProcessor(Treeprocessor):
    def __init__(self, md: Markdown, config: dict[str, Any]):
        super().__init__(md)
        self.config = config
        self.checked_for_deps = False
        self.use_attr_list = False
        self.attr_list_processor = AttrListTreeprocessor(md)
    
    def isTable(self, elem: Element):
        return elem.tag == 'table' and not any(child.tag == 'caption' for child in elem)

    def isTableCaption(self, elem: Element):
        return elem.tag == 'p' and elem.text and elem.text.strip().startswith(('Table:', 'table:', ':'))
    
    def getCaptionAndAttrs(self, elem: Element):
        caption_text = elem.text.strip().split(':', 1)[1].strip()
        attrs_string = ''

        if self.use_attr_list and caption_text.endswith('}'):
            attrs_start = caption_text.rfind('{')
            if attrs_start != -1:
                attrs_string = caption_text[attrs_start + 1 : -1]
                caption_text = caption_text[:attrs_start].strip()

        return (caption_text, attrs_string)

    
    def insertCaptionToTable(self, table: Element, caption: Element):
        caption_text, attrs_string = self.getCaptionAndAttrs(caption)

        if caption_text:
            caption = Element('caption')
            caption.text = caption_text
            table.insert(0, caption)

        if self.use_attr_list and attrs_string:
            self.attr_list_processor.assign_attrs(table, attrs_string)


    def run(self, doc: Element) -> None:
        # Check for dependent extensions
        if not self.checked_for_deps:
            for ext in self.md.registeredExtensions:
                if isinstance(ext, AttrListExtension):
                    self.use_attr_list = True

            self.checked_for_deps = True
        
        need_to_remove = []

        last_is_caption = False
        last_is_table = False
        last_elem = None

        for elem in doc:
            if self.isTableCaption(elem):
                if last_is_table:
                    self.insertCaptionToTable(last_elem, elem)
                    need_to_remove.append(elem)

                    last_elem = None
                    last_is_caption = False
                    last_is_table = False

                else:
                    last_elem = elem
                    last_is_caption = True
                    last_is_table = False

            elif self.isTable(elem):
                if last_is_caption:
                    self.insertCaptionToTable(elem, last_elem)
                    need_to_remove.append(last_elem)

                    last_elem = None
                    last_is_caption = False
                    last_is_table = False

                else:
                    last_elem = elem
                    last_is_caption = False
                    last_is_table = True

            else:
                last_elem = None
                last_is_caption = False
                last_is_table = False
        
        for elem in need_to_remove:
            doc.remove(elem)


class TableCaptionExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(TableCaptionTreeProcessor(md, self.getConfigs()), 'table_captions', 25)

def makeExtension(**kwargs):
    return TableCaptionExtension(**kwargs)

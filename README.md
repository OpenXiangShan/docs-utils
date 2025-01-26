# Utility for XiangShan Document

This repository contains the utilities and resources needed to build XiangShan's standardized Document.

## Contents

### Pandoc building environment dependency script

The script `dependency.sh` sets up the environment for pandoc builds.

- [Pandoc](https://pandoc.org/) and its filters:
  - [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) with corresponding version
  - [include-files](https://github.com/pandoc-ext/include-files)
- [TinyTeX](https://yihui.org/tinytex/) and some LaTeX Package:
  - ctex, setspace, subfig, caption, textpos
- Fonts:
  - [Source Han Sans](https://github.com/adobe-fonts/source-han-sans/)
- Other dependencies:
  - librsvg2-bin for SVG processing

### Dockerfile

The `Dockerfile` is used to build the environment for pandoc builds.

Usage:
```bash
docker run --rm -it \
  -v $(pwd):/work \
  ghcr.io/openxiangshan/docs-utils:latest \
  make
```

### Pandoc Template

Customized pandoc templates for HTML and LaTeX.

### Pandoc Lua filters

All Pandoc [Lua filters](https://pandoc.org/lua-filters.html) are located in `pandoc_filters`.

- `remove_md_links.lua`:
  
  Remove links pointing to Markdown files (*.md), which is useful for one-file project.

- `replace_variables.lua`:

  Replace placeholders (e.g. `{{foo}}`) in Markdown with their corresponding value (e.g. `bar`) defined in metadata.

  Example of metadata yaml:

  ```yaml
  replace_variables:
    foo: bar
  ```

- `svg_to_pdf.lua`:
  
  Change referenced SVG format images to their corresponding PDF format images, which is useful for LaTeX builds.

### MkDocs building environment requirements

The script `requirements.txt` defines requirements for MkDocs building.

- [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/)
- Python-Markdown extensions:
  - [markdown_grid_tables](https://gitlab.com/WillDaSilva/markdown_grid_tables)
  - [markdown_captions](https://github.com/evidlo/markdown_captions)
  - [caption](https://github.com/flywire/caption)
  - The following Python-Markdown extensions

### Python-Markdown extensions

All Python-Markdown [extensions](https://python-markdown.github.io/extensions/) are located in `mdx_extensions` folder and used in MkDocs builds.

- `remove_include.py`:

  Remove Pandoc [include-files](https://github.com/pandoc-ext/include-files) style include code blocks.

      ``` {.include}
      file1.md
      file2.md
      ```

- `remove_references.py`: 

  Remove Pandoc [crossref](https://github.com/lierdakil/pandoc-crossref) with corresponding version style reference label like `[@sec:foobar]`


- `replace_variables.py`: 
  
  Replace placeholders (e.g. `{{foo}}`) in Markdown with their corresponding value (e.g. `bar`) defined in extension config.

  Example of `mkdocs.yml`:

  ```yaml
  markdown_extensions:
    - xiangshan_docs_utils.replace_variables:
        variables:
          foo: "bar"
  ```

### Resources

- SVG and PDF format Logos of BOSC and XiangShan Community.
  
  These logos are all right reserved, and may not be used without permission.

## LICENSE

This project is licensed under Mulan PSL v2 License, unless otherwise specified.

Copyright © 2024 The XiangShan Team, Beijing Institute of Open Source Chip


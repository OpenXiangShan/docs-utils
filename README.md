# Utility for XiangShan Document

This repository contains the utilities and resources needed to build XiangShan's standardized Document.

## Contents

### Pandoc building environment dependency script

The script `dependency.sh` sets up the environment for pandoc builds.

- [Pandoc](https://pandoc.org/) and its filters:
  - [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) with corresponding version
  - [include-files](https://github.com/pandoc-ext/include-files)
- [TinyTeX](https://yihui.org/tinytex/) and some LaTeX Package:
  - ctex, setspace, subfig, caption, textpos, tocloft, titlesec
- Fonts:
  - [Source Han Serif](https://github.com/adobe-fonts/source-han-serif/)
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

### MkDocs general config

The yaml file `mkdocs-base.yml` defines the general configurations of MkDocs, and is recommended to be `INHERIT` by `mkdocs.yml`.

```
INHERIT: utils/mkdocs-base.yml
site_name: Your Site Name
# ...
```

### MkDocs building environment requirements

The script `requirements.txt` defines requirements for MkDocs building.

- [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/)
- Python-Markdown extensions:
  - [markdown_grid_tables](https://gitlab.com/WillDaSilva/markdown_grid_tables)
  - [markdown_captions](https://github.com/evidlo/markdown_captions)
  - The following Python-Markdown extensions

### Mkdocs-Material Customization

All customizations to the Mkdocs-Material theme are located in the `custom_theme` directory. Add the following config into `mkdocs.yml` to use it:

```yml
theme:
  custom_dir: utils/custom_theme
```

- Additional CSS `assets/stylesheets/`
  - `table_fix.css`: fixes the display of table caption. See [squidfunk/mkdocs-material#7889](https://github.com/squidfunk/mkdocs-material/issues/7889).

- Additional JavaScript `assets/javascripts/`
  - `mathjax.js`: Enables MathJax support.
  - `readthedocs.js`: Enable ReadTheDocs Version Addon, see details below.

- Overide Partials `partials/`
  - `alternate.html`: Enables [stay-on-page](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#stay-on-page-insiders) feature for language selector.

- ReadTheDocs Version Addon: integrate the Read the Docs version menu into the site navigation
  - Using block override `main.html` to add additional meta and javascript.
  - Add the following config to mkdocs.yml:

    ```yml
    extra:
      readthedocs_version: true
    ```

### Python-Markdown extensions

All Python-Markdown [extensions](https://python-markdown.github.io/extensions/) are located in `mdx_extensions` folder and used in MkDocs builds.

- `remove_include.py`:

  Remove Pandoc [include-files](https://github.com/pandoc-ext/include-files) style include code blocks.

      ``` {.include}
      file1.md
      file2.md
      ```

- `remove_references.py`: 

  Remove [Pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)-style reference label like `[@sec:foobar]`


- `replace_variables.py`: 
  
  Replace placeholders (e.g. `{{foo}}`) in Markdown with their corresponding value (e.g. `bar`) defined in extension config or a yaml file.

  Example of `mkdocs.yml`:

  ```yaml
  markdown_extensions:
    - xiangshan_docs_utils.replace_variables:
        yaml_file: variables.yml
        variables:
          foo: "bar"
  ```

- `table_captions.py`:

  Support pandoc-style [table captions](https://pandoc.org/MANUAL.html#extension-table_captions) with attribute lists.

  ```
  Table: This is a Table {#tbl:example-table}

  | Col1 | Col2 |
  |------|------|
  |  11  |  22  |
  ```

- `crossref.py`:
  
  Supports [pandoc-crossref](https://lierdakil.github.io/pandoc-crossref/) style cross-reference syntax, e.g., `[@fig:figure1]`.

  Features:

  - [x] Generate in-page links for `[@fig:figure1]`, etc.
  - [x] Remove certain types of cross-references
  - [ ] Support numbering of figures and tables
  - [ ] Interact with figure/table caption extensions
  - [ ] Cross-page references

### Resources

- SVG and PDF format Logos of BOSC and XiangShan Community.
  
  These logos are all right reserved, and may not be used without permission.

## LICENSE

This project is licensed under Mulan PSL v2 License, unless otherwise specified.

Copyright © 2024 The XiangShan Team, Beijing Institute of Open Source Chip


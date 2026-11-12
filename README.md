# Utility for XiangShan Document

English | [简体中文](README.zh.md)

This repository contains the utilities and resources needed to build XiangShan's standardized Document.

XiangShan's standardized documentation uses [Copier](https://copier.readthedocs.io/) to manage documentation repository structure and resources, [MkDocs](https://www.mkdocs.org/) and [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/) to build documentation websites, and [Pandoc](https://pandoc.org/) and LaTeX to build PDFs.

## Documentation repository Copier template

[Copier](https://copier.readthedocs.io/) manages documentation repository templates and keeps downstream repositories in sync with template changes. The Copier template is located in the `template` directory.

Create a documentation repository from the template with:

```bash
copier copy --vcs-ref=master \
  https://github.com/OpenXiangShan/docs-utils.git \
  my-documentation
```

From a clean working tree in the downstream repository, update the template with:

```bash
copier update --vcs-ref=master
```

The template includes a GitHub Actions workflow that checks for template changes each week and opens or updates a draft PR when there are changes.

## Pandoc and LaTeX toolchain

### Dependency installation script

The script `dependency.sh` sets up the environment for Pandoc and LaTeX builds.

- [Pandoc](https://pandoc.org/) and its filters:
  - [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) with corresponding version
- [TinyTeX](https://yihui.org/tinytex/) and some LaTeX Package:
  - ctex, setspace, subfig, caption, textpos, tocloft, titlesec
- Fonts:
  - [Source Han Serif](https://github.com/adobe-fonts/source-han-serif/)
  - [Source Han Sans](https://github.com/adobe-fonts/source-han-sans/)
- Other dependencies:
  - librsvg2-bin for SVG processing

### Dockerfile

The `Dockerfile` is used to build the environment for pandoc builds.

Run this command from the root of the downstream documentation repository:

```bash
docker run --rm -it \
  -v $(pwd):/work \
  ghcr.io/openxiangshan/docs-utils:latest \
  make
```

### Pandoc Template

The customized LaTeX template is located in `template/tools/pandoc/template.tex`.

### Pandoc Lua filters

All Pandoc [Lua filters](https://pandoc.org/lua-filters.html) are located in `pandoc_filters`.

- `include-files.lua`:

  [pandoc-ext/include-files](https://github.com/pandoc-ext/include-files), licensed under MIT.

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

## MkDocs toolchain

### MkDocs general config

The templates `template/mkdocs-en.yml.jinja` and `template/mkdocs-zh.yml.jinja` generate complete MkDocs configurations. `mkdocs.yml` selects the language using `MKDOCS_YML_FILE`, defaulting to Chinese.

Maintain `nav` in each generated language file.

### MkDocs building environment requirements

The file `template/requirements.txt` defines requirements for MkDocs building, and is copied to `requirements.txt` in each document repository.

- [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/)
- Python-Markdown extensions:
  - [markdown_grid_tables](https://gitlab.com/WillDaSilva/markdown_grid_tables)
  - [markdown_captions](https://github.com/evidlo/markdown_captions)
  - The following Python-Markdown extensions

### Mkdocs-Material Customization

All customizations to the MkDocs-Material theme are located in the `template/tools/mkdocs_theme` directory. Add the following to `mkdocs.yml` to enable them:

```yml
theme:
  custom_dir: tools/mkdocs_theme
```

- Additional CSS `assets/stylesheets/`
  - `table_fix.css`: fixes the display of table caption. See [squidfunk/mkdocs-material#7889](https://github.com/squidfunk/mkdocs-material/issues/7889).

- Additional JavaScript `assets/javascripts/`
  - `mathjax.js`: Enables MathJax support.
  - `readthedocs.js`: Enable ReadTheDocs Version Addon, see details below.

- Override Partials `partials/`
  - `alternate.html`: Enables [stay-on-page](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#stay-on-page-insiders) feature for language selector.

  - `header.html`: Add a back-to-home button. 

    ```yml
    extra:
      back_to_home:
        url: https://docs.xiangshan.cc/
        # icon: material/home    # Optional
        # title: Back to home    # Optional
    ```

- ReadTheDocs Version Addon: integrate the Read the Docs version menu into the site navigation
  - Using block override `main.html` to add additional meta and javascript.
  - Add the following config to `mkdocs.yml`:

    ```yml
    extra:
      readthedocs_version: true
    ```

### Python-Markdown extensions

All Python-Markdown [extensions](https://python-markdown.github.io/extensions/) are located in the `mdx_extensions` directory and used in MkDocs builds. Install them with:

```bash
pip install git+https://github.com/OpenXiangShan/docs-utils.git
```

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
    - replace_variables:
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

## Other resources

- `figs/`: BOSC and XiangShan Community logos in SVG and PDF formats.
  
  All rights to these logos are reserved; they may not be used without permission.

## LICENSE

This project is licensed under Mulan PSL v2 License, unless otherwise specified.

Copyright © 2024 The XiangShan Team, Beijing Institute of Open Source Chip


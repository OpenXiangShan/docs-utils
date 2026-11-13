# 香山文档工具

[English](README.md) | 简体中文

本仓库包含构建香山标准化文档所需的工具与资源。

香山标准化文档使用 [Copier](https://copier.readthedocs.io/) 管理文档仓库架构和资源，使用 [MkDocs](https://www.mkdocs.org/) 和 [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/) 构建文档网站，使用 [Pandoc](https://pandoc.org/) 和 LaTeX 构建 PDF。

## 文档仓库 Copier 模板

[Copier](https://copier.readthedocs.io/) 用于管理文档仓库模板，并在模板更新后同步下游仓库，使其持续跟进模板变更。Copier 模板位于 `template` 目录。

使用以下命令从模板创建文档仓库：

```bash
copier copy --vcs-ref=master \
  https://github.com/OpenXiangShan/docs-utils.git \
  my-documentation
```

在下游仓库中，确保工作区干净，然后运行以下命令更新模板：

```bash
copier update --vcs-ref=master
```

模板中包含 GitHub Actions workflow，每周检查模板变更，并在有变更时创建或更新草稿 PR。

## Pandoc 和 LaTeX 工具链

### 依赖安装脚本

`dependency.sh` 脚本用于配置 Pandoc 和 LaTeX 构建环境。

- [Pandoc](https://pandoc.org/) 及其过滤器：
  - 与 Pandoc 版本对应的 [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)
- [TinyTeX](https://yihui.org/tinytex/) 及部分 LaTeX 宏包：
  - ctex、setspace、subfig、caption、textpos、tocloft、titlesec
- 字体：
  - [思源宋体](https://github.com/adobe-fonts/source-han-serif/)
  - [思源黑体](https://github.com/adobe-fonts/source-han-sans/)
- 其他依赖：
  - librsvg2-bin，用于处理 SVG

### Dockerfile

`Dockerfile` 用于构建 Pandoc 构建环境。

在下游文档仓库根目录运行：

```bash
docker run --rm -it \
  -v $(pwd):/work \
  ghcr.io/openxiangshan/docs-utils:latest \
  make
```

### Pandoc 模板

自定义 LaTeX 模板位于 `template/tools/pandoc/template.tex`。

### Pandoc Lua 过滤器

所有 Pandoc [Lua 过滤器](https://pandoc.org/lua-filters.html)均位于 `pandoc_filters`。

- `include-files.lua`：

  [pandoc-ext/include-files](https://github.com/pandoc-ext/include-files)，MIT 许可证。

- `remove_md_links.lua`：

  移除指向 Markdown 文件（*.md）的链接，适用于生成单文件文档的项目。

- `replace_variables.lua`：

  将 Markdown 中的占位符（如 `{{foo}}`）替换为元数据中定义的对应值（如 `bar`）。

  元数据 YAML 示例：

  ```yaml
  replace_variables:
    foo: bar
  ```

- `svg_to_pdf.lua`：

  将引用的 SVG 图片改为对应的 PDF 图片，适用于 LaTeX 构建。

## MkDocs 工具链

### MkDocs 通用配置

`template/mkdocs-en.yml.jinja` 和 `template/mkdocs-zh.yml.jinja` 模板用于生成完整的 MkDocs 配置。`mkdocs.yml` 通过 `MKDOCS_YML_FILE` 选择语言，默认为中文。

在生成的各语言配置文件中维护 `nav`。

### MkDocs 构建环境依赖

`template/requirements.txt` 定义了 MkDocs 构建所需的依赖，生成文档仓库时会复制到根目录的 `requirements.txt`。

- [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/)
- Python-Markdown 扩展：
  - [markdown_grid_tables](https://gitlab.com/WillDaSilva/markdown_grid_tables)
  - [markdown_captions](https://github.com/evidlo/markdown_captions)
  - 下文介绍的 Python-Markdown 扩展

### MkDocs-Material 自定义主题

对 MkDocs-Material 主题的所有自定义内容均位于 `template/tools/mkdocs_theme` 目录。在 `mkdocs.yml` 中加入以下内容以启用：

```yml
theme:
  custom_dir: tools/mkdocs_theme
```

- 附加 CSS `assets/stylesheets/`
  - `table_fix.css`：修正表格标题的显示，参见 [squidfunk/mkdocs-material#7889](https://github.com/squidfunk/mkdocs-material/issues/7889)。

- 附加 JavaScript `assets/javascripts/`
  - `mathjax.js`：启用 MathJax 支持。
  - `readthedocs.js`：启用 Read the Docs 版本插件，详见下文。

- 覆盖局部模板 `partials/`
  - `alternate.html`：为语言选择器启用[切换语言时保留当前页面](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#stay-on-page-insiders)的功能。

  - `header.html`：添加返回首页的按钮。

    ```yml
    extra:
      back_to_home:
        url: https://docs.xiangshan.cc/
        # icon: material/home    # Optional
        # title: Back to home    # Optional
    ```

- Read the Docs 版本插件：将 Read the Docs 版本菜单集成到站点导航中。
  - 通过覆盖 `main.html` 中的块添加额外的 meta 和 JavaScript。
  - 在 `mkdocs.yml` 中添加以下配置：

    ```yml
    extra:
      readthedocs_version: true
    ```

### Python-Markdown 扩展

所有 Python-Markdown [扩展](https://python-markdown.github.io/extensions/)均位于 `mdx_extensions` 目录，用于 MkDocs 构建。通过以下命令安装：

```bash
pip install git+https://github.com/OpenXiangShan/docs-utils.git
```

- `remove_include.py`：

  移除 Pandoc [include-files](https://github.com/pandoc-ext/include-files) 风格的文件包含代码块。

      ``` {.include}
      file1.md
      file2.md
      ```

- `remove_references.py`：

  移除 [Pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) 风格的引用标记，如 `[@sec:foobar]`。

- `replace_variables.py`：

  将 Markdown 中的占位符（如 `{{foo}}`）替换为扩展配置或 YAML 文件中定义的对应值（如 `bar`）。

  `mkdocs.yml` 示例：

  ```yaml
  markdown_extensions:
    - replace_variables:
        yaml_file: variables.yml
        variables:
          foo: "bar"
  ```

- `table_captions.py`：

  支持带属性列表的 Pandoc 风格[表格标题](https://pandoc.org/MANUAL.html#extension-table_captions)。

  ```
  Table: This is a Table {#tbl:example-table}

  | Col1 | Col2 |
  |------|------|
  |  11  |  22  |
  ```

- `crossref.py`：

  支持 [pandoc-crossref](https://lierdakil.github.io/pandoc-crossref/) 风格的交叉引用语法，如 `[@fig:figure1]`。

  功能：

  - [x] 为 `[@fig:figure1]` 等引用生成页内链接
  - [x] 移除指定类型的交叉引用
  - [ ] 支持图表编号
  - [ ] 与图表标题扩展联动
  - [ ] 跨页面引用

## 其他资源

- `figs/`：BOSC 和香山社区的 SVG、PDF 格式 Logo。

  这些 Logo 保留所有权利，未经许可不得使用。


## 许可证

除非另有说明，本项目采用 Mulan PSL v2 许可证。

Copyright © 2024 The XiangShan Team, Beijing Institute of Open Source Chip

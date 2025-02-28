import markdown
from utils.mdx_extensions.crossref import CrossRefExtension

def test_crossref():
    test_cases = [
        "This is a reference to [@fig:example1].",
        "This is a reference to [@fig:example1] and another to [@tbl:example2].",
        "Multiple references [@fig:example1;@sec:example3].",
        "Multiple references [@fig:example1;@fig:example2;@fig:example3].",
        "Multiple references [@fig:example1;@fig:example2;@sec:example3;@fig:example2].",
        "No prefix reference [-@fig:example1].",
        "Invalid reference [@invalid:example].",
        "with prefix verbatim [Prefix @fig:1].",
        "In citation group, citations with the same prefix will be grouped [A @fig:1; A @fig:2; B @fig:3].",
        "It can be used to an advantage [Appendices @sec:A1; Appendices @sec:A2; Appendices @sec:A3]."
    ]

    md = markdown.Markdown(
        extensions=[
            CrossRefExtension(
                enable_ref_group=False,
                enable_ref_number=False,
                figPrefix='此图',
                tblPrefix='此表',
                secPrefix='此节',
                refDelim='、',
                groupDelim='、',
                remove_ref_types=['sec'],
            )
        ]
    )

    for text in test_cases:
        print(text)
        print("-" * 40)
        html = md.convert(text)
        print(html)
        print("=" * 40)

if __name__ == "__main__":
    test_crossref()

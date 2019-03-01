#!/usr/bin/env python
"""
Demonstration of how to print using the HTML class.
"""
from __future__ import unicode_literals, print_function
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import default_ui_style, default_pygments_style, BaseStyle, merge_styles
from prompt_toolkit.styles import Style

print = print_formatted_text


def title(text):
    print(HTML('\n<u><b>{}</b></u>').format(text))


def main():
    title('Special formatting')
    print(HTML('    <b>Bold</b>'))
    print(HTML('    <blink>Blink</blink>'))
    print(HTML('    <i>Italic</i>'))
    print(HTML('    <reverse>Reverse</reverse>'))
    print(HTML('    <u>Underline</u>'))
    print(HTML('    <hidden>Hidden</hidden> (hidden)'))

    # Ansi colors.
    title('ANSI colors')

    print(HTML('    <ansired>ANSI Red</ansired>'))
    print(HTML('    <ansiblue>ANSI Blue</ansiblue>'))

    # Other named colors.
    title('Named colors')

    print(HTML('    <orange>orange</orange>'))
    print(HTML('    <purple>purple</purple>'))

    # Background colors.
    title('Background colors')

    print(HTML('    <style fg="ansiwhite" bg="ansired">ANSI Red</style>'))
    print(HTML('    <style fg="ansiwhite" bg="ansiblue">ANSI Blue</style>'))

    # Interpolation.
    title('HTML interpolation (see source)')

    print(HTML('    <i>{}</i>').format('<test>'))
    print(HTML('    <b>{text}</b>').format(text='<test>'))
    print(HTML('    <u>%s</u>') % ('<text>', ))

    print()

    style = Style.from_dict({
            'hello': '#ff0066',
            'world': '#884444 italic',
        })

    print_formatted_text(HTML('<hello>Hello</hello> <world>world</world>!'), style=style)
if __name__ == '__main__':
    main()
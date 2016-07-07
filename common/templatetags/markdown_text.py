import re
import bleach

from django import template
from markdown import markdown as md
from wiki.etc import generate_article_link

register = template.Library()

ALLOWED_TAGS = (bleach.ALLOWED_TAGS +
                ['p', 'table', 'tr', 'td', 'th', 'thead', 'tbody'] +
                ['h' + str(i + 1) for i in range(6)])

@register.filter(name='mdtext')
def mdtext(text):
    mdbody = re.sub(
        '\\[\\[(.*?)\\]\\]',
        lambda match: generate_article_link(match.group(1)),
        text
        )

    mdbody = md(
        mdbody,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.footnotes'
        ],
        output_format='html5'
        )

    return bleach.clean(
        mdbody,
        tags=ALLOWED_TAGS
        )

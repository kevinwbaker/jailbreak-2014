from django import template

register = template.Library()

@register.filter(name='unescape')
def html_decode(s):
    '''
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    '''
    html_codes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in html_codes:
        s = s.replace(code[1], code[0])
    return s
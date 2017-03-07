#encoding: utf-8
''' from snippet http://djangosnippets.org/snippets/1259/ '''
from django import template

register = template.Library()

@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    # Make sure it's unicode
    value = unicode(value)
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    # Cut the string
    value = value[:limit]
    
    # Break into words and remove the last  
    words = value.split(' ')
    
    # Join the words and return
    return ' '.join(words) + '...'


@register.filter
def cap_name(value):
    namelist = unicode(value).split(' ');
    fixed = ''
    for name in namelist:
        name = name.lower()
        if name != 'de' and name != 'da' and name != 'das' and name != 'do'\
                    and name != 'dos' and name != 'di' and name !='e' :
            fixed += name.capitalize() + ' '
        else:
            fixed += name + ' '
                
    return fixed

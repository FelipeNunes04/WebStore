from django import template
import re

register = template.Library()


@register.filter
def youtubize(value, args):
    """
    Converts http:// links to youtube into youtube-embed statements, so that
    one can provide a simple link to a youtube video and this filter will
    embed it.

    Based on the Django urlize filter.
    """
    text = value
    args = args.split('x')
    # Configuration for urlize() function
    LEADING_PUNCTUATION = ['(', '<', '&lt;', '.', ',', ')', '>', '\n', '&gt;', '&nbsp;']
    TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;', '(', '<', '&lt;', '&nbsp;']
    word_split_re = re.compile(r'([\w./:?=-]+)')
    punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
            ('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
            '|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
    youtube_re1 = re.compile('http://www.youtube.com/watch.v=(?P<videoid>(.+))')
    youtube_re2 = re.compile('http://youtube.com/watch.v=(?P<videoid>(.+))')
    vimeo_re1 = re.compile('http://www.vimeo.com/(?P<videoid>(\d+))')
    vimeo_re2 = re.compile('http://vimeo.com/(?P<videoid>(\d+))')

    words = word_split_re.split(text)
    for i, word in enumerate(words):
        match = punctuation_re.match(word)
        if match:
            lead, middle, trail = match.groups()
            if middle.startswith('http://www.youtube.com/watch') or\
                            middle.startswith('http://youtube.com/watch'):
                video_match = youtube_re1.match(middle)
                if not video_match:
                    video_match = youtube_re2.match(middle)
                if video_match:
                    video_id = video_match.groups()[1]
                    middle = '''<object width="%s" height="%s">
      <param name="movie" value="http://www.youtube.com/v/%s"/>
      <param name="wmode" value="transparent"/>
      <embed src="http://www.youtube.com/v/%s?wmode=opaque" type="application/x-shockwave-flash" wmode="transparent" width="%s" height="%s"/>
    </object>''' % (args[0], args[1], video_id, video_id, args[0], args[1])
            elif middle.startswith('http://www.vimeo.com') or\
                                        middle.startswith('http://vimeo.com'):
                video_match = vimeo_re1.match(middle)
                if not video_match:
                    video_match = vimeo_re2.match(middle)
                if video_match:
                    video_id = video_match.groups()[1]
                    middle = '''
    <embed src="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=0&amp;show_byline=0&amp;show_portrait=0&amp;color=00ADEF&amp;fullscreen=0&amp;autoplay=0&amp;loop=0"
    type="application/x-shockwave-flash"
    allowfullscreen="true"
    allowscriptaccess="always" width="%s" height="%s"/>
    ''' % (video_id, args[0], args[1])
            if lead + middle + trail != word:
                words[i] = lead + middle + trail
    return ''.join(words)




@register.filter
def youtubizeP(value):
    """
    Converts http:// links to youtube into youtube-embed statements, so that
    one can provide a simple link to a youtube video and this filter will
    embed it.

    Based on the Django urlize filter.
    """
    text = value
    # Configuration for urlize() function
    LEADING_PUNCTUATION  = ['(', '<', '&lt;','.', ',', ')', '>', '\n', '&gt;','&nbsp;']
    TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;','(', '<', '&lt;', '&nbsp;']
    word_split_re = re.compile(r'([\w./:?=-]+)')
    punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
            ('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
            '|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
    youtube_re1 = re.compile ('http://www.youtube.com/watch.v=(?P<videoid>(.+))')
    youtube_re2 = re.compile ('http://youtube.com/watch.v=(?P<videoid>(.+))')
    vimeo_re1 = re.compile ('http://www.vimeo.com/(?P<videoid>(\d+))')
    vimeo_re2 = re.compile ('http://vimeo.com/(?P<videoid>(\d+))')

    words = word_split_re.split(text)
    for i, word in enumerate(words):
        match = punctuation_re.match(word)
        if match:
            lead, middle, trail = match.groups()
            if middle.startswith('http://www.youtube.com/watch') or\
                            middle.startswith('http://youtube.com/watch'):
                video_match = youtube_re1.match(middle)
                if not video_match:
                    video_match = youtube_re2.match(middle)
                if video_match:
                    video_id = video_match.groups()[1]
                    middle = '''<object width="275" height="170">
      <param name="movie" value="http://www.youtube.com/v/%s"/>
      <param name="wmode" value="transparent"/>
      <embed src="http://www.youtube.com/v/%s" type="application/x-shockwave-flash" wmode="transparent" width="275" height="170"/>
    </object>''' % (video_id, video_id)
            elif middle.startswith('http://www.vimeo.com') or\
                                        middle.startswith('http://vimeo.com'):
                video_match = vimeo_re1.match(middle)
                if not video_match:
                    video_match = vimeo_re2.match(middle)
                if video_match:
                    video_id = video_match.groups()[1]
                    middle = '''
    <embed src="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=0&amp;show_byline=0&amp;show_portrait=0&amp;color=00ADEF&amp;fullscreen=0&amp;autoplay=0&amp;loop=0"
    type="application/x-shockwave-flash"
    allowfullscreen="true"
    allowscriptaccess="always" width="275" height="170"/>
    ''' % ( video_id)
            if lead + middle + trail != word:
                words[i] = lead + middle + trail

    return ''.join(words)

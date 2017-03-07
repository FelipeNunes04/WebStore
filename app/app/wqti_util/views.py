# coding: utf-8
from wqti_util.ajax_form_val import form_error_list
from wqti_util.decorators import ajax_required, post_required
from wqti_util.json import to_json_response


@ajax_required
@post_required
@to_json_response
def ajax_post_form_view(request, form_class):
    form = form_class(request.POST)
    
    if form.is_valid():
        form.save()
        r = {'ok': True}
    else:
        r = {'ok': False, 'errors': form_error_list(form)}
    
    return r
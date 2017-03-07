django.jQuery(document).ready(function($) {
    var orderstatus_set = $('[id^=orderstatus_set].has_original');
    orderstatus_set.each(function(index) {
        var $this = $(this);
        $this.find('input').attr('readonly', 'readonly');
        
        var $select = $this.find('select');
        $select.after('<p>' + $select.find('option:selected').text() + '</p>').hide();
    });
});

var menu = {
    init: function(){
        this.menu = $('#menu');
        $('dt', this.menu)
            .bind('mouseenter', $.proxy(this.show_submenu, this))
            .bind('mouseleave', $.proxy(this.hide_submenu, this));
        $('dd', this.menu)
            .bind('mouseleave', $.proxy(this.hide_submenu, this));
        this.menu
            .bind('mouseleave', $.proxy(this.hide_submenu, this));
    },
    show_submenu: function(e){
        var dt = $(e.currentTarget),
            dd = dt.next();
        dt.addClass('selected');
        $('dt:not(.selected) + dd', this.menu).hide();
        if(dd[0].tagName == 'DD'){
            dd.show();
            $(dd).css({'left': $(dd).prev()[0].offsetLeft, 'top':$(dd).prev()[0].offsetTop + 35});

        }
    },
    hide_submenu: function(e){
        var el = $(e.currentTarget);
        if(el[0].tagName == 'DD'){
            el.hide().prev().removeClass('selected');
        } else {
            if(el[0].tagName == 'DIV'){
                el.find('dd').hide().prev().removeClass('selected');
            }
            if(el.next()[0].tagName == 'DD'){
                el.removeClass('selected');
            }
        }
    }
};

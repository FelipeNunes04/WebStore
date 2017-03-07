/*
 * jQuery select replacement
 * http://crgdesign.com.br/blog/
 *
 * Copyright (c) 2009 Carlos Roberto Gomes Júnior
 * 
 * Version: 1.1
 */
(function() {

jQuery.fn.selectreplace = function(options) {

  settings = jQuery.extend({
     width: 220,
     borderSize:0,
     forceZindex:-1,
     float:'none',
     mouseOutClass:'msout',
     mouseOverClass:'msover',
     scrollAfter: 19,
     autoZindex:true,
     lastZindex:200
      }, options);
    
    /* TODO: marcar opção selecionada como citado em http://www.brainfault.com/2007/07/23/select-box-replacement/ */
    
  return this.each(function(){  
     
     var select_element = $(this), selected_text;
     //alert($(this).children("option[selected]").length);
     if($(this).children("option[selected]").length >0){
         selected_text = $(this).children("option[selected]").text();
     } else {
         selected_text = $(this).children("option:first").text();
     }
     
     var select_body = '<div class="selbox"><div class="selected"><a href="#" class="selected-focus">'+selected_text+'</a></div><ul></ul></div>';
          
     select_element.after(select_body).hide();
     
     var select = select_element.next(".selbox");
     var sel_option = select.children(".selected");
     
     if($.browser.msie && $.browser.version <= 6){
       sel_option.height(sel_option.innerHeight());
     } else {
       sel_option.height(sel_option.height());
     }
     
     var ul = select.children("ul");
     
     
     //modificacoes para Virtuallia
     select_element.bind('change', function(){
         selected_text = $(this).children("option[selected]").text();
         select.find('a.selected-focus').text(selected_text);
     });
     
     
     //select.css({border:"1px solid red"});
     //sel_option.css({border:"1px solid blue"});
     sel_option
     .addClass("msout")
     .hover(function(){
       $(this).addClass("msover").removeClass("msout");
     }, function(){
       $(this).addClass("msout").removeClass("msover");
     })
     .click(function(){
         if( ul.css('display') == 'none' ) {
           // $('.selbox ul').hide();
            ul
            .show()
            .children("li")
            .addClass("m_out")
            .removeClass("m_over")
            .eq(select_element.attr("selectedIndex"))
            .addClass("m_over")
            .removeClass("m_out");
         } else {
            ul.hide();
         }
         return false;
     });
     
     
     if($.browser.msie && $.browser.version <= 7){
      sel_option.css({display:'inline-block'});
     }
     
     var list = new Array();
     
     $(this).children().each(function(){
      if(this.nodeName == "OPTION"){
         list.push('<li>'+$(this).text()+'</li>');
      }
     });
     
     
     select.css({width:settings.width, float:settings.float});
     


     if(settings.autoZindex){
         var selboxObjects = $('.selbox');
         if(selboxObjects.length > 1) {
            selboxObjects.eq( selboxObjects.length - 1 ).css({zIndex:(settings.lastZindex - (selboxObjects.length - 1) )});
         } else {
           selboxObjects.eq(selboxObjects.length - 1).css({zIndex:settings.lastZindex});
         }
     }

     if(settings.forceZindex >= 0 ){
       select.css({zIndex:settings.forceZindex});
     }

     $("*").not(".selbox").click(function( e ){
       if( !e.target.className.match(/selected/) ) {
         ul.hide(); 
       }
     });
     
     ul
     .css({width:(settings.width - settings.borderSize), visibility:'hidden'})  
     .append(list.join(''));
     
      if(settings.scrollAfter > 0 && ul.find('li').length > settings.scrollAfter ){
         var hsum = 0;
         for(i=0; i < settings.scrollAfter; i++ ){
            hsum += ul.find('li').eq(i).innerHeight();
         }
         ul.addClass('scroll').height(hsum);
      }
      
      ul.css({visibility:'visible'})
      .hide();

     
     ul.children("li").click(function(){
        var index = ul.children().index(this);
        select_element.attr("selectedIndex", index);
        select_element.find('option:selected').removeAttr('selected');
        select_element.find('option').eq(index).attr('selected', 'selected');
        sel_option.children('.selected-focus').text($(this).text());
        ul.hide();
        select_element.trigger("change");
     })
     .css({position:'relative'})
     .hover(function(){
       $(this).addClass("m_over").removeClass("m_out");
     }, function(){
       $(this).addClass("m_out").removeClass("m_over");
     }).blur(function(){ $(this).addClass("m_out").removeClass("m_over"); });
  });
  
};

})(jQuery);
/*!
 * jCarousel - Riding carousels with jQuery
 *   http://sorgalla.com/jcarousel/
 *
 * Copyright (c) 2006 Jan Sorgalla (http://sorgalla.com)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 *
 * Built on top of the jQuery library
 *   http://jquery.com
 *
 * Inspired by the "Carousel Component" by Bill Scott
 *   http://billwscott.com/carousel/
 */

(function(i){i.fn.jcarousel=function(a){if(typeof a=="string"){var c=i(this).data("jcarousel"),b=Array.prototype.slice.call(arguments,1);return c[a].apply(c,b)}else return this.each(function(){i(this).data("jcarousel",new h(this,a))})};var p={vertical:false,rtl:false,start:1,offset:1,size:null,scroll:3,visible:null,animation:"normal",easing:"swing",auto:0,wrap:null,initCallback:null,reloadCallback:null,itemLoadCallback:null,itemFirstInCallback:null,itemFirstOutCallback:null,itemLastInCallback:null, itemLastOutCallback:null,itemVisibleInCallback:null,itemVisibleOutCallback:null,buttonNextHTML:"<div></div>",buttonPrevHTML:"<div></div>",buttonNextEvent:"click",buttonPrevEvent:"click",buttonNextCallback:null,buttonPrevCallback:null,itemFallbackDimension:null},q=false;i(window).bind("load.jcarousel",function(){q=true});i.jcarousel=function(a,c){this.options=i.extend({},p,c||{});this.locked=false;this.buttonPrev=this.buttonNext=this.list=this.clip=this.container=null;if(!c||c.rtl===undefined)this.options.rtl= (i(a).attr("dir")||i("html").attr("dir")||"").toLowerCase()=="rtl";this.wh=!this.options.vertical?"width":"height";this.lt=!this.options.vertical?this.options.rtl?"right":"left":"top";for(var b="",d=a.className.split(" "),e=0;e<d.length;e++)if(d[e].indexOf("jcarousel-skin")!=-1){i(a).removeClass(d[e]);b=d[e];break}if(a.nodeName.toUpperCase()=="UL"||a.nodeName.toUpperCase()=="OL"){this.list=i(a);this.container=this.list.parent();if(this.container.hasClass("jcarousel-clip")){if(!this.container.parent().hasClass("jcarousel-container"))this.container= this.container.wrap("<div></div>");this.container=this.container.parent()}else if(!this.container.hasClass("jcarousel-container"))this.container=this.list.wrap("<div></div>").parent()}else{this.container=i(a);this.list=this.container.find("ul,ol").eq(0)}b!=""&&this.container.parent()[0].className.indexOf("jcarousel-skin")==-1&&this.container.wrap('<div class=" '+b+'"></div>');this.clip=this.list.parent();if(!this.clip.length||!this.clip.hasClass("jcarousel-clip"))this.clip=this.list.wrap("<div></div>").parent(); this.buttonNext=i(".jcarousel-next",this.container);if(this.buttonNext.size()==0&&this.options.buttonNextHTML!=null)this.buttonNext=this.clip.after(this.options.buttonNextHTML).next();this.buttonNext.addClass(this.className("jcarousel-next"));this.buttonPrev=i(".jcarousel-prev",this.container);if(this.buttonPrev.size()==0&&this.options.buttonPrevHTML!=null)this.buttonPrev=this.clip.after(this.options.buttonPrevHTML).next();this.buttonPrev.addClass(this.className("jcarousel-prev"));this.clip.addClass(this.className("jcarousel-clip")).css({overflow:"hidden", position:"relative"});this.list.addClass(this.className("jcarousel-list")).css({overflow:"hidden",position:"relative",top:0,margin:0,padding:0}).css(this.options.rtl?"right":"left",0);this.container.addClass(this.className("jcarousel-container")).css({position:"relative"});!this.options.vertical&&this.options.rtl&&this.container.addClass("jcarousel-direction-rtl").attr("dir","rtl");var f=this.options.visible!=null?Math.ceil(this.clipping()/this.options.visible):null;b=this.list.children("li");var g= this;if(b.size()>0){var j=0;e=this.options.offset;b.each(function(){g.format(this,e++);j+=g.dimension(this,f)});this.list.css(this.wh,j+100+"px");if(!c||c.size===undefined)this.options.size=b.size()}this.container.css("display","block");this.buttonNext.css("display","block");this.buttonPrev.css("display","block");this.funcNext=function(){g.next()};this.funcPrev=function(){g.prev()};this.funcResize=function(){g.reload()};this.options.initCallback!=null&&this.options.initCallback(this,"init");if(!q&& i.browser.safari){this.buttons(false,false);i(window).bind("load.jcarousel",function(){g.setup()})}else this.setup()};var h=i.jcarousel;h.fn=h.prototype={jcarousel:"0.2.5"};h.fn.extend=h.extend=i.extend;h.fn.extend({setup:function(){this.prevLast=this.prevFirst=this.last=this.first=null;this.animating=false;this.tail=this.timer=null;this.inTail=false;if(!this.locked){this.list.css(this.lt,this.pos(this.options.offset)+"px");var a=this.pos(this.options.start);this.prevFirst=this.prevLast=null;this.animate(a, false);i(window).unbind("resize.jcarousel",this.funcResize).bind("resize.jcarousel",this.funcResize)}},reset:function(){this.list.empty();this.list.css(this.lt,"0px");this.list.css(this.wh,"10px");this.options.initCallback!=null&&this.options.initCallback(this,"reset");this.setup()},reload:function(){this.tail!=null&&this.inTail&&this.list.css(this.lt,h.intval(this.list.css(this.lt))+this.tail);this.tail=null;this.inTail=false;this.options.reloadCallback!=null&&this.options.reloadCallback(this);if(this.options.visible!= null){var a=this,c=Math.ceil(this.clipping()/this.options.visible),b=0,d=0;this.list.children("li").each(function(e){b+=a.dimension(this,c);if(e+1<a.first)d=b});this.list.css(this.wh,b+"px");this.list.css(this.lt,-d+"px")}this.scroll(this.first,false)},lock:function(){this.locked=true;this.buttons()},unlock:function(){this.locked=false;this.buttons()},size:function(a){if(a!=undefined){this.options.size=a;this.locked||this.buttons()}return this.options.size},has:function(a,c){if(c==undefined||!c)c= a;if(this.options.size!==null&&c>this.options.size)c=this.options.size;for(var b=a;b<=c;b++){var d=this.get(b);if(!d.length||d.hasClass("jcarousel-item-placeholder"))return false}return true},get:function(a){return i(".jcarousel-item-"+a,this.list)},add:function(a,c){var b=this.get(a),d=0,e=i(c);if(b.length==0){var f;b=this.create(a);for(var g=h.intval(a);f=this.get(--g);)if(g<=0||f.length){g<=0?this.list.prepend(b):f.after(b);break}}else d=this.dimension(b);if(e.get(0).nodeName.toUpperCase()=="LI"){b.replaceWith(e); b=e}else b.empty().append(c);this.format(b.removeClass(this.className("jcarousel-item-placeholder")),a);e=this.options.visible!=null?Math.ceil(this.clipping()/this.options.visible):null;d=this.dimension(b,e)-d;a>0&&a<this.first&&this.list.css(this.lt,h.intval(this.list.css(this.lt))-d+"px");this.list.css(this.wh,h.intval(this.list.css(this.wh))+d+"px");return b},remove:function(a){var c=this.get(a);if(!(!c.length||a>=this.first&&a<=this.last)){var b=this.dimension(c);a<this.first&&this.list.css(this.lt, h.intval(this.list.css(this.lt))+b+"px");c.remove();this.list.css(this.wh,h.intval(this.list.css(this.wh))-b+"px")}},next:function(){this.stopAuto();this.tail!=null&&!this.inTail?this.scrollTail(false):this.scroll((this.options.wrap=="both"||this.options.wrap=="last")&&this.options.size!=null&&this.last==this.options.size?1:this.first+this.options.scroll)},prev:function(){this.stopAuto();this.tail!=null&&this.inTail?this.scrollTail(true):this.scroll((this.options.wrap=="both"||this.options.wrap== "first")&&this.options.size!=null&&this.first==1?this.options.size:this.first-this.options.scroll)},scrollTail:function(a){if(!(this.locked||this.animating||!this.tail)){var c=h.intval(this.list.css(this.lt));!a?c-=this.tail:c+=this.tail;this.inTail=!a;this.prevFirst=this.first;this.prevLast=this.last;this.animate(c)}},scroll:function(a,c){this.locked||this.animating||this.animate(this.pos(a),c)},pos:function(a){var c=h.intval(this.list.css(this.lt));if(this.locked||this.animating)return c;if(this.options.wrap!= "circular")a=a<1?1:this.options.size&&a>this.options.size?this.options.size:a;for(var b=this.first>a,d=this.options.wrap!="circular"&&this.first<=1?1:this.first,e=b?this.get(d):this.get(this.last),f=b?d:d-1,g=null,j=0,l=false,k=0;b?--f>=a:++f<a;){g=this.get(f);l=!g.length;if(g.length==0){g=this.create(f).addClass(this.className("jcarousel-item-placeholder"));e[b?"before":"after"](g);if(this.first!=null&&this.options.wrap=="circular"&&this.options.size!==null&&(f<=0||f>this.options.size)){e=this.get(this.index(f)); if(e.length)g=this.add(f,e.clone(true))}}e=g;k=this.dimension(g);if(l)j+=k;if(this.first!=null&&(this.options.wrap=="circular"||f>=1&&(this.options.size==null||f<=this.options.size)))c=b?c+k:c-k}d=this.clipping();var o=[],n=0;f=a;var m=0;for(e=this.get(a-1);++n;){g=this.get(f);l=!g.length;if(g.length==0){g=this.create(f).addClass(this.className("jcarousel-item-placeholder"));e.length==0?this.list.prepend(g):e[b?"before":"after"](g);if(this.first!=null&&this.options.wrap=="circular"&&this.options.size!== null&&(f<=0||f>this.options.size)){e=this.get(this.index(f));if(e.length)g=this.add(f,e.clone(true))}}e=g;k=this.dimension(g);if(k==0)throw Error("jCarousel: No width/height set for items. This will cause an infinite loop. Aborting...");if(this.options.wrap!="circular"&&this.options.size!==null&&f>this.options.size)o.push(g);else if(l)j+=k;m+=k;if(m>=d)break;f++}for(g=0;g<o.length;g++)o[g].remove();if(j>0){this.list.css(this.wh,this.dimension(this.list)+j+"px");if(b){c-=j;this.list.css(this.lt,h.intval(this.list.css(this.lt))- j+"px")}}j=a+n-1;if(this.options.wrap!="circular"&&this.options.size&&j>this.options.size)j=this.options.size;if(f>j){n=0;f=j;for(m=0;++n;){g=this.get(f--);if(!g.length)break;m+=this.dimension(g);if(m>=d)break}}f=j-n+1;if(this.options.wrap!="circular"&&f<1)f=1;if(this.inTail&&b){c+=this.tail;this.inTail=false}this.tail=null;if(this.options.wrap!="circular"&&j==this.options.size&&j-n+1>=1){b=h.margin(this.get(j),!this.options.vertical?"marginRight":"marginBottom");if(m-b>d)this.tail=m-d-b}for(;a-- > f;)c+=this.dimension(this.get(a));this.prevFirst=this.first;this.prevLast=this.last;this.first=f;this.last=j;return c},animate:function(a,c){if(!(this.locked||this.animating)){this.animating=true;var b=this,d=function(){b.animating=false;a==0&&b.list.css(b.lt,0);if(b.options.wrap=="circular"||b.options.wrap=="both"||b.options.wrap=="last"||b.options.size==null||b.last<b.options.size)b.startAuto();b.buttons();b.notify("onAfterAnimation");if(b.options.wrap=="circular"&&b.options.size!==null)for(var e= b.prevFirst;e<=b.prevLast;e++)if(e!==null&&!(e>=b.first&&e<=b.last)&&(e<1||e>b.options.size))b.remove(e)};this.notify("onBeforeAnimation");if(!this.options.animation||c==false){this.list.css(this.lt,a+"px");d()}else this.list.animate(!this.options.vertical?this.options.rtl?{right:a}:{left:a}:{top:a},this.options.animation,this.options.easing,d)}},startAuto:function(a){if(a!=undefined)this.options.auto=a;if(this.options.auto==0)return this.stopAuto();if(this.timer==null){var c=this;this.timer=setTimeout(function(){c.next()}, this.options.auto*1E3)}},stopAuto:function(){if(this.timer!=null){clearTimeout(this.timer);this.timer=null}},buttons:function(a,c){if(a==undefined||a==null){a=!this.locked&&this.options.size!==0&&(this.options.wrap&&this.options.wrap!="first"||this.options.size==null||this.last<this.options.size);if(!this.locked&&(!this.options.wrap||this.options.wrap=="first")&&this.options.size!=null&&this.last>=this.options.size)a=this.tail!=null&&!this.inTail}if(c==undefined||c==null){c=!this.locked&&this.options.size!== 0&&(this.options.wrap&&this.options.wrap!="last"||this.first>1);if(!this.locked&&(!this.options.wrap||this.options.wrap=="last")&&this.options.size!=null&&this.first==1)c=this.tail!=null&&this.inTail}var b=this;this.buttonNext[a?"bind":"unbind"](this.options.buttonNextEvent+".jcarousel",this.funcNext)[a?"removeClass":"addClass"](this.className("jcarousel-next-disabled")).attr("disabled",a?false:true);this.buttonPrev[c?"bind":"unbind"](this.options.buttonPrevEvent+".jcarousel",this.funcPrev)[c?"removeClass": "addClass"](this.className("jcarousel-prev-disabled")).attr("disabled",c?false:true);this.options.buttonNextCallback!=null&&this.buttonNext.data("jcarouselstate")!=a&&this.buttonNext.each(function(){b.options.buttonNextCallback(b,this,a)}).data("jcarouselstate",a);this.options.buttonPrevCallback!=null&&this.buttonPrev.data("jcarouselstate")!=c&&this.buttonPrev.each(function(){b.options.buttonPrevCallback(b,this,c)}).data("jcarouselstate",c)},notify:function(a){var c=this.prevFirst==null?"init":this.prevFirst< this.first?"next":"prev";this.callback("itemLoadCallback",a,c);if(this.prevFirst!==this.first){this.callback("itemFirstInCallback",a,c,this.first);this.callback("itemFirstOutCallback",a,c,this.prevFirst)}if(this.prevLast!==this.last){this.callback("itemLastInCallback",a,c,this.last);this.callback("itemLastOutCallback",a,c,this.prevLast)}this.callback("itemVisibleInCallback",a,c,this.first,this.last,this.prevFirst,this.prevLast);this.callback("itemVisibleOutCallback",a,c,this.prevFirst,this.prevLast, this.first,this.last)},callback:function(a,c,b,d,e,f,g){if(!(this.options[a]==undefined||typeof this.options[a]!="object"&&c!="onAfterAnimation")){var j=typeof this.options[a]=="object"?this.options[a][c]:this.options[a];if(i.isFunction(j)){var l=this;if(d===undefined)j(l,b,c);else if(e===undefined)this.get(d).each(function(){j(l,this,d,b,c)});else for(var k=d;k<=e;k++)k!==null&&!(k>=f&&k<=g)&&this.get(k).each(function(){j(l,this,k,b,c)})}}},create:function(a){return this.format("<li></li>",a)},format:function(a, c){a=i(a);for(var b=a.get(0).className.split(" "),d=0;d<b.length;d++)b[d].indexOf("jcarousel-")!=-1&&a.removeClass(b[d]);a.addClass(this.className("jcarousel-item")).addClass(this.className("jcarousel-item-"+c)).css({"float":this.options.rtl?"right":"left","list-style":"none"}).attr("jcarouselindex",c);return a},className:function(a){return a+" "+a+(!this.options.vertical?"-horizontal":"-vertical")},dimension:function(a,c){var b=a.jquery!=undefined?a[0]:a,d=!this.options.vertical?(b.offsetWidth|| h.intval(this.options.itemFallbackDimension))+h.margin(b,"marginLeft")+h.margin(b,"marginRight"):(b.offsetHeight||h.intval(this.options.itemFallbackDimension))+h.margin(b,"marginTop")+h.margin(b,"marginBottom");if(c==undefined||d==c)return d;d=!this.options.vertical?c-h.margin(b,"marginLeft")-h.margin(b,"marginRight"):c-h.margin(b,"marginTop")-h.margin(b,"marginBottom");i(b).css(this.wh,d+"px");return this.dimension(b)},clipping:function(){return!this.options.vertical?this.clip[0].offsetWidth-h.intval(this.clip.css("borderLeftWidth"))- h.intval(this.clip.css("borderRightWidth")):this.clip[0].offsetHeight-h.intval(this.clip.css("borderTopWidth"))-h.intval(this.clip.css("borderBottomWidth"))},index:function(a,c){if(c==undefined)c=this.options.size;return Math.round(((a-1)/c-Math.floor((a-1)/c))*c)+1}});h.extend({defaults:function(a){return i.extend(p,a||{})},margin:function(a,c){if(!a)return 0;var b=a.jquery!=undefined?a[0]:a;if(c=="marginRight"&&i.browser.safari){var d={display:"block","float":"none",width:"auto"},e,f;i.swap(b,d, function(){e=b.offsetWidth});d.marginRight=0;i.swap(b,d,function(){f=b.offsetWidth});return f-e}return h.intval(i.css(b,c))},intval:function(a){a=parseInt(a);return isNaN(a)?0:a}})})(jQuery);
var nivo_carousel = function() {
    $('#slider').nivoSlider({
        effect: 'random', // Specify sets like: 'fold,fade,sliceDown'
        animSpeed: 800, // Slide transition speed
        pauseTime: 8000, // How long each slide will show
        directionNav: false,
        controlNav: true,
        controlNavThumbs: true,
        controlNavThumbsFromRel: true,
		randomStart: true,
    });
};


function banner_carousel_fadeOut(carousel){
    var JCcontainerID = carousel.clip.context.id;
    $('ul.banner-carousel'+ JCcontainerID).fadeOut();
}

function banner_carousel_fadeIn(carousel){
    var JCcontainerID = carousel.clip.context.id;
    $('ul.banner-carousel' + JCcontainerID).fadeIn();
}

var banner_carousel = function(){
    if ($('div.banner ul.banner-carousel li').length > 1 ){
        $('div.banner ul.banner-carousel').jcarousel({
            auto:5,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            itemLoadCallback: {
                onBeforeAnimation: banner_carousel_fadeOut,
                onAfterAnimation: banner_carousel_fadeIn
            }

        });
    }
};

$(document).ready(function(){
    function top_ten_carousel(){
        function toptenInitCallback(carousel){
            $('#top-ten .next').bind('click', function () {
                carousel.next();
                return false;
            });

            $('#top-ten .prev').bind('click', function () {
                carousel.prev();
                return false;
            });
        }

        $('#home #top-ten ul').jcarousel({
            initCallback: toptenInitCallback,
            auto:0,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            animation:500
        });
    }
    function last_news_carousel(){
        function lastnewsInitCallback(carousel){
            $('#last-news .next').bind('click', function () {
                carousel.next();
                return false;
            });

            $('#last-news .prev').bind('click', function () {
                carousel.prev();
                return false;
            });
        }

        $(' #home #last-news ul').jcarousel({
            initCallback: lastnewsInitCallback,
            auto:0,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            animation:500
        });
    }
    function channel_carousel(){
        function channelInitCallback(carousel){
            $('#channel .next').bind('click', function () {
                carousel.next();
                return false;
            });

            $('#channel .prev').bind('click', function () {
                carousel.prev();
                return false;
            });
        }

        $('#home #channel ul').jcarousel({
            initCallback: channelInitCallback,
            auto:0,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            animation:500
        });
    }
    // carrossel dos videos em categoria
    function category_carousel(){
        function categoryInitCallback(carousel){
            $('#videos .next').bind('click', function () {
                carousel.next();
                return false;
            });

            $('#videos .prev').bind('click', function () {
                carousel.prev();
                return false;
            });
        }

        $('#category #videos ul').jcarousel({
            initCallback: categoryInitCallback,
            auto:0,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            animation:500
        });
    }

    function ad_promotion_coupon(){
        function couponInitCallback(carousel){
            $('#ad .coupons .arrows-coupons .next').bind('click', function () {
                var actual = $('#ad .coupons span.actual').text();
                actual = parseInt(actual);
                var total = $('#ad .coupons span.total').text().replace('/', '');
                total = parseInt(total);
                if (actual >= total){
                    $('#ad .coupons span.actual').text('1');
                }else{
                    actual = actual + 1;
                    $('#ad .coupons span.actual').text(actual);
                }
                carousel.next();
                return false;
            });

            $('#ad .coupons .arrows-coupons .prev').bind('click', function () {
                var actual = $('#ad .coupons span.actual').text();
                actual = parseInt(actual);
                var total = $('#ad .coupons span.total').text().replace('/', '');
                total = parseInt(total);
                if (actual <= 1){
                    $('#ad .coupons span.actual').text(total);
                }else{
                    actual = actual - 1;
                    $('#ad .coupons span.actual').text(actual);
                }
                carousel.prev();
                return false;
            });
        }

        $('#ad .results ul.carousel-coupon').jcarousel({
            initCallback: couponInitCallback,
            auto:0,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            animation:500
        });
    }

    function ad_promotion_valley(){
        function valleyInitCallback(carousel){
            $('#ad .valley .arrows-valley .next').bind('click', function () {
                var actual = $('#ad .valley span.actual').text();
                actual = parseInt(actual);
                var total = $('#ad .valley span.total').text().replace('/', '');
                total = parseInt(total);
                if (actual >= total){
                    $('#ad .valley span.actual').text('1');
                }else{
                    actual = actual + 1;
                    $('#ad .valley span.actual').text(actual);
                }
                carousel.next();
                return false;
            });

            $('#ad .valley .arrows-valley .prev').bind('click', function () {
                var actual = $('#ad .valley span.actual').text();
                actual = parseInt(actual);
                var total = $('#ad .valley span.total').text().replace('/', '');
                total = parseInt(total);
                if (actual <= 1){
                    $('#ad .valley span.actual').text(total);
                }else{
                    actual = actual - 1;
                    $('#ad .valley span.actual').text(actual);
                }
                carousel.prev();
                return false;
            });
        }

        $('#ad .results ul.carousel-valley').jcarousel({
            initCallback: valleyInitCallback,
            auto:0,
            scroll:1,
            wrap:'circular',
            buttonNextHTML:null,
            buttonPrevHTML:null,
            animation:500
        });
    }

    nivo_carousel();
    top_ten_carousel();
    last_news_carousel();
    channel_carousel();
    category_carousel();
    banner_carousel();
    ad_promotion_coupon();
    ad_promotion_valley();
});

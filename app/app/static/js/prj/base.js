var Maps = function(){
	var map = null;
	var geocoder = null;


	this.initialize = function() {
		if (GBrowserIsCompatible()) {
			map = new GMap2(document.getElementById("map-canvas"));
			var directionsPanel;
			var directions;
			geocoder = new GClientGeocoder();
			map.addControl(new GSmallMapControl());
			map.addControl(new GMapTypeControl());

		}
	};

	this.showAddress = function(address) {
		if (geocoder) {

			geocoder.getLatLng(address, function(point){
				if (!point) {
				} else {
					map.setCenter(point, 15);
					var marker = new GMarker(point);
					var html = '<div id="map-marker">'+
						'<b>'+ $('.content #title').val() +'</b><br />'+
						address+
						'</div>';
					map.addOverlay(marker);
					marker.openInfoWindowHtml(html);
				}
			});
		}
	};
	this.showMap = function(address) {
		if (geocoder) {
			geocoder.getLatLng(address, function(point){
				if (!point) {
					console.log(address + " not found");
				} else {
					map.setCenter(point, 15);
					var marker = new GMarker(point);
					map.addOverlay(marker);
				}
			});
		}
	};
};

$(document).ready(function(){
	$('input, textarea').placeholder();

	// marca link selecionado no menu
	function select_menu(){
		var rel = $('body').attr('rel');
		if (rel){
			$('#menu ').find('.' + String(rel)).addClass('active');
		}
	}
	select_menu();
	var k = new Maps(),
		 address;
	if( $('#edit-ad #map-canvas').length ){
		k.initialize();
		address = $('#address #id_street').val() + ', ' +
		 $('#address #id_number').val() + ', ' +
		 $('#address #id_complement').val() + ', ' +
		 $('#address #id_city option:selected').text() + ', ' +
		 $('#address #id_state option:selected').text();
		k.showAddress(address);
		$('#id_street, #id_number, #id_complement, #id_state, #id_city').blur(function(){
		 address = $('#address #id_street').val() + ', ' +
			 $('#address #id_number').val() + ', ' +
			 $('#address #id_complement').val() + ', ' +
			 $('#address #id_city option:selected').text() + ', ' +
			 $('#address #id_state option:selected').text();
		k.showAddress(address);
		});
	}else if( $('#ad #map-canvas').length ){
		address = $('#map-canvas').attr('rel');
		k.initialize();
		k.showMap(address);
	 }

	 // .live('click',function(){
	//customiza campo de arquivo
	function update_input(){
		if ($.browser.msie){
			$('input[type="file"]').wrap('<span class="input-file"></span>').parent().prepend('<span class="val"/>');
			$('input[type="file"]').live('change', function(){
				var value_span = $(this).val();
				$(this).parent().find("span.val").html(value_span);
			});
		} else {
			$('input[type="file"]').wrap('<span class="input-file"></span>').parent().prepend('<span class="val"/>');
			$('input[type="file"]').live('change', function(){
				$(this).parent().find("span.val").text($(this).val());
			});
		}
	}
	update_input();

	//carousel da home
	$('#home #header #carousel ul').roundabout({
		  minOpacity: 0.7,
		  minScale: 0.2,
		  btnNext: '#carousel .next',
		  btnPrev: '#carousel .prev'
	  });

	// customiza selects
	$('#search-form select#id_locale').selectreplace({width:142, height:22, scrollAfter:6});
	$('#search-form select#id_state').selectreplace({width:57, height:22, scrollAfter:6});
	$('#sign-up .article form .column select').selectreplace({width:135, height:22, scrollAfter:6});
	$('#sign-up .article form .small-column select').selectreplace({width:135, height:22, scrollAfter:6});
	$('#sign-up .article form .row select').selectreplace({width:135, height:22, scrollAfter:6});
	$('#sign-up .article form .plan select').selectreplace({width:219, height:22, scrollAfter:6});
	$('#edit-ad select#id_type_ad').selectreplace({width:135, height:22, scrollAfter:6});
	$('#contact .form select#id_subject').selectreplace({width:142, height:22, scrollAfter:6});
	$('#new-voucher form #id_type_promotion').selectreplace({width:142, height:22, scrollAfter:6});

	// Atualiza div da enquete após voto
	$('#poll-form form').submit(function(){
		$.post($(this).attr('action'), $(this).serialize(), function(data) {
			$('#poll-form').load(data);
		});
		return false;
	});

	// Atualiza pagina da enquete após clicar em ver resultado(foi retirado do site)
	$('#poll-form a').click(function(){
		$('#poll-form').load($(this).attr('href'));
		return false;
	});

	// Paginação de news, channel
	$('#channel .pagination a, #news .pagination a').live('click',function(){
		var id = $(this).parents('div.pages').attr('id');
		$(this).parents('div.pages').load($(this).attr('href') + ' #'+id+' div');
		return false;
	});
	// paginação resultado filtro: categoria e anuncio aberto
	$('#results div.pagination-filter a').live('click',function(){
		$(this).parents('div.pages').load($(this).attr('href') + ' #'+id+' div');
		return false;
	});

	// Atualiza div em channel para videos mais vistos ou todos ordem aleatória
	$('#filter-video input[type="radio"]').live('change', function(){
		if ($('#show-more').is(':checked')){
			$('#more').hide();
			$('#more-viewed').show();
		}
		else {
			$('#more-viewed').hide();
			$('#more').show();
		}
	});

	// Menu lateral de channel
	$('#channel #content .wrap .menu .links a').click(function(){
		var self = this;
		$('div.bg-top').load('/tv/categoria/'+ $(this).attr('id') + '/ .bg-bottom' , function(){
			$('#channel .links a.active').removeClass('active');
			$(self).addClass('active');
		});
		return false;
	});

	$('#channel .more .results a').live('click', function(){
		$('div.bg-top').load('/tv/'+ $(this).attr('rel') + '/ .bg-bottom' );
		return false;
	});


	// Valida e-mail
	function checkEmail(theEmail){
		if(theEmail.match(/^\w+([\.\-]\w+)*\@\w+([\.\-]\w+)*\.\w{2,4}$/i)){
			return true;
		}else{
			return false;
		}
	}

	// Valida todos os campos do form comments em channel
	$('#channel div.comments form').live('submit', function(e){
		var error = false;
		if($('#id_comment').val() === ''){
			error = true;
			$('span.id_comment').html('Este campo é obrigatório');
		}else {
			$('span.id_comment').empty();
		}
		if($('#id_email').val() == 'E-mail' || $('#id_email').val() === ''){
			error = true;
			$('span.id_email').html('Este campo é obrigatório');
		}else {
			var check = checkEmail($('#id_email').val());
			if(!check){
				error = true;
				$('span.id_email').html('Digite um e-mail válido');
			}else {
				$('span.id_email').empty();
			}
		}
		if($('#id_name').val() === ''){
			error = true;
			$('span.id_name').html('Este campo é obrigatório');
		}else {
			$('span.id_name').empty();
		}
		if(error){
			e.preventDefault();
			return false;
		}else{
			this.submit();
		}
	});

	// Valida todos os campos do form comments em anúncios
	$('#ad div.comments li').live('submit', function(e){
		var error = false;
		if($('#id_comment').val() === ''){
			error = true;
			$('span.id_comment').html('Este campo é obrigatório');
		}else {
			$('#span.id_comment').empty();
		}
		if($('#id_email').val() == 'E-mail' || $('#id_email').val() === ''){
			error = true;
			$('span.id_email').html('Este campo é obrigatório');
		} else {
			var check = checkEmail($('#id_email').val());
			if(!check){
				error = true;
				$('span.id_email').html('Digite um e-mail válido');
			} else {
				$('span.id_email').empty();
			}
		}
		if($('.user #id_name').val() === ''){
			error = true;
			$('span.id_name').html('Este campo é obrigatório');
		} else {
			$('span.id_name').empty();
		}
		if(error){
			e.preventDefault();
			return false;
		} else{
			this.submit();
		}
	});

	// Valida todos os campos do form comments em news
	$('#news div.comments form').live('submit', function(e){
		var error = false;
		if($('#id_comment').val() === ''){
			error = true;
			$('span.id_comment').html('Este campo é obrigatório');
		}else {
			$('span.id_comment').empty();
		}
		if($('#id_email').val() == 'E-mail' || $('#id_email').val() === ''){
			error = true;
			$('span.id_email').html('Este campo é obrigatório');
		}else {
			var check = checkEmail($('#id_email').val());
			if(!check){
				error = true;
				$('span.id_email').html('Digite um e-mail válido');
			}else {
				$('span.id_email').empty();
			}
		}
		if($('#id_name').val() === ''){
			error = true;
			$('span.id_name').html('Este campo é obrigatório');
		}else {
			$('span.id_name').empty();
		}
		if(error){
			e.preventDefault();
			return false;
		}else{
			this.submit();
		}
	});

	// Mascaras nos campos dos forms
	$(function(){
		$('#id_cpf_cnpj').mask('999.999.999-99');
		$('#id_birth_date').mask('99/99/9999');
		$('#id_zip_code').mask('99999-999');
		$('#id_phone').mask('9999-9999');
		$('#id_cell_phone').mask('9999-9999');
		$('.ddd').mask('(99)9999-9999');
		$('#id_start_date').mask('99/99/9999');
		$('#id_end_date').mask('99/99/9999');
		$('#id_cpf').mask('999.999.999-99');
		$('#id_limit_vouchers').mask('?9999');
		$('#id_number_ads').mask('9?99999999');
	});

	$('#id_type_person').change(function(){
		if( $(this).val() == 'legal_entity' ){
			$('#id_cpf_cnpj').mask('999.999.999/9999-99');
			$('.responsible').show();
		} else {
			$('#id_cpf_cnpj').mask('999.999.999-99');
			$('.responsible').hide();
		}
	});

	//fecha ligthbox
	$('span.close').live('click', function(){
		$.fancybox.close();
	});

	//cria lightbox
	$('a.lightbox').fancybox({
		'showCloseButton': false
	});

	// Fancybox das fotos do aberto anúncio
	 $('a.lightbox-gallery').fancybox({
		 'transitionIn'	 :	 'elastic',
		 'transitionOut' :	 'elastic',
		 'speedIn'		 :	 600,
		 'speedOut'		 :	 200,
		 'overlayShow'	 :	 true,
		 'opacity'		 :	 true,
		 'titlePosition' :	 'inside'
	});

	// Não a opção marcada ao mesmo tempo que as outras em busca
	$('.article #results #all-types').live('change', function(){
		if($('#results #all-types').is(':checked')){
			$('.article input').not('#all-types').removeAttr('checked');
		}
	});

	$('.article #results form input').live('change', function(){
		if($(this).is(':checked') && $(this).attr('id') != 'all-types'){
			$('#result-search #results form #all-types').removeAttr('checked');
		}
	});

	// Atualiza filtro do resultado da busca por tipo de anunciante (busca textual)
	$('#result-search #results ul input').live('change', function(){
		var data = $(this).parents('form').serialize()+'&'+ $('#search-form').serialize();
		$('div.results').load('/resultado-busca/ ul.results', data);
	});

	// Atualiza filtro do resultado da busca por tipo de anunciante (busca em categoria)
	$('#category #results form#filter input').live('change', function(){
		var data = $(this).parents('form').serialize()+'&'+ $('#filter-form').serialize();
		$.getJSON('/categoria/filtro/', data, function(response){
			$('.bg-top').html(response.html);
			nivo_carousel();
		});
	});

	// Atualiza filtro do resultado da busca por tipo de anunciante (busca em anúncio)
	$('#ad #results form#filter input').live('change', function(){
		var data = $(this).parents('form').serialize()+'&'+ $('#filter-form').serialize();
		$.getJSON('/categoria/filtro/', data, function(response){
			$('.bg-top').html(response.html);
			nivo_carousel();
		});
	});

	//menu lateral das categorias
	$('fieldset.activities label.border-top').click(function(){
		height = $(this).siblings('ul.scroll').height();
		if( $(this).hasClass('opened') ){
			$(this).removeClass('opened').siblings('ul').slideUp();
			$('fieldset.activities > ul > li.checked')
				.removeClass('checked')
				.find('input:checked')
				.removeAttr('checked')
				.parent()
				.siblings('ul')
				.slideUp();
		} else {
			$('fieldset.activities label.opened').removeClass('opened').siblings('ul').slideUp();
			$(this).addClass('opened').siblings('ul').slideDown(function(){
				var height_ul_activity = $('ul.ul-activity').height();
				if( height_ul_activity >= 162){
					// $('ul.ul-activity').jScrollPane();
				}
				if( height >= 162){
					$('ul.scroll').jScrollPane();
				}
			}).find('>li').slideDown();
		}

	});

	$('fieldset.activities .inner input').change(function(){
		if( $(this).is(':checked') ){
			$(this).parents('li').addClass('checked').siblings().slideUp();
			$(this).parents('li').find('ul.ul-option').slideDown();
			$('fieldset.activities .inner input:checked').not(this).removeAttr('checked').parent().siblings('ul.ul-activity').slideUp();
		} else {
			$(this).parents('li').removeClass('checked').siblings().slideDown();
			$(this).parents('li').find('.ul-option').slideUp().find(':checked').removeAttr('checked');
		}
		var data = $(this).parents('form').serialize(),
			self = $(this);
		$.getJSON($(this).parents('form').attr('action'), data, function(ret){
			$('div.bg-top').html(ret.html);
			if (self.is(':checked')){
				$.each(ret.activities, function(i, item){
					var arr = item[1].join(',').split(',');

					$.each(arr, function(i, item){
						$('.ul-optionvalue input[value="' + item + '"]')
							.parents(".li-value")
							.addClass('optionvalue')
							.parents(".option")
							.show();
					});
				});
			}
			nivo_carousel();
		});
		$('#wrap-suggestion').slideDown();
	});

	$('fieldset.activities li.option span').click(function(){
		var height = $(this).siblings('ul.ul-optionvalue').height();
		if( $(this).hasClass('open')){
			$(this).siblings("ul.ul-optionvalue").slideUp();
			$(this).removeClass('open').addClass('close');
		} else {
			$(this).removeClass('close').addClass('open');
			$(this).parents().siblings().find('ul.ul-optionvalue').slideUp();
			$(this).parents().siblings().find('span').removeClass('open').addClass('close');
			$(this).siblings('ul.ul-optionvalue').slideDown(function(){
				if (height >= 156){
					$(this).addClass('ul-scroll');
					$('ul.ul-scroll').jScrollPane();
				}
			});
		}
	});

	$('fieldset.activities .ul-optionvalue input').change(function(){
		var data = $(this).parents('form').serialize(),
			self = $(this);
		if( $(this).is(':checked') ){
			$(this).parents('li.li-value').addClass('checked');
			var value = $(this).val();
		} else {
			$(this).parents('li.li-value').removeClass('checked');
		}
		$.getJSON($(this).parents('form').attr('action'), data, function(ret){
			$('div.bg-top').html(ret.html);

			$.each(ret.activities, function(i, item){
				var arr = item[1].join(',').split(',');
				// $('.optionvalue').removeClass('optionvalue');
				$.each(arr, function(i, item){
					$('.ul-optionvalue input[value="' + item + '"]')
						.parents(".li-value")
						.addClass('optionvalue')
						.parents(".option")
						.show();

				});
			});
		nivo_carousel();
		});
	});

	$('div#pagination-filter .pagination a').live('click', function(){
		var page = $(this).attr('page');
		var filter = $('div#pagination-filter div.pagination input.url-filter').val();
		$.getJSON('/categoria/filtro/?'+filter+'&page='+page , function(data){
			$('div.bg-top').html(data.html);
			nivo_carousel();
			return false;
		});
		return false;
	});

	$(' fieldset.activities > ul > li > ul > li > label > input').change(function(){
		var data = $(this).parents('form').serialize(),
			self = $(this);
		if( $(this).is(':checked') ){
			$(this).parents('li').addClass('checked');
		} else {
			$(this).parents('li').removeClass('checked');
		}
		$.getJSON($(this).parents('form').attr('action'), data, function(ret){
			$('div.bg-top').html(ret.html);
			$.each(ret.activities, function(i, item){
				var inputs = self.parent().parent().siblings().find('input');
				$.each(inputs, function(i, input){
					var arr = item[1].join(',').split(','),
						value = $(input).val();
					if ( self.is(':checked')){
						if( arr.indexOf(value) < 0){
							$(input).parent().parent().hide();
						}
					} else {
						if( arr.indexOf(value) >= 0){
							$(input).parent().parent().css('display', 'block');
						}
					}

				});
			});
			nivo_carousel();
		});
	});

	$('#filter-form fieldset.activities div.locale ul li input').change(function(){
		if( $(this).is(':checked') ){
			$(this).parents('li').addClass('checked');
		} else {
			$(this).parents('li').removeClass('checked');

		}
		var data = $(this).parents('form').serialize();
		$.getJSON($(this).parents('form').attr('action'), data, function(ret){
			$('div.bg-top').html(ret.html);
			nivo_carousel();
		});

		$('#wrap-suggestion').slideDown();
	});

	$('fieldset.activities div.payment ul li input').change(function(){
		if( $(this).is(':checked') ){
			$(this).parents('li').addClass('checked');
		} else {
			$(this).parents('li').removeClass('checked');
		}
		var data = $(this).parents('form').serialize();
		$.getJSON($(this).parents('form').attr('action'), data, function(ret){
			$('div.bg-top').html(ret.html);
			nivo_carousel();
		});
		$('#wrap-suggestion').slideDown();
	});

	//desmarca checkbox que estavam no cache
	$(' fieldset.activities input:checked').removeAttr('checked');

	$('span.text').live('click', function(){
		$.fancybox.close();
	});

	function delete_images(inputs){
		var list_images = '';
		$.each(inputs, function(i, item){
		   if ($(item).val()){
			   list_images += 'images_path=' + ($(item).val()) + '&';
		   }
		});
		$.get('/anuncio/excluir-imagems/?'+list_images);
	}

	// new-ad e edit-ad mensagem de foto caregada com sucesso.
	$('#adicionar-imagem form #id_photo_set-0-photo').change(function(){
		$("p.success0").show();
	});

	$('#adicionar-imagem form #id_photo_set-1-photo').change(function(){
		$("p.success1").show();
	});

	$('#adicionar-imagem form #id_photo_set-2-photo').change(function(){
		$("p.success2").show();
	});

	$('#adicionar-imagem form #id_photo_set-3-photo').change(function(){
		$("p.success3").show();
	});

	$('#adicionar-imagem form #id_photo_set-4-photo').change(function(){
		$("p.success4").show();
	});

	$('#adicionar-imagem form #id_photo_set-5-photo').change(function(){
		$("p.success5").show();
	});

	// logo do new-ad e edit-ad mensagem de sucesso
	$('#imagem-exibicao form input[type="file"]').change(function(){
		$("div.lightbox .help-logo").hide();
		$("div.lightbox .success-logo").show();
	});

	$('#imagem-exibicao form input[type="submit"]').live('click', function(){
		$(this).parents('form').submit();
		$('#imagem-exibicao form .loading').show();
		$("#uploader").load(function(){
			data = $('#uploader').contents().find('body').text();
			data = $.parseJSON(data);
			if ( !data.error){
				// delete_images($('#edit-ad #id_image'));
				$('#image-logo').attr('src', data.image_url);
				$('#edit-ad #id_image').val(data.image_save);
				$.fancybox.close();
				$('#imagem-exibicao form .loading').hide();
				$('.help-logo').hide();
				$('.success-logo').show();
			} else {
			   $('.new-ad #fancybox #imagem-exibicao div.error').show();
			}
		});
		return false;
	});

	$('body#edit-ad #fancybox #imagem-exibicao form input[type="submit"]').submit(function(){
		$('body#edit-ad #fancybox #imagem-exibicao form .loading').show();
		return true;
	});

	$('body#edit-ad #fancybox #adicionar-imagem form input[type="submit"]').submit(function(){
		$('body#edit-ad #fancybox #adicionar-imagem form .loading').show();
		return true;
	});

	$('body#edit-ad #fancybox #alterar-video form input[type="submit"]').submit(function(){
		$('body#edit-ad #fancybox #alterar-video form .loading').show();
		return true;
	});

	$('#adicionar-imagem form input[type="submit"]').live('click', function(){
		$(this).parents('form').submit();
		$('#adicionar-imagem form .loading').show();
		$("#uploader").load(function(){
			data = $('#uploader').contents().find('body').text().replace(/\u\'/g, '\'').replace(/\},/g, '}-----');
			data = $.parseJSON(data);
			if ( !data.error){
				var images = $('#gallery img'),
					inputs = $('.line .hidden input[name$="-photo"]');
				delete_images(inputs);
				inputs.val('');
				list_photos = data.list_photos.replace(/\[/g, '').replace(/\]/g,'').split('-----');

				$.each(list_photos, function(i, item){
					item = $.parseJSON(item.replace(/\'/g, '"'));
				   $(images).eq(i).attr('src', item.image_url);
				   $(inputs).eq(i).val(item.image);
				});

				$.fancybox.close();
				$('#adicionar-imagem form .loading').hide();
			} else {
				$('.new-ad #fancybox #adicionar-imagem div.error').show();
			}
		});
		return false;
	});

	$('.new-ad #fancybox #alterar-video form').submit(function(){
		$('#alterar-video form .loading').show();
		var value_video = $(this).find('input[type="text"]').val(),
			video;
		$('#id_video').val(value_video);

		if( value_video.indexOf('youtube') != -1 ){
			video = value_video.split('v=');
			video = video[video.length-1];
			video = 'http://www.youtube.com/v/' + video;
		}else {
			video = value_video.split('.com/');
			video = video[video.length-1];
			video = 'http://vimeo.com/moogaloop.swf?clip_id=' + video;
		}
		$('#video iframe').attr('src', video);
		$.fancybox.close();
		$("#edit-ad #video .success").show();
		$('#alterar-video form .loading').hide();
		return false;
	});

	//atualiza pagina ao alterar cidade de busca
	$('#search-form #id_locale').change(function(){
		$('#search-form').submit();
	});

	// function refresh_activity(category, uncheck){
	// 	if (uncheck){
	// 		$('div#values').slideUp().find('li').slideUp().find('input').removeAttr('checked');
	// 	}
	// 	$.getJSON('/anuncio/filtrar-atividades/'+category+'/', function(data){
	// 		console.log(data.activities)
	// 	   if(data.activities){
	// 		   $('div#activities').slideDown();
	// 		   var inputs = $('div#activities ul li label input');
	// 		   $.each(inputs, function(i, input){
	// 				var value = $(input).val(),
	// 					arr = data.activities.join(',').split(',');
	// 				if( arr.indexOf(value) >= 0){
	// 					$(input).parents('li').show();
	// 				} else {
	// 					$(input).parents('li').hide().find('input').removeAttr('checked');
	// 				}
	// 			});
	// 		   $('#activities .loader').hide();
	// 	   } else {
	// 		   $('div#activities').slideUp().find('li').slideUp().find('input').removeAttr('checked');
	// 	   }
	//    });
	// }

	function refresh_activity(category, uncheck){
		var ad = $('span.hidden').text();
		if (uncheck){
			$('div#values').slideUp().find('li').slideUp().find('input').removeAttr('checked');
		}
		$.getJSON('/anuncio/filtrar-atividades/'+category+'/'+ad+'/', function(data){
		   	if(data.activities){
		   		$('div#activities ul').empty();
		   		for(i=0; i<= data.activities.length-1; i++){
		   			if(data.ad_activities){
		   				for(j=0; j<=data.ad_activities.length-1; j++){
		   					if( (data.activities[i]['id'])  == (data.ad_activities[j]['id'])){
		   						$('#activities ul').append('<li><label for="id_activities_'+i+'"><input id="id_activities_'+i+'" type="radio" value="'+data.activities[i]['id']+'" name="activities" checked="checked">'+data.activities[i]['name']+'</label></li>');
		   						var activities = 'activities='+data.activities[i]['id']
		   						refresh_option_values(activities);
		   					}else{
		   						$('#activities ul').append('<li><label for="id_activities_'+i+'"><input id="id_activities_'+i+'" type="radio" value="'+data.activities[i]['id']+'" name="activities">'+data.activities[i]['name']+'</label></li>');
		   					}
		   				}
		   			}else{
		   				$('#activities ul').append('<li><label for="id_activities_'+i+'"><input id="id_activities_'+i+'" type="radio" value="'+data.activities[i]['id']+'" name="activities">'+data.activities[i]['name']+'</label></li>');
		   			}
				}
				$('div#activities div.loader').hide();
				$('div#activities').show();
		   	}else {
			   	$('div#activities').hide().find('li').slideUp().find('input').removeAttr('checked');
		   	}
	   	});
	}

	function refresh_option_values(activities){
		var ad = $('span.hidden').text();
		$.getJSON('/anuncio/filtrar-caracteristicas/'+ad+'/', activities, function(data){
			if(data.values){
				$('#values ul').empty();
				for(i=0; i<= data.values.length-1 ; i++){
					if(data.ad_values){
						// for(j=0; j<=data.ad_values.length-1; j++){
						var j = 0;
						while( j<data.ad_values.length && (data.values[i]['id']) != (data.ad_values[j]['id']) ){
							j++;
						}
						if (j == data.ad_values.length){
							$('#values ul').append('<li><label for="id_option_values_'+i+'"><input id="id_option_values_'+i+'" type="checkbox" value="'+data.values[i]['id']+'" name="option_values">'+data.values[i]['name']+'</label></li>');
						}else{
							$('#values ul').append('<li><label for="id_option_values_'+i+'"><input id="id_option_values_'+i+'" type="checkbox" value="'+data.values[i]['id']+'" name="option_values" checked="checked">'+data.values[i]['name']+'</label></li>');
						}

							// if( (data.values[i]['id']) == (data.ad_values[j]['id']) ){
							// 	$('#values ul').append('<li><label for="id_option_values_'+i+'"><input id="id_option_values_'+i+'" type="checkbox" value="'+data.values[i]['id']+'" name="option_values" checked="checked">'+data.values[i]['name']+'</label></li>');
							// }else{
							// 	$('#values ul').append('<li><label for="id_option_values_'+i+'"><input id="id_option_values_'+i+'" type="checkbox" value="'+data.values[i]['id']+'" name="option_values">'+data.values[i]['name']+'</label></li>');
							// }
					}else{
						$('#values ul').append('<li><label for="id_option_values_'+i+'"><input id="id_option_values_'+i+'" type="checkbox" value="'+data.values[i]['id']+'" name="option_values">'+data.values[i]['name']+'</label></li>');
					}
				}
				$('#values div.loader').hide();
				$('div#values').show();
				$('#values').find('ul').show();
			}else{
				$('div#values').hide().find('li').slideUp().find('input').removeAttr('checked');
				$('#values').find('ul').show();
			}
		});
	}

	$('#edit-ad div#categories ul li label input').live('change', function(){
		refresh_activity($(this).val(), true);
		$('#activities .loader').show();
	});

	$('#edit-ad div#activities ul li label input').live('change', function(){
		var activities = $('#activities ul li label input:checked').serialize();
		refresh_option_values(activities);
		$('#values .loader').show();
		$('#values').find('ul').hide();
	});

	if($('body#edit-ad').length){
		var activities = $('#activities ul li label input:checked').serialize(),
			category = $('#categories ul li input:checked').val(),
			images = $('#gallery img'),
			inputs = $('.line .hidden input[name$="-photo"]');
		if (category){
			refresh_activity(category, false);
			$('#activities .loader').show();
			if (activities){
				refresh_option_values(activities);
				$('#values .loader').show();
				$('#values').find('ul').hide();
			}
		}
		$.each(inputs, function(i, item){
			if($(item).val()){
				var img = $(item).val().split('/');
				img[img.length-1] = 'thumb.' + img[img.length-1];
				img = img.join('/');

				$(images).eq(i).attr('src', '/media/' + img )
					.parents('a').attr('href','/media/' + $(item).val());
			}
		});
	}


	$('#edit-ad #video iframe').each(function(){
		var url = $(this).attr("src",url+"?wmode=opaque");
	});

	$('#ad form.is_active').change(function(){
		$.post($(this).attr('action'), $(this).serialize());
	});

	$('#sign-up .submit input[type="submit"]').click(function(){
		$.fancybox($('div.confirmation').html());
		$('#fancybox-content .fancybox-confirmation a.no').click(function(){
			$.fancybox.close();
			return false;
		 });
		 $('#fancybox-content .fancybox-confirmation a.yes').click(function(){
			$('body#sign-up .article form').submit();
			return false;
		});
		return false;
	});

	$('#sign-up .article form p.submit input[type="submit"]').click(function(){
		$.fancybox($('div.confirmation').html());
		$('#fancybox-content .fancybox-confirmation a.no').click(function(){
			$.fancybox.close();
			return false;
		});
		$('#fancybox-content .fancybox-confirmation a.yes').click(function(){
			$('body#sign-up .article form').submit();
			return false;
		});
		return false;
 	});

	function load_cep(cep){
		$.post('/locations/refresh-address/', {'zipcode': cep.replace("-", "")}, function(data){
			if (data.empty){
				$('#address input#id_street').val('').removeAttr('readonly');
				$('#address input#id_number').removeAttr('readonly');
				$('#address input#id_complement').val('').removeAttr('readonly');
				$('#address .ad-state #id_state').remove();
				$('#address .ad-state').append('<select id="id_state" name="state"><option selected="selected" value="">Estado *</option></select>');
				$.each(data.list_state, function(i, item){
					$('#address .ad-state #id_state').append('<option value="'+ item[0] +'">'+ item[1] +'</option>');
				});
				$('#address .ad-city #id_city').remove();
				$('#address .ad-city').append('<input id="id_city" type="text" value="" name="city" placeholder="Cidade*"/>');

				$('#address .ad-area #id_area').remove();
				$('#address .ad-area').append('<input id="id_area" type="text" value="" name="area" placeholder="Bairro*"/>');
				//Anuncie #sign-up
				$('#sign-up #id_address').val('').removeAttr('readonly');
				$('#sign-up #id_area').val('').removeAttr('readonly');
				$('#sign-up #id_city').val('').removeAttr('readonly');
				$('#sign-up ._state .border-left').remove();
				$('#sign-up ._state #id_state').remove();
				$('#sign-up ._state .selbox').remove();
				$('#sign-up ._state').append('<select id="id_state" name="state"><option selected="selected" value="">Estado *</option></select>');
				$.each(data.list_state, function(i, item){
					$('#sign-up #id_state').append('<option value="'+ item[1] +'">'+ item[1] +'</option>');
				});
				$('#sign-up #id_state').selectreplace({width:135, height:22, scrollAfter:6});
				// $('#sign-up select#id_state').remove();
				// $('#sign-up select#id_state option').hide()
			}
			else{
				// New_Ad
				$('#address #id_street').val(data.address);
				$('select#id_state').remove();
				$('#address .ad-state #id_state').remove();
				$('#address .ad-state').append('<input class="state_readonly" id="id_state" type="text" value="' + data.state + '" name="_state" readonly="readonly"/>');
				$('#address .ad-state').append('<input id="id_state" type="hidden" value="' + data.id_state + '" name="state" />');
				$('select#id_city').remove();
				$('#address .ad-city #id_city').remove();
				$('#address .ad-city').append('<input id="id_city" type="text" value="' + data.city + '" name="_city" readonly="readonly"/>');
				$('#address .ad-city').append('<input id="id_city" type="hidden" value="' + data.city + '" name="city" />');
				$('select#id_area').remove();
				$('#address .ad-area #id_area').remove();
				$('#address .ad-area').append('<input id="id_area" type="text" value="' + data.area + '" name="_area" readonly="readonly"/>');
				$('#address .ad-area').append('<input id="id_area" type="hidden" value="' + data.id_area + '" name="area" />');
				// Anuncie
				$('input#id_address').val(data.address);
				$('input#id_area').val(data.area).attr('readonly', 'readonly');
				$('.small-column .selbox').remove();
				$('._state .border-left').remove();
				$('._state').append('<div class="border-left"><div class="border-right small"><input id="id_state" type="text" maxlength="64" value="' + data.state + '" name="state" readonly="readonly"></div></div>');
				$('input#id_city').val(data.city).attr('readonly', 'readonly');
				$('#id_complement').val('');
			}
		},'json');
	}

	if($('input#id_zip_code').length && $('body').find('input#id_zip_code').val() !== ""){
		load_cep($('#id_zip_code').val());
	}

	$('#id_zip_code').mask('99999-999', {
		completed : function() {
			$('.cep-carregando').show();
			load_cep(this.val());

		}
	});

	$('#id_zip_code').blur(function(){
		if ($(this).val() !== ""){
			load_cep($('#id_zip_code').val());
		}
	});

	// base.html para atualizar as cidades no topo
	// Atualiza select de cidade de acordo com o estado
	$('form#search-form .state select#id_state').change(function(){
		$.post('/locations/refresh-city/', {'state': $(this).val()}, function(data){
			$('form#search-form .city .selbox').remove();
			$('form#search-form .city select#id_locale option').remove();
			var UF = $('form#search-form .state .selbox a.selected-focus').text();
			if(UF ==='UF'){
		        $('form#search-form .city select#id_locale').append('<option value="0"> Todas cidades</option>');
		        $('form#search-form').submit();
			}else{
			    $('form#search-form .city select#id_locale').append('<option value="0"> Selecione uma cidade </option>');
			}
			if ( data.city ){
				$.each(data.city, function(i, city){
					$('form#search-form .city select#id_locale').append('<option value="'+ city.city +'">'+ city.city__city +'</option>');
				});
			}
			$('#search-form select#id_locale').selectreplace({width:142, height:22, scrollAfter:6});
		},'json');
	});

	// calcula o valor da assinatura no plano
	$('#sign-up #id_plan').change(function(){
		var price = $(this).find(':selected').text().split('R$')[1],
			total = price * $('#id_number_ads').val();
		$('#total-value').val(total);
		$('#value_signature').text(total);
	});

	$('#sign-up #id_plan').change(function(){
		var price = $('#id_number_ads').val(),
			total = price * $(this).val();
		$('#value_signature').text(total.toFixed(2));
	});

	$('#sign-up #id_number_ads').blur(function(){
		var price = $('#id_plan :selected').text().split('R$')[1],
			total = price * $(this).val();
		$('#value_signature').text(total.toFixed(2));
	});

	$('#new-voucher form #id_discount').blur(function(){
		var discount = $(this).val();
		discount = discount.replace(",", ".");
		$(this).val(discount);
	});

	$('#new-voucher form #id_price').blur(function(){
		var price = $(this).val();
		price = price.replace(',', '.');
		$(this).val(price);
	});

	$('#new-voucher form #id_discount').blur(function(){
		var price = $('#new-voucher form #id_price').val();
		var discount = $(this).val();
		var discounted_price = price - ((price * discount) / 100);
		var the_savings = (price - discounted_price);
		$('#new-voucher form #id_discouted_price').val(discounted_price.toFixed(2));
		$('#new-voucher form #the_savings').val(the_savings.toFixed(2));
	});

	$('#new-voucher form #id_price').blur(function(){
		var price = $(this).val();
		var discount = $('#new-voucher form #id_discount').val();
		var discounted_price = price - ((price * discount) / 100);
		var the_savings = (price - discounted_price);
		$('#new-voucher form #id_discouted_price').val(discounted_price.toFixed(2));
		$('#new-voucher form #the_savings').val(the_savings.toFixed(2));
	});

	var price = $('#ad .article .promotion .share .price p.price').text().replace("R$", "");
	var discounted_price = $('#ad .article .promotion .share .price p.discounted_price').text().replace("R$", "");;
	var the_savings = price - discounted_price;
	$('#ad .article .promotion .share .price p.the_savings').text('R$'+the_savings.toFixed(2));

	if($('#new-voucher .article form .type #id_type_promotion').val() == 'valley_toast'){
		$('#new-voucher .article form .hide').hide();
		$('#new-voucher .article form .price #id_discount').val('');
		$('#new-voucher .article form .price #id_discouted_price').val('');
		$('#new-voucher .article form .price #the_savings').val('');
		$('#new-voucher .article form .active label').text('Vale-brinde ativo');
		$('#new-voucher .article form .active span').text('Desmarcar para desativar vale-brinde.');
		$('#new-voucher .article form .date label[for="id_limit_vouchers"]').text('Limite vale-brinde:');
		$('#new-voucher .article form input[type="submit"]').attr('value', 'Criar vale-brinde');
		$('#new-voucher .article form .price').addClass('valley-large');
		$('#new-voucher .article form .price label[for="id_price"]').text('Ganhe um brinde no valor de:');
	}else{
		$('#new-voucher .article form .price').show();
		$('#new-voucher .article form .active label').text('Cupom ativo');
		$('#new-voucher .article form .active span').text('Desmarcar para desativar Cupom.');
		$('#new-voucher .article form .date label[for="id_limit_vouchers"]').text('Limite de cupons:');
		$('#new-voucher .article form input[type="submit"]').attr('value', 'Criar cupom');
		$('#new-voucher .article form .price').removeClass('valley-large');
		$('#new-voucher .article form .price label[for="id_price"]').text('De');
	}

	$('#new-voucher .article form .type #id_type_promotion').change(function(){
		if( $(this).val() == 'valley_toast'){
			$('#new-voucher .article form .hide').hide();
			$('#new-voucher .article form .price #id_discount').val('');
			$('#new-voucher .article form .price #id_discouted_price').val('');
			$('#new-voucher .article form .price #the_savings').val('');
			$('#new-voucher .article form .active label').text('Vale-brinde ativo');
			$('#new-voucher .article form .active span').text('Desmarcar para desativar vale-brinde.');
			$('#new-voucher .article form .date label[for="id_limit_vouchers"]').text('Limite vale-brinde:');
			$('#new-voucher .article form input[type="submit"]').attr('value', 'Criar vale-brinde');
			$('#new-voucher .article form .price').addClass('valley-large');
			$('#new-voucher .article form .price label[for="id_price"]').text('Ganhe um brinde no valor de:');
		}else{
			$('#new-voucher .article form .price').show();
			$('#new-voucher .article form .active label').text('Cupom ativo');
			$('#new-voucher .article form .active span').text('Desmarcar para desativar Cupom.');
			$('#new-voucher .article form .date label[for="id_limit_vouchers"]').text('Limite de cupons:');
			$('#new-voucher .article form input[type="submit"]').attr('value', 'Criar cupom');
			$('#new-voucher .article form .price').removeClass('valley-large');
			$('#new-voucher .article form .price label[for="id_price"]').text('De');
		}
	});

	$('#new-voucher .article form .img-promotion #id_image').change(function(){
		$('#new-voucher .article form .img-promotion span.success').show();
		$('#new-voucher .article form .img-promotion label').addClass('align');

	})

});

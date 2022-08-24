;document.addEventListener('DOMContentLoaded', () => {


	// charts
	const options = {
		colors:['#4A72FE', '#7D9AFF', '#9C27B0'],
		series: [
			{
				name: "DM's",
				data: ['300', '250', '320', '480', '370', '450', '335']
			}
		],
		chart: {
			height: 220,
			width: '100%',
			type: 'area',
			toolbar: false,
		},
		dataLabels: {
			enabled: false
		},
		stroke: {
			curve: 'smooth',
			width: 5
		},
		xaxis: {
			categories: ["1 June", "2 June", "3 June", "4 June", "5 June", "6 June", "7 June"],
			labels: {
				// offsetX: 1,
				style: {
					colors: '#A2A2AC',
					fontSize: '11px'
				}
			},
			tooltip: {
				enabled: false
			}
		},
		yaxis: {
			show: false
		},
		grid: {
			borderColor: '#dfdfdf',
			strokeDashArray: 8,
			yaxis: {
				lines: {
					show: false
				}
			},
			xaxis: {
				lines: {
					show: true
				}
			},
			padding: {
				left: 50,
				right: 50
			}
		},
		tooltip: {
			custom: function({series, seriesIndex, dataPointIndex, w}) {
				return `
					<div class="chart-tooltip">
						<div class="daly">Sended daly</div>
						<div class="num">${series[seriesIndex][dataPointIndex]}k DM\'s</div>
					</div>
				`;
			}
		}
	};

	const chartContainer1 = document.querySelector('.js-chart');
	const chartContainer2 = document.querySelector('.js-chart-animation');
	const chart1 = new ApexCharts(chartContainer1, options);
	const chart2 = new ApexCharts(chartContainer2, options);
	
	if (chartContainer1 != null) chart1.render();
	if (chartContainer2 != null) {
		chart2.render();

		const seriesData = [
			['300', '250', '320', '480', '370', '450', '335'],
			['370', '450', '335', '300', '250', '320', '120'],
			['400', '100', '250', '320', '450', '700', '480']
		];

		let counter = 0;

		setInterval(function(){
			if (counter == 3) counter = 0;

			// white popups
			$('.home-chart .popup-item').removeClass('active');
			$('.home-chart .popup-item').eq(counter).addClass('active');

			// user anims
			$('.home-chart .imgs-wrap .img').removeClass('anim-1 anim-2');
			
			if (counter == 1) {
				$('.home-chart .imgs-wrap .img').addClass('anim-1');
			} else if (counter == 2) {
				$('.home-chart .imgs-wrap .img').addClass('anim-2');
			}

			changeSeries(seriesData[counter++])
		}, 2000);


		function changeSeries(data){
			chart2.updateOptions({
				series: [
					{
						name: "DM's",
						data: data
					}
				]
			})
		}
	}

	// user info toggle
	$('.js-user-info').click(function(){
		$(this).parents('.user-wrap').find('.popup-wrap').toggleClass('active');
	});

	$(document).click(function(event) { 
		var $target = $(event.target);

		if( !$target.closest('.header-main .user-wrap').length ) {
			$('.header-main .user-wrap .popup-wrap').removeClass('active');
		}
	});


	// toggle nav
	$('.js-toggle-nav').click(function(){
		$(this).toggleClass('active');
		$('nav.nav-wrap').toggleClass('active');
	});


	// header fixed
	$(window).scroll(() => {
		if ( $(window).scrollTop() >= 10 ) {
			$('header.header-main').addClass('fixed')
		} else {
			$('header.header-main').removeClass('fixed');
		}
	});

	// menu toggle btn
	$('.js-toggle-menu').click(() => {
		$('.js-toggle-menu, .header-main .menu-wrap').toggleClass('active');
	});

	// menu inner toggle
	$('.js-toggle-inner').click(function(){
		const $ul = $(this).parents('li').find('ul.inner');

		$(this).toggleClass('open');
		$ul.slideToggle(250);
	});

	// menu hide on scroll
	$(window).scroll(() => {
		$('.js-toggle-menu, .header-main .menu-wrap').removeClass('active');
		$('.js-toggle-nav, nav.nav-wrap').removeClass('active');
	});

	// live orders
	// setInterval(function(){
	// 	const random = Math.floor(Math.random() * (4 - 1 + 1)) + 1;
	// 	const $liveItem = $('.home-orders .items .item:nth-child('+random+')').clone();
	// 	$('.home-orders .items').prepend($liveItem);

	// 	$('.home-orders .items .item:last-child').remove();
	// }, 5000);

	// faq accordione
	$('.js-accordione').click(function(){
		const parent = $(this).parents('.item');
		const text = parent.find('.text-wrap');

		text.stop().slideToggle(300);
		parent.toggleClass('active');
	});

	// popup
	$('.js-popup').magnificPopup({
		closeMarkup: `<button class="mfp-close"><svg viewBox="0 0 22 22" width="22px"><use xlink:href="./img/sprite.svg#ic-close"></use></svg></button>`
	});

	// toggle deposit
	$('.js-toggle-deposit').click(function(){
		$('.js-toggle-deposit').removeClass('active');
		$(this).addClass('active');
	});

	// toggle password
	$('.js-toggle-password').click(function(){
		$(this).toggleClass('show');
		const $input = $(this).parents('.input-wrap').find('input');

		if ( $(this).hasClass('show') ) {
			$input.attr('type', 'text')
		} else {
			$input.attr('type', 'password')
		}
	});


	// tooltip
	new jBox('Tooltip', {
		attach: '.js-tooltip'
	});

	// tab order
	$('.js-tab-btn').click(function(){
		const tab = $(this).data('tab');
		$('.js-tab-btn').removeClass('active');
		$(this).addClass('active');

		$('.order-dms-main .tab-content').removeClass('active');
		$('.order-dms-main .tab-content[data-tab='+tab+']').addClass('active');

		// upade range amount
		const range = $(`.js-range-${tab}`).data("ionRangeSlider");
		const rangeIndex = range.old_from || 0;
		$('.js-price-amount').text(rangeValues[tab].pricePerAmount[rangeIndex]);
		console.log(range);
	});

	const rangeValues = {
		instagram: {
			amount: ['20k', '50k', '100k', '150k', '200k', '300k', '400k', '500k', '600k', '700k', '800k', '1m', '1.5m', '2m', '3m', '4m', '5m'],
			pricePer1k: ['4$ per 1k', '3$ per 1k', '2.8$ per 1k', '2.8$ per 1k', '2.5$ per 1k', '2.5$ per 1k', '2$ per 1k', '2$ per 1k', '2$ per 1k', '1.9$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.5$ per 1k'],
			pricePerAmount: ['80$', '150$', '280$', '420$', '560$', '750$', '920$', '1000$', '1200$', '1400$', '1520$', '1700$', '2550$', '3400$', '5100$', '6800$', '7500$'],
			percent: ['0%', '25%', '30%', '30%', '30%', '38%', '43%', '50%', '50%', '50%', '53%', '57%', '57%', '57%', '57%', '57%', '63%']
		},
		twitter: {
			amount: ['10k', '50k', '75к', '100k', '150к', '200k', '250к', '300k', '500k', '600к', '700k', '1m'],
			pricePer1k: ['25$ per 1k', '22$ per 1k', '22$ per 1k', '20$ per 1k', '20$ per 1k', '18$ per 1k', '18$ per 1k', '18$ per 1k', '17$ per 1k', '17$ per 1k', '17$ per 1k', '15$ per 1k'],
			pricePerAmount: ['250$', '1100$', '1650$', '2000$', '3000$', '3600$', '4500$', '5400$', '8500$', '10200$', '11900$', '15000$'],
			percent: ['0%', '12%', '12%', '20%', '20%', '28%', '28%', '28%', '32%', '32%', '32%', '40%']
		},
		discord: {
			amount: ['10k', '50k', '75к', '100k', '150к', '200k', '250к', '300k', '500k', '600к', '700k', '1m'],
			pricePer1k: ['25$ per 1k', '22$ per 1k', '22$ per 1k', '20$ per 1k', '20$ per 1k', '18$ per 1k', '18$ per 1k', '18$ per 1k', '17$ per 1k', '17$ per 1k', '17$ per 1k', '15$ per 1k'],
			pricePerAmount: ['250$', '1100$', '1650$', '2000$', '3000$', '3600$', '4500$', '5400$', '8500$', '10200$', '11900$', '15000$'],
			percent: ['0%', '12%', '12%', '20%', '20%', '28%', '28%', '28%', '32%', '32%', '32%', '40%']
		},
		telegram: {
			amount: ['10k', '20к', '30k', '40k', '50k', '60к', '70k', '100k', '120к', '150k', '300k'],
			pricePer1k: ['40$ per 1k', '39$ per 1k', '39$ per 1k', '38$ per 1k', '37$ per 1k', '37$ per 1k', '37$ per 1k', '36$ per 1k', '36$ per 1k', '36$ per 1k', '35$ per 1k'],
			pricePerAmount: ['400$', '780$', '1170$', '1520$', '1850$', '2220$', '2590$', '3600$', '4320$', '5400$', '10500$'],
			percent: ['0%', '3%', '3%', '5%', '8%', '8%', '8%', '10%', '10%', '10%', '13%']
		}
	}

	// input range
	initRange('instagram');
	initRange('twitter');
	initRange('discord');
	initRange('telegram');

	function initRange(social){
		$(`.js-range-${social}`).ionRangeSlider({
			skin: 'round',
			grid: true,
			hide_min_max: true,
			hide_from_to: true,
			values: rangeValues[social].amount,
			onChange: range,
			onStart: range
		});

		// range on change
		function range(data){
			const index = +data.from_pretty || 0;
			const val = rangeValues[social].amount[index];
			const $parent = $(`.js-range-${social}`).parents('.block-social-calculator');

			const $amount = $parent.find('.js-amount');
			const $pricePer1k = $parent.find('.js-price-per-1k');
			const $pricePerAmount = $parent.find('.js-price-per-amount');
			const $percent = $parent.find('.js-percent');

			const pricePer1k = rangeValues[social].pricePer1k[index];
			const pricePerAmount = rangeValues[social].pricePerAmount[index];
			const percent = rangeValues[social].percent[index];
			
			$amount.text(val);
			$pricePer1k.text(pricePer1k);
			$pricePerAmount.text(pricePerAmount);
			$percent.text(percent);

			// global amount
			$('.js-price-amount').text(pricePerAmount);
		}
	}



	// swiper calc home
	const swiper = new Swiper('.js-swiper-calc', {
		effect: 'coverflow',
		grabCursor: false,
		centeredSlides: true,
		// width: 280,
		allowTouchMove: false,
		coverflowEffect: {
			rotate: 0,
			stretch: 123,
			depth: 425,
			modifier: 1,
			slideShadows: false,
		},
		navigation: {
			nextEl: '.js-swiper-next',
			prevEl: '.js-swiper-prev'
		},
		breakpoints: {
			561: {
				width: 380
			}
		}
	});

	$('.js-swiper-to').click(function(){
		const index = +$(this).data('index');
		swiper.slideTo(index);
	});




	// scroll to block
	$('[data-scroll-from]').click(function(e){
		if ( $('.is-home').length  == 0) return; // in not home page

		e.preventDefault();
		const scroll = $(this).attr('data-scroll-from');

		$('html, body').animate({
			scrollTop: $('[data-scroll-to='+scroll+']').offset().top
		}, 1000);
	});







	jQuery.fn.ForceNumericOnly =
	function()
	{
	    return this.each(function()
	    {
	        $(this).keydown(function(e)
	        {
	            var key = e.charCode || e.keyCode || 0;
	            // allow backspace, tab, delete, enter, arrows, numbers and keypad numbers ONLY
	            // home, end, period, and numpad decimal
	            return (
	                key == 8 || 
	                key == 9 ||
	                key == 13 ||
	                key == 46 ||
	                key == 110 ||
	                key == 190 ||
	                (key >= 35 && key <= 40) ||
	                (key >= 48 && key <= 57) ||
	                (key >= 96 && key <= 105));
	        });
	    });
	};

	$('.js-input-numeric').ForceNumericOnly();


	// textarea max
	$('.js-textarea-max').keyup(function(){
		const characterCount = $(this).val().length;
		const $parent = $(this).parents('.textarea-counter-wrap');
		const $current = $parent.find('span.current');
		const $maximum = $parent.find('span.max');

		$current.text(characterCount);
	});


	// textarea auto height
	$(function() {
	    //  changes mouse cursor when highlighting loawer right of box
	    $(document).on('mousemove', 'textarea', function(e) {
			var a = $(this).offset().top + $(this).outerHeight() - 16,	//	top border of bottom-right-corner-box area
				b = $(this).offset().left + $(this).outerWidth() - 16;	//	left border of bottom-right-corner-box area
			$(this).css({
				cursor: e.pageY > a && e.pageX > b ? 'nw-resize' : ''
			});
		})
	    //  the following simple make the textbox "Auto-Expand" as it is typed in
	    .on('keyup', 'textarea', function(e) {
	        //  the following will help the text expand as typing takes place
	        while($(this).outerHeight() < this.scrollHeight + parseFloat($(this).css("borderTopWidth")) + parseFloat($(this).css("borderBottomWidth"))) {
	            $(this).height($(this).height()+1);
	        };
	    });
	});


	// popup cookies
	$('.js-close-cookies').click(function(){
		$('.popup-cookies').fadeOut(250);
	});


	// home numbers animation
	$(window).scroll(testScroll);
		var viewed = false;

		function isScrolledIntoView(elem) {
		    var docViewTop = $(window).scrollTop();
		    var docViewBottom = docViewTop + $(window).height();

		    var elemTop = $(elem).offset().top;
		    var elemBottom = elemTop + $(elem).height();

		    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
		}

		function testScroll() {
		  if (isScrolledIntoView($(".js-numbers-anim")) && !viewed) {
		      viewed = true;
		      $('.value').each(function () {
		      $(this).prop('Counter',0).animate({
		          Counter: $(this).text()
		      }, {
		          duration: 4000,
		          easing: 'swing',
		          step: function (now) {
		              $(this).text(Math.ceil(now));
		          }
		      });
		    });
		  }
	}


});
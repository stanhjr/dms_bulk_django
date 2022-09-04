
// old range data

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



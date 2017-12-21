/*
	Project Name : Directin
	Author Company : Ewebcraft
	Project Date: 01 Aug , 2016
	Author Website : http://www.ewebcraft.com
	Author Email : ewebcraft@gmail.com
*/

$(window).load(function(){
    $('#loader').fadeOut("slow");
});

(function($) {
    
	"use strict";

	/************** add listings form signup and signin *******************/
	// $("#user-signup").hide();
	$("span#sign-up").on('click',function(){
		$("form#user-signin,form#user-signup").toggleClass('hide-form');
		$(this).addClass('selected');
		$("#sign-in").removeClass('selected');
	});
	$("span#sign-in").on('click',function(){
		$("form#user-signin,form#user-signup").toggleClass('hide-form');
		$(this).addClass('selected');
		$("#sign-up").removeClass('selected');
	});
	
	// $('#user-option p span').on('click',function() {
	// 	e.preventDefault(); //prevent the link from being followed
	// 	$('#user-option p span').removeClass('selected');
	// 	$(this).addClass('selected');
	// });
	
	/******************* add search categories *******************/
	$("#search-categories-boxes1").hide();
		$("button.search-category").on('click',function() {
        $("#search-categories-boxes1").slideToggle();
			$("button.search-category").html(function(i, v){
		   		return v === '<i class="fa fa-bars"></i> View Less' ? '<i class="fa fa-bars"></i> View More' : '<i class="fa fa-bars"></i> View Less';
		});
    });
	
	/****************** coutter *******************/
	//success count
	if($(".success-count").length > 0)
	{
		$('.success-count').counterUp({
			delay:20,
			time:2000
		});
	}

	
	/************** client slider ****************/

	$('#client-slider .client-carousel').bxSlider({
	   minSlides: 1,
	   maxSlides: 6,
	   slideWidth:175,
	   slideMargin: 10,
	   moveSlides: 1,
	   controls: false,
	   pager: false,
	   auto: true,
	   autoStart: true,
	   autoHover: true,
	   infiniteLoop: true,
	   speed: 4000,
	   pause: 0,
	   easing: 'linear',
	   responsive: true,
	   autoDirection: 'next',
	   useCSS: false,
	   preventDefaultSwipeX: false,
	   preventDefaultSwipeY: true,
	   touchEnabled: false,
	});
	
	/*********************** disable class to select *****************/
	$('select#parentCategory').on('change', function() {
	 var optionValue=this.value ; 
	 if(optionValue!==0){
		   $('#subCategory').removeAttr('disabled');
		 }
		 if(optionValue===0){
		   $('#subCategory').attr('disabled','');
		 }
	 });
	 
	 /*************************** add more images ************************/
	$('span.addsection').on('click',function() {
    $('#add-new-imagess .col-sm-6,#add-new-images .col-md-4').each(function () {
        if ($(this).css('display') === 'none') {
            $(this).css('display', 'block');
            return false;
        }
    });
		var i = 0;
		$('#add-new-imagess .col-sm-6,#add-new-images .col-md-4').each(function () {
			if ($(this).css('display') !=='none') {
				i++;
			}
		});
	
		if (i === 6) 
		{
			$('span.addsection').css("color","#cccccc");
		}
	});
})(jQuery);
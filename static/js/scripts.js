$(".testi3").owlCarousel({
  loop: true,
  margin: 30,
  nav: false,
  dots: true,
  autoplay: true,
  responsiveClass: true,
  responsive: {
      0: {
          items: 1,
          nav: false,
      },
      1024: {
          items: 3,
      },
  },
});

$(window).scroll(function () {
  var sticky = $(".site-header"),
      scroll = $(window).scrollTop();
  if (scroll >= 100) sticky.addClass("fixed-header");
  else sticky.removeClass("fixed-header");
});

$(".more-details").click(function () {
  $(".policy-details").slideDown();
});

$("#close").click(function () {
  $(".policy-details").slideUp();
});

//-------------DatePicker Single
$(function () {
//  $("#datepicker").datepicker();
});
//-------------DatePicker Double
$(function () {
//  $(".from").datepicker({
//      onClose: function (selectedDate) {
//          $(".to").datepicker("option", "minDate", selectedDate);
//      },
//  });
//  $(".to").datepicker({
//      onClose: function (selectedDate) {
//          $(".from").datepicker("option", "maxDate", selectedDate);
//      },
//  });
});

// Change tab class and display content
// tabbed content
$(".tab_content").hide();
$(".tab_content:first").show();

/* if in tab mode */
$("ul.tabs li").click(function () {
  $(".tab_content").hide();
  var activeTab = $(this).attr("rel");
  $("#" + activeTab).fadeIn();

  $("ul.tabs li").removeClass("active");
  $(this).addClass("active");

  $(".tab_drawer_heading").removeClass("d_active");
  $(".tab_drawer_heading[rel^='" + activeTab + "']").addClass("d_active");
});
/* if in drawer mode */
$(".tab_drawer_heading").click(function () {
  $(".tab_content").hide();
  var d_activeTab = $(this).attr("rel");
  $("#" + d_activeTab).fadeIn();

  $(".tab_drawer_heading").removeClass("d_active");
  $(this).addClass("d_active");

  $("ul.tabs li").removeClass("active");
  $("ul.tabs li[rel^='" + d_activeTab + "']").addClass("active");
});

/* Extra class "tab_last"
   to add border to right side
   of last tab */
$("ul.tabs li").last().addClass("tab_last");

// $(document).ready(function (){
//     $(document).on('click','.nav-item',function(e){
//         e.preventDefault();
//         var href=$(this).children().attr('href');
//         $(".nav-item").removeClass("active");
//         $(this).addClass("active");
//
//         $.ajaxSetup({
//             headers: {
//                 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
//             }
//         });
//         $.ajax({
//             type:"GET",
//             url:href,
//             success:function (data){
//                 console.log(data);
//             }
//         });
//
//
//
//
//
//
//     });
// });




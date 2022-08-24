//hide year of manufacture, engine capacity and valuation if not comprehensive
$(document).ready(function(){

$('.yom').hide();
    $(".ecc").hide();
    $(".estValue").hide();
    $('#yom').removeAttr('required');
    $('#estValue1').hide();
    $('#ecc').removeAttr('required');
    $('#estValue').removeAttr('required');
    $('#yom').removeAttr('data-error');
    $('#ecc').removeAttr('data-error');
    $('#estValue').removeAttr('data-error');



$("#category").change(function(e) {
//alert("category");
  if ($(this).val() == "comprehensive") {
    $('.yom').show();
    $('.ecc').show();
    $('.estValue').show();
    $('#yom').attr('required', '');
    $('#ecc').attr('required', '');
    $('#estValue').attr('required', '');
    $('#yom').attr('data-error', 'Indicate the year of manufacture');
    $('#ecc').attr('data-error', 'Indicate the engine capacity (cc)');
    $('#estValue').attr('data-error', 'Indicate the valuation (click link above to value)');
  } else {
    $('.yom').hide();
    $(".ecc").hide();
    $(".estValue").hide();
    $('#yom').removeAttr('required');
    $('#estValue1').hide();
    $('#ecc').removeAttr('required');
    $('#estValue').removeAttr('required');
    $('#yom').removeAttr('data-error');
    $('#ecc').removeAttr('data-error');
    $('#estValue').removeAttr('data-error');
  }
});

//hide tonnage if insurance type is private
$("#usage").change(function() {
  if ($(this).val() == "private"){
    $('#tonage').removeAttr('required');
    $('#tonage').removeAttr('data-error');
    $('.tonage').hide();
    $('.pc').hide();
  } else {
    $('.tonage').show();
    $('.pc').show();

    $('#tonage').attr('required', '');
    $('#tonage').attr('data-error', 'Indicate the tonage(weight) of the vehicle');
  }
});

//hide seating capacity if insurance type not psv
$("#coverType").change(function() {
  if ($(this).val() == "psv" ){
    $('#pc').attr('required', '');
    $('#pc').attr('data-error', 'Indicate the seating capacity(passenger only)');
  } else {
    $('#pc').removeAttr('required');
    $('#pc').removeAttr('data-error');
  }
});

$("#coverType").change(function() {
  if ($(this).val() == "private" ){
   $('#tonage').removeAttr('required');
    $('#tonage').removeAttr('data-error');
    $('.tonage').hide();
    $('.pc').hide();
  } else {
    $('.tonage').show();
    $('.pc').show();

    $('tonage').attr('required', '');
    $('#tonage').attr('data-error', 'Indicate the tonage(weight) of the vehicle');
  }
});

//hide seating capacity and tonage if motorcycle
$("#vtype").change(function() {
  if ($(this).val() == "motor_cycle"){
     $('.pc').hide();
    $('.tonage').hide();
    $('#pc').removeAttr('required');
    $('#tonage').removeAttr('required');
  }
});

});


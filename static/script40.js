//hide year of manufacture, engine capacity and valuation if not comprehensive
$("#coverType").change(function() {
  if ($(this).val() == "comprehensive") {
    $('#yom').show();
    $('#eng_cap').show();  
    $('#estmValue').show();  
    $('#Year').attr('required', '');
    $('#engineCapacity').attr('required', '');  
    $('#valuation').attr('required', '');  
    $('#Year').attr('data-error', 'Indicate the year of manufacture');
    $('#engineCapacity').attr('data-error', 'Indicate the engine capacity (cc)');  
    $('#valuation').attr('data-error', 'Indicate the valuation (click link above to value)');  
  } else {
    $('#yom').hide();
    $('#eng_cap').hide();  
    $('#estmValue').hide();   
    $('#Year').removeAttr('required');
    $('#engineCapacity').removeAttr('required');  
    $('#valuation').removeAttr('required'); 
    $('#Year').removeAttr('data-error');  
    $('#engineCapacity').removeAttr('data-error');
    $('#valuation').removeAttr('data-error');  
  }
});

//hide tonnage if insurance type is private
$("#insuranceType").change(function() {
  if ($(this).val() == "private"){
    $('#netWeight').hide();
    $('#tonage').removeAttr('required');
    $('#tonage').removeAttr('data-error');
  } else {
    $('#netWeight').show();
    $('#tonage').attr('required', '');
    $('#tonage').attr('data-error', 'Indicate the tonage(weight) of the vehicle');
  }
});

//hide seating capacity if insurance type not psv
$("#insuranceType").change(function() {
  if ($(this).val() == "psv"){
    $('#seat_cap').show();
    $('#seatingCapacity').attr('required', '');
    $('#seatingCapacity').attr('data-error', 'Indicate the seating capacity(passenger only)');
  } else {
    $('#seat_cap').hide();
    $('#seatingCapacity').removeAttr('required');
    $('#seatingCapacity').removeAttr('data-error');
  }
});

//hide seating capacity and tonage if motorcycle
$("#body_type").change(function() {
  if ($(this).val() == "motor_cycle"){
    $('#seat_cap').hide();
    $('#netWeight').hide();  
    $('#seatingCapacity').removeAttr('required');
    $('#tonage').removeAttr('required');  
  }
});                                                    


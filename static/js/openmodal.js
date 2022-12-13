$('#narratModal').on('hide.bs.modal', function() {
  let val = $('.myInput').val();
  $('#cash_narrat').val(val);
})
$( document ).ready(function() {
    $('.variation-input').change(function(){
        var slug = $(this).data('slug');
        var previous = parseInt($(this).attr('data-previous'));
        var quantity = parseInt($(this).val());
        var price = parseInt($(this).attr('data-price'));
        var subtotal = price * quantity;
        var total = parseInt($('#table-total-value').html().substring(1, $('#table-total-value').html().length))+subtotal-(previous*price);
        $('#table-' + slug).find('.table-price').html('₱' + subtotal + '.00');
        $('#table-' + slug).find('.subtitle').html('x ' + quantity);
        $('#table-total-value').html('₱' + total + '.00');
        $(this).attr('data-previous', quantity);
    });

    if($("#claiming-Shipping:checked").val()?true:false) {
        $("#table-shipping").show();
    }
    else {
        $("#table-shipping").hide();
    }
    $('.claiming').change(function(){
        var price = $('#table-shipping').attr('data-price');
        var total = parseInt($('#table-total-value').html().substring(1, $('#table-total-value').html().length));

       if($("#claiming-Shipping:checked").val()?true:false) {
            total += price;
            $("#table-shipping").show();
            $('#table-total-value').html('₱' + total + '.00');
       }
       else {
            total -= price;
            $("#table-shipping").hide();
            $('#table-total-value').html('₱' + price + '.00');
       }
    });
});

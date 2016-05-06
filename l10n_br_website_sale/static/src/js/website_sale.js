$(document).ready(function() {

    $('.oe_website_sale').each(function() {
        var oe_website_sale = this;

        $(oe_website_sale).on('change', "select[name='state_id']", function() {
            var vals = { 'state_id': $(this).val() };
            openerp.jsonRpc("/shop/get_cities", 'call', vals)
                .then(function(data) {
                    $('#select_l10n_br_city_id').find('option').remove().end();
                    var selected = $('#l10n_br_city_id').val();
                    $('#select_l10n_br_city_id').append('<option value="">Cidade...</option>');
                    $.each(data, function(i, item) {
                        $('#select_l10n_br_city_id').append($('<option>', {
                            value: item[0],
                            text: item[1],
                            selected: item[0]==selected?true:false,
                        }));
                    });
                });
            });
        $(oe_website_sale).find("select[name='state_id']").change();

        $(oe_website_sale).on('change', "select[name='shipping_state_id']", function() {
            var vals = { 'state_id': $(this).val() };
            openerp.jsonRpc("/shop/get_cities", 'call', vals)
                .then(function(data) {
                    $('#select_shipping_l10n_br_city_id').find('option').remove().end();
                    var selected = $('#shipping_l10n_br_city_id').val();
                    $('#select_shipping_l10n_br_city_id').append('<option value="">Cidade...</option>');
                    $.each(data, function(i, item) {
                        $('#select_shipping_l10n_br_city_id').append($('<option>', {
                            value: item[0],
                            text: item[1],
                            selected: item[0]==selected?true:false,
                        }));
                    });
                });
            });
        $(oe_website_sale).find("select[name='state_id']").change();
    });
});

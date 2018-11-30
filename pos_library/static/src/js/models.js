odoo.define('pos_library.models', function (require) {

    "use strict";

    var models = require('point_of_sale.models');

    var core = require('web.core');
    var time = require('web.time');

    models.load_fields('res.partner', ['current_rental_ids']);
    models.load_fields('product.product', [
        'book',
        'book_state',
        'edition_date',
        'isbn',
        'acquisition_year',
        'acquisition_price'
    ]);

    models.load_models([{
        model: 'library.rental',
        label: 'Rentals',
        fields: ['rental_date', 'return_date', 'customer_id', 'book_id'],
        ids: function (self, tmp) {
            var rental_ids = [];
            _(self.partners).each(function (p) {
                rental_ids.push(p.current_rental_ids);
            });
            return _.flatten(rental_ids);
        },
        loaded: function (self, rentals) {

            var str2date = time.str_to_date;
            var date_format = time.getLangDateFormat();

            _(rentals).each(function (r) {
                r.display_rental_date = moment(str2date(r.rental_date)).format(date_format);
                r.display_return_date = moment(str2date(r.return_date)).format(date_format);
            });
            self.db.add_rentals(rentals);
        }
    }], {
        after: 'product.product'
    });

    var _super_product = models.Product.prototype;
    models.Product = models.Product.extend({
        initialize: function (attr, options) {
            _super_product.initialize.apply(this, arguments);

            if (!!this.book) {
                this.book_states = {
                    'available': core._t('Available'),
                    'rented': core._t('Rented')
                };

                var str2date = time.str_to_date;
                var date_format = time.getLangDateFormat();
                this.display_edition_date = moment(str2date(this.edition_date)).format(date_format);
            }
        }
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        add_product: function (product, options) {
            if (product.book_state !== 'available') {
                this.pos.gui.show_popup('error', {
                    title: core._t('Book Unavailable'),
                    body: core._t('The book "' + product.display_name + '", is not available for renting.')
                });
            } else {
                _super_order.add_product.apply(this, arguments);
            }
        }
    });

});

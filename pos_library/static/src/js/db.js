odoo.define('pos_library.DB', function (require) {

    "use strict";

    var PoSDB = require('point_of_sale.DB');

    PoSDB.include({
        add_products: function (products) {
            /*
            Override to filter out non books or lost books
             */
            if (!(products instanceof Array)) {
                products = [products];
            }

            var books = _(products).filter(function (p) {
                return !!p.book && p.book_state !== 'lost';
            });

            this._super(books);
        },
        add_rentals: function (rentals) {
            var stored_partners = this.partner_by_id;

            if (!(rentals instanceof Array)) {
                rentals = [rentals];
            }

            _(stored_partners).each(function (partner) {
                partner.rentals = _.filter(rentals, function (rental) {
                    return rental.customer_id[0] === partner.id;
                });

            });

            var rentals_by_product_id = {};
            _(rentals).each(function (r) {
                var product_id = r.book_id[0];
                if (_.contains(rentals_by_product_id, product_id)) {
                    rentals_by_product_id[product_id].push(r);
                } else {
                    rentals_by_product_id[product_id] = [r];
                }
            });
            this.rentals_by_product_id = rentals_by_product_id;
        },
        get_rentals_by_product_id: function (product_id) {
            return this.rentals_by_product_id[product_id] || [];
        }
    });

});

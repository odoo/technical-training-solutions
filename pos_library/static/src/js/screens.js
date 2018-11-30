odoo.define('pos_library.screens', function (require) {

    "use strict";

    var screens = require('point_of_sale.screens');

    screens.ClientListScreenWidget.include({
        display_client_details: function (visibility, partner, clickpos) {
            this._super.apply(this, arguments);

            if (visibility === 'show') {
                this.$('.rental-line').click(_.bind(this._rentalClick, this));
            }
        },
        _rentalClick: function (ev) {
            var $target = $(ev.currentTarget);
            var product_id = parseInt($target.data('book-id'), 10);
            var book = this.pos.db.get_product_by_id(product_id);

            this.gui.show_popup('book-details', {
                book: book
            });
        }
    });

});

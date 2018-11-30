odoo.define('pos_library.popups', function (require) {

    "use strict";

    var gui = require('point_of_sale.gui');

    var PopupWidget = require('point_of_sale.popups');

    var core = require('web.core');
    var QWeb = core.qweb;

    var BookDetailsPopupWidget = PopupWidget.extend({
        template: 'BookDetailsPopupWidget',
        show: function (options) {
            this._super(options);
            this.$('.book-details').replaceWith($(QWeb.render('BookDetails', {
                book: this.options.book
            })));
        }
    });

    gui.define_popup({
        name: 'book-details',
        widget: BookDetailsPopupWidget
    });

});

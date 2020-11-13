from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError


class RealEstate(http.Controller):
    _items_per_page = 3

    @http.route([
        '/estates', '/estates/page/<int:page>',
        '/estates/<model("estate.property.type"):propType>', '/estates/<model("estate.property.type"):propType>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=True)
    def AllEstate(self, propType=False, page=1, **kw):
        Estate = request.env['estate.property']

        estates = Estate  # empty record set
        if propType:
            estates = propType.property_ids
        else:
            estates = Estate.search([])

        offset = (page - 1) * self._items_per_page
        estates_to_display = estates[offset:offset + self._items_per_page]

        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=len(estates),
            page=page,
            step=self._items_per_page,
        )
        return request.render("estate.all_estates", {
            'pager': pager,
            'estates': estates_to_display,
            'types': request.env['estate.property.type'].search([]),
            'current_type': propType,
            'search': kw.get('search'),
        })

    @http.route(['/estate/<model("estate.property"):estate>'], type='http', auth="public", website=True, sitemap=True)
    def OneEstate(self, estate, **kw):
        return request.render("estate.one_estate", {
            'record': estate,
            'main_object': estate,
            'sections': [
                (_('Main'), ['bedrooms', 'living_area', 'facades', 'total_area']),
                (_('Exteriors'), ['garage', 'garden', 'garden_area', 'garden_orientation']),
            ]
        })

    @http.route(['/estate/offer/<model("estate.property"):estate>'], type='http', auth="user", website=True, sitemap=False, csrf=True)
    def offer(self, estate, **kw):
        errors = []
        offer_id = False
        if request.httprequest.method == "POST":
            if not kw.get('offer_price', '').isnumeric() or int(kw['offer_price']) < estate.expected_price:
                errors.append(_("<b>Price</b> is wrong or too small"))
            if not kw.get('offer_validity', '').isnumeric():
                errors.append(_("<b>Validity</b> is invalid"))

            if not errors:
                partner = request.env.user.partner_id
                vals = {}
                if kw.get('offer_email') and not partner.email:
                    vals['email'] = kw['offer_email']
                if kw.get('offer_phone') and not partner.phone:
                    vals['phone'] = kw['offer_phone']
                if vals:
                    partner.write(vals)  # avoid update of none value, or 2 update sql
                try:
                    offer_id = request.env["estate.property.offer"].sudo().create({
                        'price': int(kw['offer_price']),
                        'partner_id': partner.id,
                        'validity': int(kw['offer_validity']),
                        'property_id': estate.id,
                    })
                except UserError:
                    errors.append('<b>Sorry</b>: We already got a superior offer, we cannot register this one.')

        return request.render("estate.offer_form", {
            'record': estate,
            'offer_id': offer_id,
            'errors': errors,
            'kw': kw,
        })

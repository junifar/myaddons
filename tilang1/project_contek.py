from openerp.osv import osv, fields


class site(osv.osv):
    _name = 'project.site'
    _description = 'Site Information.'
    _columns = {
        'name': fields.char('Site Name', 128, required=True),
        'site_alias1': fields.char('Site Alias 1', 128),
        'site_alias2': fields.char('Site Alias 2', 128),
        'area_id': fields.many2one('project.area', string='Area', required=False),
        'island_id': fields.many2one('project.island', string='Pulau', required=False),
        'province_id': fields.many2one('project.province', string='Propinsi', required=False),
        'city_id': fields.many2one('project.city', string='Kabupaten / Kota', required=False),
        'field_type_id': fields.many2one('project.field.type', string='Field Type', required=False),
        'site_id_prasetia': fields.char('Site ID Prasetia', 128),
        'site_id_customer': fields.char('Site ID Customer', 128),
        'customer_id': fields.many2one('res.partner', string='Customer', required=False,
                                       domain=[('customer', '=', True)]),
        'tower_type_id': fields.many2one('project.tower.type', required=False, string='Tower Type'),
        'tinggi_tower_id': fields.many2one('project.tinggi.tower', required=False, string='Tinggi Tower'),
        'address': fields.text('Address', required=True),
        'project_ids': fields.one2many('project.project', 'site_id', 'Project'),
        'stock_location_in_id': fields.many2one('stock.location', string='Site Stock Location In', required=False),
        'stock_location_out_id': fields.many2one('stock.location', string='Site Stock Location Out', required=False)
    }
    _defaults = {
        'site_id_prasetia': "<Auto Generate ID>",
        # 'site_id_prasetia' : "<Get From EPM>",
    }

    def create(self, cr, uid, vals, context=None):

        #
        # Fungsi penomoran site di aktifkan di sini
        #
        if not context:
            context = {}
        sql_req = """SELECT
                            id,number_next
                        FROM
                            ir_sequence
                        WHERE
                          "prefix" = '%s'
                        ORDER BY id DESC"""
        pref = "TWR"
        cr.execute(sql_req % pref)
        try:
            hasil = cr.fetchone()
            vals['site_id_prasetia'] = pref + str("%05d" % hasil[1])
            sql_req = """UPDATE ir_sequence
                            SET
                                number_next = %s
                            WHERE
                                "id" = %s"""
            cr.execute(sql_req % (str(hasil[1] + 1), str(hasil[0])))
        except Exception, e:
            vals['site_id_prasetia'] = pref + str("%05d" % 1)
            sql_req = """INSERT INTO ir_sequence(
                                create_uid,
                                create_date,
                                write_date,
                                write_uid,
                                code,
                                suffix,
                                number_next,
                                number_increment,
                                "implementation",
                                company_id,
                                padding,
                                "prefix",
                                "name",
                                active) VALUES
                                (1,current_date,current_date,1,null,null,2,1,'standard',1,3,'%s','Prasetia ID0002',NULL)
                            """
            cr.execute(sql_req % pref)
        #
        # // Fungsi penomoran site di aktifkan di sini
        #

        # Auto create site location
        stock_obj = self.pool.get('stock.location')
        location_number = 1
        stock_location_id = {}
        # Run 2 Kali penambahan location / input & output
        # while location_number <= 2:
        while location_number <= 1:
            # if location_number == 1:
            # HARDCODE LOCATION ID STOCK FOR PARENT
            location_id = 12
            name = " Stock"
            loc_type = 'none'
            auto_pack = 'manual'
            # elif location_number == 2:
            # HARDCODE LOCATION ID OUTPUT FOR PARENT
            # location_id = 11
            # name = " Output"
            # loc_type = 'customer'
            # auto_pack = 'transparent'
            stock_location = {
                'name': vals['name'] + name,
                'location_id': location_id,
                'usage': 'internal',
                'chained_location_type': loc_type,
                'chained_auto_packing': auto_pack,
            }
            stock_location_id[location_number] = stock_obj.create(cr, uid, stock_location)
            location_number += 1

        vals['stock_location_in_id'] = stock_location_id[1]
        vals['stock_location_out_id'] = stock_location_id[1]

        return super(site, self).create(cr, uid, vals, context)


site()


class project(osv.osv):
    _inherit = 'project.project'
    _description = 'Inherit OpenERP Project Prasetia.'

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            if record.site_id:
                name = record.name + " - " + record.site_id.name
            else:
                name = record.name
            res.append((record.id, name))
        return res

    def _compute_stock_moves(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            stock_move_obj = self.pool.get('stock.move')
            stock_move_result = stock_move_obj.search(cr, uid, [('project_id', '=', project.id),
                                                                ('picking_id.state', 'in', ['assigned', 'done'])],
                                                      context=context)
            result[project.id] = stock_move_result
        return result

    def _compute_purchase_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            purchase_line_obj = self.pool.get('purchase.order.line')
            purchase_line_result = purchase_line_obj.search(cr, uid, [('project_id', '=', project.id),
                                                                      ('order_id.state', 'in', ['approved', 'done'])],
                                                            context=context)
            result[project.id] = purchase_line_result
        return result

    def _compute_sale_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            src = []
            sale_line_obj = self.pool.get('sale.order.line')
            sale_line_result = sale_line_obj.search(cr, uid, [('project_id', '=', project.id),
                                                              ('order_id.state', 'in', ['progress', 'done'])],
                                                    context=context)
            result[project.id] = sale_line_result
        return result

    def _compute_customer_invoices(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            src = []
            customer_invoice_obj = self.pool.get('account.invoice.line')
            customer_invoice_result = customer_invoice_obj.search(cr, uid, [('project_id', '=', project.id), (
                'invoice_id.state', 'in', ['open', 'paid']), ('invoice_id.type', '=', 'out_invoice')], context=context)
            result[project.id] = customer_invoice_result
        return result

    def _compute_supplier_invoices(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            supplier_invoice_obj = self.pool.get('account.invoice.line')
            supplier_invoice_result = supplier_invoice_obj.search(cr, uid, [('project_id', '=', project.id), (
                'invoice_id.state', 'in', ['open', 'paid']), ('invoice_id.type', '=', 'in_invoice')], context=context)
            result[project.id] = supplier_invoice_result
        return result

    def _compute_payment_vouchers(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            src = []
            payment_voucher_obj = self.pool.get('account.voucher.line')
            payment_voucher_result = payment_voucher_obj.search(cr, uid, [('project_id', '=', project.id), (
                'voucher_id.state', 'in', ['approved', 'validated', 'authorized', 'authorized_director', 'posted']), (
                                                                              'voucher_id.type', 'in',
                                                                              ['payment', 'cash_advance',
                                                                               'reimbursement'])], context=context)
            result[project.id] = payment_voucher_result
        return result

    def _compute_receipt_vouchers(self, cr, uid, ids, name, args, context=None):
        result = {}
        for project in self.browse(cr, uid, ids, context=context):
            src = []
            receipt_voucher_obj = self.pool.get('account.voucher.line')
            receipt_voucher_result = receipt_voucher_obj.search(cr, uid, [('project_id', '=', project.id), (
                'voucher_id.state', 'in', ['approved', 'validated', 'authorized', 'authorized_director', 'posted']),
                                                                          ('voucher_id.type', '=', 'receipt')],
                                                                context=context)
            result[project.id] = receipt_voucher_result
        return result

    _columns = {
        'project_manager_id': fields.many2one('res.users', 'Project Manager', required=True, ondelete='cascade'),
        'site_id': fields.many2one('project.site', 'Site', required=True, ondelete='cascade'),
        'addwork_category_id': fields.many2one('project.addwork.category', string='Addwork Category'),
        'misc_category_id': fields.many2one('project.misc.category', string='Miscellanous Category'),
        'misc_work_id': fields.many2one('project.misc.work', string='Miscellanous Work'),
        'operator_id': fields.many2one('project.operator', string='Operator', required=True),
        'site_type_id': fields.many2one('project.site.type', string='Site Type', required=True),
        'tanggal_target_rfi': fields.date('Target RFI'),
        'tanggal_surat_tugas': fields.date('Tanggal Surat Tugas'),
        'epm_export': fields.boolean('EPM export Status', ),
        'site_alias1': fields.related('site_id', 'site_alias1', string='Alias 1', type='char', size=64, store=False),
        'site_alias2': fields.related('site_id', 'site_alias2', string='Alias 2', type='char', size=64, store=False),
        # 'payment_ids': fields.function(_compute_lines, relation='account.move.line', type="many2many", string='Payments'),
        'sale_ids': fields.function(_compute_sale_lines, relation='sale.order.line', type="many2many", string='Sales'),
        'purchase_ids': fields.function(_compute_purchase_lines, relation='purchase.order.line', type="many2many",
                                        string='Purchase'),
        'stock_ids': fields.function(_compute_stock_moves, relation='stock.move', type="many2many", string='Warehouse'),
        'customer_invoice_ids': fields.function(_compute_customer_invoices, relation='account.invoice.line',
                                                type="many2many", string='Customer Invoice'),
        'supplier_invoice_ids': fields.function(_compute_supplier_invoices, relation='account.invoice.line',
                                                type="many2many", string='Supplier Invoice'),
        'payment_ids': fields.function(_compute_payment_vouchers, relation='account.voucher.line', type="many2many",
                                       string='Payment'),
        'receipt_ids': fields.function(_compute_receipt_vouchers, relation='account.voucher.line', type="many2many",
                                       string='Receipt'),
        'remark': fields.text('Remark')
    }

    def cekPref(self, val):
        options = {
            1: "TN",
            2: "SA",
        }
        return options[val]

    def cekSuff(self, val):
        options = {
            1: "01",
            2: "02",
            3: "03",
        }
        return options[val]

    def _get_Prasetia_ProjectID(self, cr, uid, context, *args):
        return "<Auto Generate ID>"
        # return "Get From EPM"

    def getOperatorID(self, cr, val):
        sql_req = "select epm_id from project_operator where id = %s"
        cr.execute(sql_req % val)
        return cr.fetchone()[0]

    def getSiteType(self, cr, val):
        sql_req = "select kode from project_site_type where id = %s"
        cr.execute(sql_req % val)
        return cr.fetchone()[0]

    def create(self, cr, uid, vals, context=None):

        #
        # Fungsi penomoran project di aktifkan di sini
        #

        # sql_req = """SELECT
        # NAME
        # FROM
        # account_analytic_account where name like '%s'
        # ORDER BY id desc
        # limit 1""";
        if not context:
            context = {}
        sql_req = """SELECT
                            id,number_next
                        FROM
                            ir_sequence
                        WHERE
                          "prefix" = '%s' AND suffix = '%s'
                        ORDER BY id DESC"""
        # val = self.cekPref(1)+"01%"
        # cr.execute(sql_req % val)

        pref = self.getSiteType(cr, vals['site_type_id'])
        suff = self.getOperatorID(cr, vals['operator_id'])
        cr.execute(sql_req % (pref, str("%02d" % suff)))

        # vals['name'] = "Fake Number"
        # try:
        # vals['name'] = cr.fetchone()[0] + "X"
        # except Exception, e:
        #     vals['name'] = "TN010000"

        try:
            hasil = cr.fetchone()
            vals['name'] = pref + str("%02d" % suff) + str("%04d" % hasil[1])

            sql_req = """UPDATE ir_sequence
                                SET
                                    number_next = %s
                                WHERE
                                    "id" = %s"""
            cr.execute(sql_req % (str(hasil[1] + 1), str(hasil[0])))
        except Exception, e:
            vals['name'] = pref + str("%02d" % suff) + str("%04d" % 1)
            sql_req = """INSERT INTO ir_sequence(
                                create_uid,
                                create_date,
                                write_date,
                                write_uid,
                                code,
                                suffix,
                                number_next,
                                number_increment,
                                "implementation",
                                company_id,
                                padding,
                                "prefix",
                                "name",
                                active) VALUES
                                (1,current_date,current_date,1,null,'%s',2,1,'standard',1,3,'%s','Prasetia ID0001',NULL)
                            """
            cr.execute(sql_req % (str("%02d" % suff), pref))

        return super(project, self).create(cr, uid, vals, context)

    _defaults = {
        'active': True,
        'name': _get_Prasetia_ProjectID,
        'epm_export': False,
    }

    def getLastID(self, cr, uid, ids, name, args, context=None):
        sql_req = """SELECT
                                NAME
                            FROM
                                account_analytic_account where name like 'Tmp%'
                            ORDER BY id desc
                            limit 1"""
        cr.execute(sql_req)
        pass


project()


class operator(osv.osv):
    _name = 'project.operator'
    _description = 'Operator Information'
    _columns = {
        'name': fields.char('Operator Name', 128, required=True),
        'epm_id': fields.integer('Reference to EPM ID', required=True),
        'code' : fields.char('Operator Code',127, required=False)
    }


operator()


class site_type(osv.osv):
    _name = 'project.site.type'
    _description = 'Site Type Information'
    _columns = {
        'name': fields.char('Site Type Name', 128, required=True),
        'kode': fields.char('Kode', 128, required=True),
    }


site_type()


class tower_type(osv.osv):
    _name = 'project.tower.type'
    _description = 'Tower Type Information'
    _columns = {
        'name': fields.char('Tower Type Name', 128, required=True),
    }


tower_type()


class tinggi_tower(osv.osv):
    _name = 'project.tinggi.tower'
    _description = 'Tinggi Tower Information'
    _columns = {
        'name': fields.char('Tinggi Tower', 128, required=True),
    }


tinggi_tower()


class island(osv.osv):
    _name = 'project.island'
    _description = 'Island Information'
    _columns = {
        'name': fields.char('Pulau', 128, required=True),
    }


island()


class province(osv.osv):
    _name = 'project.province'
    _description = 'Province Information'
    _columns = {
        'name': fields.char('Propinsi', 128, required=True),
        'island_id': fields.many2one('project.island', string='Pulau', required=False),
    }


province()


class city(osv.osv):
    _name = 'project.city'
    _description = 'City Information'
    _columns = {
        'name': fields.char('Kabupaten / Kota', 128, required=True),
        'province_id': fields.many2one('project.province', string='Propinsi', required=False),
        'island_id': fields.many2one('project.island', string='Pulau', required=False),
    }


city()


class area(osv.osv):
    _name = 'project.area'
    _description = 'Area Information'
    _columns = {
        'name': fields.char('Area', 128, required=True),
    }


area()


class field_type(osv.osv):
    _name = 'project.field.type'
    _description = 'Field Type Information'
    _columns = {
        'name': fields.char('Field Type', 128, required=True),
    }


field_type()


class misc_category(osv.osv):
    _name = 'project.misc.category'
    _description = 'Miscellanous Category Information'
    _columns = {
        'name': fields.char('Misc Category', 128, required=True),
    }


misc_category()


class misc_work(osv.osv):
    _name = 'project.misc.work'
    _description = 'Miscellanous Work Information'
    _columns = {
        'name': fields.char('Misc Work', 128, required=True),
        'misc_category_id': fields.many2one('project.misc.category', string='Misc Category', required=False),
    }


misc_work()


class addwork_category(osv.osv):
    _name = 'project.addwork.category'
    _description = 'Addwork Category Information'
    _columns = {
        'name': fields.char('Addwork Category', 128, required=True),
    }


addwork_category()

# class account_analytic_account(osv.osv):
# _inherit = 'account.analytic.account'
# _description = 'Analytic Account'

# # def generate_account_analytic_account(self,cr,uid,vals,account_analytic_account,context=None):
# #     # print vals
# #     vals['parent_id'] = account_analytic_account
# #     # print "PHASE 1 : Passed"

# #     super(account_analytic_account,self).create(cr,uid,vals)
#     #     return analytic_account_id

#     # def create(self, cr, uid, vals, context=None):
#     #     if context is None:
#     #         context = {}

#     #     print 'CEK CEK CEK TTTTTTTTTTTTTTTTTTTT'
#     #     print vals

#     #     # print vals.get('child_ids')
#     #     if vals.get('child_ids', False) and context.get('analytic_project_copy', False):
#     #         vals['child_ids'] = []
#     #     analytic_account_id = super(account_analytic_account, self).create(cr, uid, vals, context=context)
#     #     # print vals
#     #     self.project_create(cr, uid, analytic_account_id, vals, context=context)
#     #     # self.generate_account_analytic_account(cr,uid,vals,analytic_account_id,context=context)
#     #     self.generate_account_analytic_account(cr,uid,vals,context=context)
#     #     return analytic_account_id

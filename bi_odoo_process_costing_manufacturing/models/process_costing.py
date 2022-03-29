# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
import math

class MrpBom(models.Model):
    _inherit = "mrp.bom"
    
    def _compute_total_material_cost(self):
        total = 0.0
        for line in self.bom_material_cost_ids:
            total += line.total_cost
        self.bom_total_material_cost = total
            
    def _compute_total_labour_cost(self):
        total = 0.0
        for line in self.bom_labour_cost_ids:
            total += line.total_cost
        self.bom_total_labour_cost = total

    def _compute_total_overhead_cost(self):
        total = 0.0
        for line in self.bom_overhead_cost_ids:
            total += line.total_cost
        self.bom_total_overhead_cost = total        
        
    @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    bom_material_cost_ids = fields.One2many("mrp.bom.material.cost","mrp_bom_material_id","Material Cost")
    bom_labour_cost_ids = fields.One2many("mrp.bom.labour.cost","mrp_bom_labour_id","Labour Cost")
    bom_overhead_cost_ids = fields.One2many("mrp.bom.overhead.cost","mrp_bom_overhead_id","Overhead Cost")
    # single page total cost
    bom_total_material_cost = fields.Float(compute='_compute_total_material_cost',string="Total Material Cost",default=0.0)
    bom_total_labour_cost = fields.Float(compute='_compute_total_labour_cost',string="Total Labour Cost",default=0.0)
    bom_total_overhead_cost = fields.Float(compute='_compute_total_overhead_cost',string="Total Overhead Cost",default=0.0)
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

class MrpBomMaterialCost(models.Model):
    _name = "mrp.bom.material.cost"
    
    operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
    product_id = fields.Many2one('product.template',string="Product")
    planned_qty = fields.Float(string="Planned Qty",default=0.0)
    actual_qty = fields.Float(string="Actual Qty",default=0.0)
    uom_id = fields.Many2one('product.uom',string="UOM")
    cost = fields.Float(string="Cost/Unit")
    total_cost = fields.Float(compute='onchange_planned_qty',string="Total Cost")
    total_actual_cost = fields.Float(compute='onchange_planned_qty',string="Total Actual Cost")
    mrp_bom_material_id = fields.Many2one("mrp.bom","Mrp Bom Material")
    mrp_pro_material_id = fields.Many2one("mrp.production","Mrp Production Material")
    mrp_wo_material_id = fields.Many2one("mrp.workorder","Mrp Workorder Material")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    
    @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
                
    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        
    #@api.multi
    @api.onchange('planned_qty', 'cost')
    def onchange_planned_qty(self):
        for line in self:
            price = line.planned_qty * line.cost
            actual_price = line.actual_qty * line.cost
            line.total_cost = price
            line.total_actual_cost = actual_price

class MrpBomLabourCost(models.Model):
    _name = "mrp.bom.labour.cost"
    
    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
            
    #@api.multi
    @api.onchange('planned_qty', 'cost')    
    def onchange_labour_planned_qty(self):
        for line in self:
            price = line.planned_qty * line.cost
            actual_price = line.actual_qty * line.cost
            line.total_cost = price
            line.total_actual_cost = actual_price
            
    @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
    product_id = fields.Many2one('product.template',string="Product")
    planned_qty = fields.Float(string="Planned Qty",default=0.0)
    actual_qty = fields.Float(string="Actual Qty",default=0.0)
    uom_id = fields.Many2one('product.uom',string="UOM")
    cost = fields.Float(string="Cost/Unit")
    total_cost = fields.Float(compute='onchange_labour_planned_qty',string="Total Cost")
    total_actual_cost = fields.Float(compute='onchange_labour_planned_qty',string="Total Actual Cost")
    #total_labour_cost = fields.Float(string="Total Labour Cost")
    mrp_bom_labour_id = fields.Many2one("mrp.bom","Mrp Bom Labour")
    mrp_pro_labour_id = fields.Many2one("mrp.production","Mrp Production Labour")
    mrp_wo_labour_id = fields.Many2one("mrp.workorder","Mrp Workorder Labour")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    
class MrpBomOverheadCost(models.Model):
    _name = "mrp.bom.overhead.cost"
    
    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        
    #@api.multi
    @api.onchange('planned_qty', 'cost')
    def onchange_overhead_planned_qty(self):
        for line in self:
            price = line.planned_qty * line.cost
            actual_price = line.actual_qty * line.cost
            line.total_cost = price
            line.total_actual_cost = actual_price
            
    @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
    product_id = fields.Many2one('product.template',string="Product")
    planned_qty = fields.Float(string="Planned Qty",default=0.0)
    actual_qty = fields.Float(string="Actual Qty",default=0.0)
    uom_id = fields.Many2one('product.uom',string="UOM")
    cost = fields.Float(string="Cost/Unit")
    total_cost = fields.Float(compute='onchange_overhead_planned_qty',string="Total Cost")
    total_actual_cost = fields.Float(compute='onchange_overhead_planned_qty',string="Total Actual Cost")
    #total_overhead_cost = fields.Float(string="Total Overhead Cost")
    mrp_bom_overhead_id = fields.Many2one("mrp.bom","Mrp Bom Overhead")
    mrp_pro_overhead_id = fields.Many2one("mrp.production","Mrp Production Overhead")
    mrp_wo_overhead_id = fields.Many2one("mrp.workorder","Mrp Workorder Overhead")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    @api.multi
    def _generate_workorders(self, exploded_boms):
        workorders = self.env['mrp.workorder']
        list_of_material = []
        list_of_labour = []
        list_of_overhead = []
        
        for material in self.pro_material_cost_ids:
            list_of_material.append(material.id)
        
        for labour in self.pro_labour_cost_ids:
            list_of_labour.append(labour.id)
        
        for overhead in self.pro_overhead_cost_ids:
            list_of_overhead.append(overhead.id)
        
        for bom, bom_data in exploded_boms:
            # If the routing of the parent BoM and phantom BoM are the same, don't recreate work orders, but use one master routing
            if bom.routing_id.id and (not bom_data['parent_line'] or bom_data['parent_line'].bom_id.routing_id.id != bom.routing_id.id):
                workorders += self._workorders_create(bom, bom_data)
                workorders.write({'wo_material_cost_ids': [(6,0,list_of_material)],
                                  'wo_labour_cost_ids': [(6,0,list_of_labour)],
                                  'wo_overhead_cost_ids': [(6,0,list_of_overhead)],})
        return workorders
        
    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def onchange_product_id(self):
        """ Finds UoM of changed product. """
        list_of_material = []
        list_of_labour = []
        list_of_overhead = []
        
        if not self.product_id:
            self.bom_id = False
        else:
            bom = self.env['mrp.bom']._bom_find(product=self.product_id, picking_type=self.picking_type_id, company_id=self.company_id.id)
            if bom.type == 'normal':
                self.bom_id = bom.id
                
                for material in bom.bom_material_cost_ids:
                    list_of_material.append(material.id)
                self.pro_material_cost_ids = [(6,0,list_of_material)]
                
                for labour in bom.bom_labour_cost_ids:
                    list_of_labour.append(labour.id)
                self.pro_labour_cost_ids = [(6,0,list_of_labour)]
                
                for overhead in bom.bom_overhead_cost_ids:
                    list_of_overhead.append(overhead.id)
                self.pro_overhead_cost_ids = [(6,0,list_of_overhead)]
                
            else:
                self.bom_id = False
                
                for material in bom.bom_material_cost_ids:
                    list_of_material.append(material.id)
                self.pro_material_cost_ids = [(6,0,list_of_material)]
                
                for labour in bom.bom_labour_cost_ids:
                    list_of_labour.append(labour.id)
                self.pro_labour_cost_ids = [(6,0,list_of_labour)]
                
                for overhead in bom.bom_overhead_cost_ids:
                    list_of_overhead.append(overhead.id)
                self.pro_overhead_cost_ids = [(6,0,list_of_overhead)]
                
            self.product_uom_id = self.product_id.uom_id.id
            return {'domain': {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}}


    def _compute_total_material_cost(self):
        total = 0.0
        actual_total = 0.0
        for line in self.pro_material_cost_ids:
            total += line.total_cost
            actual_total += line.total_actual_cost
        self.total_material_cost = total
        self.total_actual_material_cost = actual_total
            
    def _compute_total_labour_cost(self):
        total = 0.0
        actual_total = 0.0
        for line in self.pro_labour_cost_ids:
            total += line.total_cost
            actual_total += line.total_actual_cost
        self.total_labour_cost = total
        self.total_actual_labour_cost = actual_total

    def _compute_total_overhead_cost(self):
        total = 0.0
        actual_total = 0.0
        for line in self.pro_overhead_cost_ids:
            total += line.total_cost
            actual_total += line.total_actual_cost
        self.total_overhead_cost = total 
        self.total_actual_overhead_cost = actual_total
            
    def _compute_total_all_cost(self):
        total = 0.0
        actual_total = 0.0
        total = self.total_material_cost + self.total_labour_cost + self.total_overhead_cost
        actual_total = self.total_actual_material_cost + self.total_actual_labour_cost + self.total_actual_overhead_cost
        self.total_all_cost = total 
        self.total_actual_all_cost = actual_total
        
    @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    def _compute_total_product_cost(self):
        total = 0.0
        for line in self.finished_move_line_ids:
            if line.qty_done != 0.0:
                total =  self.total_actual_all_cost / line.qty_done
        self.product_unit_cost = total
        
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    
    pro_material_cost_ids = fields.One2many("mrp.bom.material.cost","mrp_pro_material_id","Material Cost")
    pro_labour_cost_ids = fields.One2many("mrp.bom.labour.cost","mrp_pro_labour_id","Labour Cost")
    pro_overhead_cost_ids = fields.One2many("mrp.bom.overhead.cost","mrp_pro_overhead_id","Overhead Cost")
    pro_total_material_cost = fields.Float(string="Total Material Cost",default=0.0)
    
    # Costing Tab
    total_material_cost = fields.Float(compute='_compute_total_material_cost',string="Total Material Cost",default=0.0)
    total_labour_cost = fields.Float(compute='_compute_total_labour_cost',string="Total Labour Cost",default=0.0)
    total_overhead_cost = fields.Float(compute='_compute_total_overhead_cost',string="Total Overhead Cost",default=0.0)
    total_all_cost = fields.Float(compute='_compute_total_all_cost',string="Total Cost",default=0.0)
    
    # Costing Tab
    total_actual_material_cost = fields.Float(compute='_compute_total_material_cost',string="Total Actual Material Cost",default=0.0)
    total_actual_labour_cost = fields.Float(compute='_compute_total_labour_cost',string="Total Actual Labour Cost",default=0.0)
    total_actual_overhead_cost = fields.Float(compute='_compute_total_overhead_cost',string="Total Actual Overhead Cost",default=0.0)
    total_actual_all_cost = fields.Float(compute='_compute_total_all_cost',string="Total Actual Cost",default=0.0)
    
    product_unit_cost = fields.Float(compute='_compute_total_product_cost',string="Product Unit Cost",default=0.0)

class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"
    
    def _compute_total_material_cost(self):
        total = 0.0
        actual_total = 0.0
        for order in self:
            for line in order.wo_material_cost_ids:
                total += line.total_cost
                actual_total += line.total_actual_cost
            order.total_material_cost = total
            order.total_actual_material_cost = actual_total
            
    def _compute_total_labour_cost(self):
        total = 0.0
        actual_total = 0.0
        for order in self:
            for line in order.wo_labour_cost_ids:
                total += line.total_cost
                actual_total += line.total_actual_cost
            order.total_labour_cost = total
            order.total_actual_labour_cost = actual_total

    def _compute_total_overhead_cost(self):
        total = 0.0
        actual_total = 0.0
        for order in self:
            for line in order.wo_overhead_cost_ids:
                total += line.total_cost
                actual_total += line.total_actual_cost
            order.total_overhead_cost = total
            order.total_actual_overhead_cost = actual_total

    def _compute_total_all_cost(self):
        total = 0.0
        actual_total = 0.0
        total = self.total_material_cost + self.total_labour_cost + self.total_overhead_cost
        actual_total = self.total_actual_material_cost + self.total_actual_labour_cost + self.total_actual_overhead_cost
        self.total_all_cost = total
        self.total_actual_all_cost = actual_total
                
    @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    
    wo_material_cost_ids = fields.One2many("mrp.bom.material.cost","mrp_wo_material_id","Material Cost")
    wo_labour_cost_ids = fields.One2many("mrp.bom.labour.cost","mrp_wo_labour_id","Labour Cost")
    wo_overhead_cost_ids = fields.One2many("mrp.bom.overhead.cost","mrp_wo_overhead_id","Overhead Cost")
    #wo_total_material_cost = fields.Float(string="Total Material Cost",default=0.0)
    
    # Costing Tab
    total_material_cost = fields.Float(compute='_compute_total_material_cost',string="Total Material Cost",default=0.0)
    total_labour_cost = fields.Float(compute='_compute_total_labour_cost',string="Total Labour Cost",default=0.0)
    total_overhead_cost = fields.Float(compute='_compute_total_overhead_cost',string="Total Overhead Cost",default=0.0)
    total_all_cost = fields.Float(compute='_compute_total_all_cost',string="Total Cost",default=0.0)
    
    # Costing Tab
    total_actual_material_cost = fields.Float(compute='_compute_total_material_cost',string="Total Actual Material Cost",default=0.0)
    total_actual_labour_cost = fields.Float(compute='_compute_total_labour_cost',string="Total Actual Labour Cost",default=0.0)
    total_actual_overhead_cost = fields.Float(compute='_compute_total_overhead_cost',string="Total Actual Overhead Cost",default=0.0)
    total_actual_all_cost = fields.Float(compute='_compute_total_all_cost',string="Total Actual Cost",default=0.0)
    
    product_unit_cost = fields.Float(string="Product Unit Cost",default=0.0)
    
class ChangeProductionQty(models.TransientModel):
    _inherit = 'change.production.qty'
    
    @api.multi
    def change_prod_qty(self):
        for wizard in self:
            production = wizard.mo_id
            list_of_material = []
            produced = sum(production.move_finished_ids.mapped('quantity_done'))
            if wizard.product_qty < produced:
                raise UserError(_("You have already processed %d. Please input a quantity higher than %d ")%(produced, produced))
            production.write({'product_qty': wizard.product_qty})
            
            # Change Material,Labour and Overhead quantity
            for material in production.pro_material_cost_ids:
                    material.write({'planned_qty':wizard.product_qty,'actual_qty':wizard.product_qty})
        
            for labour in production.pro_labour_cost_ids:
                    labour.write({'planned_qty':wizard.product_qty,'actual_qty':wizard.product_qty}) 

            for overhead in production.pro_overhead_cost_ids:
                    overhead.write({'planned_qty':wizard.product_qty,'actual_qty':wizard.product_qty})                                                   

            done_moves = production.move_finished_ids.filtered(lambda x: x.state == 'done' and x.product_id == production.product_id)
            qty_produced = production.product_id.uom_id._compute_quantity(sum(done_moves.mapped('product_qty')), production.product_uom_id)
            factor = production.product_uom_id._compute_quantity(production.product_qty - qty_produced, production.bom_id.product_uom_id) / production.bom_id.product_qty
            boms, lines = production.bom_id.explode(production.product_id, factor, picking_type=production.bom_id.picking_type_id)
            for line, line_data in lines:
                production._update_raw_move(line, line_data)
            operation_bom_qty = {}
            for bom, bom_data in boms:
                for operation in bom.routing_id.operation_ids:
                    operation_bom_qty[operation.id] = bom_data['qty']
            self._update_product_to_produce(production, production.product_qty - qty_produced)
            moves = production.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            moves._action_assign()
            for wo in production.workorder_ids:
                operation = wo.operation_id
                if operation_bom_qty.get(operation.id):
                    cycle_number = math.ceil(operation_bom_qty[operation.id] / operation.workcenter_id.capacity)  # TODO: float_round UP
                    wo.duration_expected = (operation.workcenter_id.time_start +
                                 operation.workcenter_id.time_stop +
                                 cycle_number * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency)
                if production.product_id.tracking == 'serial':
                    quantity = 1.0
                else:
                    quantity = wo.qty_production - wo.qty_produced
                    quantity = quantity if (quantity > 0) else 0
                wo.qty_producing = quantity
                if wo.qty_produced < wo.qty_production and wo.state == 'done':
                    wo.state = 'progress'
                # assign moves; last operation receive all unassigned moves
                # TODO: following could be put in a function as it is similar as code in _workorders_create
                # TODO: only needed when creating new moves
                moves_raw = production.move_raw_ids.filtered(lambda move: move.operation_id == operation and move.state not in ('done', 'cancel'))
                if wo == production.workorder_ids[-1]:
                    moves_raw |= production.move_raw_ids.filtered(lambda move: not move.operation_id)
                moves_finished = production.move_finished_ids.filtered(lambda move: move.operation_id == operation) #TODO: code does nothing, unless maybe by_products?
                moves_raw.mapped('move_line_ids').write({'workorder_id': wo.id})
                (moves_finished + moves_raw).write({'workorder_id': wo.id})
                if wo.move_raw_ids.filtered(lambda x: x.product_id.tracking != 'none') and not wo.active_move_line_ids:
                    wo._generate_lot_ids()
        return {}

'''class MrpProductionReport(models.Model):
    _name = "mrp.production.report"
    _auto = False
    
    bom_cost_id = fields.Many2one('mrp.bom','Bom Cost')
    mrp_production_id = fields.Many2one('mrp.production','Production')
    planned_qty = fields.Float(string="Planned Qty",default=0.0)
    cost = fields.Float(string="Cost/Unit")
    main_total = fields.Float(string="Total")
    #total_material_cost = fields.Float(string="Total Material Cost")
    #total_labour_cost = fields.Float(string="Total Labour Cost")
    #total_overhead_cost = fields.Float(string="Total Overhead Cost")
    #total_all_cost = fields.Float(string="Total Cost")
    
    # Costing Tab
    #total_actual_material_cost = fields.Float(string="Total Actual Material Cost")
    #total_actual_labour_cost = fields.Float(string="Total Actual Labour Cost")
    #total_actual_overhead_cost = fields.Float(string="Total Actual Overhead Cost")
    #total_actual_all_cost = fields.Float(string="Total Actual Cost")
    
    _order = 'bom_cost_id'
    
    def _select(self):
        select_str = """
                    select 
                           mrp_production.id as id,
                           mrp_production.id as mrp_production_id,
                           
                           
                    """
        return select_str
                
    def _from(self):
        return """
            FROM mrp_production AS mrp_production
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
            )
        """ % (self._table, self._select(), self._from())
        )  '''         
               
    
            

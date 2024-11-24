from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):
    _name = 'project.task'
    _description = 'Project Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Task Name', required=True)
    project_id = fields.Many2one('project.management', string='Project')
    project_assigned_team=fields.Many2many('hr.employee',related="project_id.assigned_team", string='Assigned Team' ,required=True)
    description = fields.Text(string='Description')
    assigned_to = fields.Many2one(
        'hr.employee',
        string="Assigned To",
        domain="[('id', 'in', project_assigned_team)]",
        required=True
    )
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    priority = fields.Selection(
        [ ('not_defined','Not_defined'),('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        string='Priority'
    )
    status = fields.Selection(
        [('to_do', 'To Do'),
         ('in_progress', 'In Progress'),
         ('done', 'Done')],
        string='Status',
        default='to_do',
        tracking=1
    )
    progress = fields.Float(string='Progress', compute='_compute_progress')
    deadline = fields.Date(string='Deadline', track_visibility='onchange')
    @api.depends('status')
    def _compute_progress(self):
        for task in self:
            if task.status == 'done':
                task.progress = 100.0
            elif task.status == 'in_progress':
                task.progress = 50.0
            else:
                task.progress = 0.0

    @api.depends('status')
    def _compute_priority(self):
        for task in self:
            if task.status == 'high':
                task.priority = 3.0
            elif task.status == 'medium':
                task.priority = 2.0
            else:
                task.priority = 1.0

    @api.model
    def _notify_upcoming_deadlines(self):
        tasks = self.search([('deadline', '>=', fields.Date.today())])
        for task in tasks:
            task.message_post(
                body=f"Reminder: The deadline for task '{task.name}' is approaching!",
                subtype_xmlid='mail.mt_comment',
            )
    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date:
            return {
                'domain': {
                    'end_date': [('>', self.start_date)],
                }
            }

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date and record.end_date <= record.start_date:
                raise ValidationError("End Date must be greater than Start Date.")
from odoo import models, fields,api

class ProjectManagement(models.Model):
    _name = 'project.management'
    _description = 'Project Management'

    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection(
        [('planning', 'Planning'),
         ('in_progress', 'In Progress'),
         ('completed', 'Completed'),
         ('on_hold', 'On Hold')],
        string='Status',
        default='planning'
    )
    assigned_team = fields.Many2many('hr.employee', string='Assigned Team')
    progress = fields.Float(string="Progress (%)", compute="_compute_progress", store=True)
    task_ids = fields.One2many('project.task', 'project_id', string='Tasks')
    total_tasks = fields.Integer(string="Total Tasks", compute="_compute_task_counts", store=True)
    completed_tasks = fields.Integer(string="Completed Tasks", compute="_compute_task_counts", store=True)
    deadline_missed = fields.Boolean(string='Deadline Missed', compute='_compute_deadline_missed')

    @api.depends('task_ids.status')
    def _compute_task_stats(self):
        for project in self:
            project.total_tasks = len(project.task_ids)
            project.completed_tasks = len(project.task_ids.filtered(lambda t: t.status == 'done'))



    @api.depends('end_date', 'task_ids.status')
    def _compute_deadline_missed(self):
        for project in self:
            if project.end_date and fields.Date.today() > project.end_date and project.completed_tasks < project.total_tasks:
                project.deadline_missed = True
            else:
                project.deadline_missed = False

    @api.depends('completed_tasks', 'total_tasks')
    def _compute_progress(self):
        for project in self:
            if project.total_tasks:
                project.progress = (project.completed_tasks / project.total_tasks) * 100.0
            else:
                project.progress = 0.0



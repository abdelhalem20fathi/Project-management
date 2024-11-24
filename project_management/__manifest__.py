{
    'name': 'Project Management',
    'version': '17.0.0.1',
    'summary': 'Manage projects, tasks, and team collaboration.',
    'author': 'Abdelhalem',
    'depends': ['base', 'hr'],
    'data': [
        'security/project_management_access.xml',
        'security/ir.model.access.csv',
        'views/project_management_views.xml',
        'views/project_task_views.xml',
        'views/menu_views.xml',
        'views/project_dashboard_views.xml',
        'views/project_performance_views.xml',
        # 'views/project_gantt_view.xml',
        'reports/project_performance_report.xml',
        'data/cron.xml',
    ],
    'assets': {
            'web.assets_backend': [
                '/project_management/static/src/css/styles.css',
            ],
        },
    'installable': True,
    'application': True,
}

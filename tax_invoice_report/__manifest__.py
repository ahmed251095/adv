{
    'name': "Invoice Report",
    'summary': """
        Invoice Report""",
    'description': """
        Invoice Report
    """,
    'license': 'LGPL-3',
    'author': "Ahmed Hussein",
    'category': 'Uncategorized',
    'version': '16.1',
    'depends': ['base','account','l10n_sa'],
    'data': [
        'views/invoice_report.xml',
        'report/invoice_header_footer.xml',
        'report/report.xml'
    ],
}

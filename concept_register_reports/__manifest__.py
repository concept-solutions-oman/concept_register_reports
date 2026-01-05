# cg_sales_register/__manifest__.py
{
    "name": "CG Sales Register",
    "summary": "Sales Register by product line (Date, Invoice, Customer, Product, Qty)",
    "version": "17.0.1.0.0",
    "author": "Concept Solutions",
    "website": "",
    "license": "OPL-1",
    "category": "Accounting/Reporting",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/sales_register_report_views.xml",
        "views/purchase_register_report.xml",
    ],
    "installable": True,
    "application": False,
    "price": 50.00,
    "currency": "USD",
}

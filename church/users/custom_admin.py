from django.contrib.admin import AdminSite


class MyCustomAdminSite(AdminSite):
    site_title = "ACK GOOD SAMARITAN"  # The name to be displayed as the title of the admin panel
    site_header = "ACK GOOD SAMARITAN"  # The text to be displayed as the header of the admin panel
    index_title = "Welcome to the Admin Panel"  # The text to be displayed on the main admin page

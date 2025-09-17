from django.apps import AppConfig

# This class is used to configure the website app
class WebsiteConfig(AppConfig): 
    # The default_auto_field attribute is used to specify the type of primary key that will be used for the models in the app
    default_auto_field = 'django.db.models.BigAutoField'
    # The name of the app
    name = 'website'

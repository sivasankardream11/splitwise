import os


# Import settings based on the value of the DEBUG environment variable
if os.environ.get('DEBUG') == 'development':
    from core.settings.development import *  # Import development settings
elif os.environ.get('DEBUG') == 'production':
    from core.settings.production import *  # Import production settings

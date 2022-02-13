from django.apps import AppConfig


class UploadConfig(AppConfig):
    name = 'upload'

    # running function that deletes the expire uploaded file
    def ready(self):
        from background_task import updater
        updater.start()
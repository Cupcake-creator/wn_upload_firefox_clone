from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from upload.models import Upload 
from django.utils import timezone
import os

# check if expire data exist
def schedule_adds_on():
    cmd_start = 'Start delete expired data...'
    cmd_end = 'End'

    print(f'[{timezone.now()}]') 
    print(cmd_start)    
    expried_data = Upload.objects.filter(expire_date__lt=timezone.now())
    data_expire_count = len(expried_data)
    if data_expire_count == 0 :
        print(f'-- No expire data available')
    else:
        for data in expried_data:
            path = data.file.name
            filename = path.split('/')[-1]
            print(f'-- {filename}')
            os.remove(path)
        print(f'-- deleted file count : {data_expire_count}')
        expried_data.delete() 
    print(cmd_end)
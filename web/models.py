import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.db import models


class Collection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=200)

    def get_new_file_path(self, prefix):
        """Provide new file path for fetched dataset."""
        suffix = datetime.now().strftime('%Y%m%d%H%M%s')
        path = f"{settings.MEDIA_ROOT}/{prefix}-{suffix}.csv"
        return path

    def write_file(self, data, path):
        """Write data set under provided path."""
        write_header = not os.path.exists(path)
        with open(path, "a", newline='') as f:
            csvwriter = csv.DictWriter(
                f, fieldnames=data[0].keys()
            )
            if write_header:
                csvwriter.writeheader()
            csvwriter.writerows(data)
            self.filename = path
        return path

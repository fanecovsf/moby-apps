from django.utils.text import slugify
import os

class Utils:

    @staticmethod
    def attachment_file_path(instance, filename):
        base_filename, file_extension = os.path.splitext(filename)
        slug = slugify(base_filename)
        return f"attachments/{slug}{file_extension}"
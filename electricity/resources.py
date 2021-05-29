from import_export import resources
from electricity.models import FeedBack

class FeedBackResource(resources.ModelResource):
    class Meta:
        model = FeedBack

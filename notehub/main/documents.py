from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Document as DocumentModel, Tag

# Define the Elasticsearch index
documents_index = Index('documents')
documents_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@documents_index.doc_type
class DocumentDocument(Document):
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    tags = fields.TextField(
        attr='get_tags',
        fields={
            'raw': fields.KeywordField(),
        }
    )

    class Django:
        model = DocumentModel  # The model associated with this Document
        fields = [
            'id',
            'file_url',
            'file_size',
            'file_type',
        ]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Document as DocumentModel, Tag

# Define the Elasticsearch index
documents_index = Index('documents')
documents_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        'analyzer': {
            'edge_ngram_analyzer': {
                'type': 'custom',
                'tokenizer': 'edge_ngram_tokenizer'
            }
        },
        'tokenizer': {
            'edge_ngram_tokenizer': {
                'type': 'edge_ngram',
                'min_gram': 1,
                'max_gram': 20,
                'token_chars': ['letter', 'digit']
            }
        }
    }
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

    author = fields.ObjectField(
        attr='author',
        properties={
            'username': fields.TextField(
                analyzer='edge_ngram_analyzer'
            ),
            'email': fields.KeywordField(),
        }
    )

    class Django:
        model = DocumentModel
        fields = [
            'id',
            'file_url',
            'file_size',
            'file_type',
        ]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_author(self, obj):
        return {
            'username': obj.author.username,
            'email': obj.author.email,
        }
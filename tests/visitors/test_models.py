from django_codemod.visitors.models import ModelsPermalinkTransformer
from tests.visitors.base import BaseVisitorTest


class TestAvailableAttrsTransformer(BaseVisitorTest):

    transformer = ModelsPermalinkTransformer

    def test_simple_substitution_args(self) -> None:
        before = """
            from django.db import models

            class MyModel(models.Model):

                @models.permalink
                def url(self):
                    return ('guitarist_detail', [self.slug])
        """
        after = """
            from django.db import models
            from django.urls import reverse

            class MyModel(models.Model):

                def url(self):
                    return reverse('guitarist_detail', None, [self.slug])
        """
        self.assertCodemod(before, after)

    def test_simple_substitution_kwargs(self) -> None:
        before = """
            from django.db import models

            class MyModel(models.Model):

                @models.permalink
                def url(self):
                    return ('guitarist_detail', [], {'slug': self.slug})
        """
        after = """
            from django.db import models
            from django.urls import reverse

            class MyModel(models.Model):

                def url(self):
                    return reverse('guitarist_detail', None, [], {'slug': self.slug})
        """
        self.assertCodemod(before, after)

from django.db import models


class Repository(models.Model):
    LANGUAGE_RUST = 'RS'
    LANGUAGES = (
        (LANGUAGE_RUST, 'Rust'),
    )
    language = models.CharField(choices=LANGUAGES, max_length=2,
                                default=LANGUAGE_RUST)

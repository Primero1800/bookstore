from datetime import datetime, timedelta

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=70, verbose_name='Name')
    surname = models.CharField(max_length=70, verbose_name='Surname')
    slug = models.SlugField(null=False, unique=True)
    born = models.DateField(verbose_name='Date of birth', blank=True, null=True)
    died = models.DateField(verbose_name='Date of death', blank=True, null=True)

    def __str__(self):
        return f"Author ({self.pk}) {self.name} {self.surname}"

    def is_alive(self):
        return self.died is None or self.died > datetime.now().date()

    @property
    def ages(self):
        if self.born:
            end_date = self.died if self.died else datetime.now().date()
            return end_date.year - self.born.year - ((end_date.month, end_date.day) < (self.born.month, self.born.day))
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'slug': self.slug,
            'born': self.born,
            'died': self.died,
            'ages': self.ages,
            'is_alive': self.is_alive(),
            'books': self.books.all().values(),
        }

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = "Authors"
        ordering = ('-slug', )

class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name='Title')
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(max_length=1000, verbose_name='Description', blank=True, null=True)
    year = models.SmallIntegerField(verbose_name='Year published')
    authors = models.ManyToManyField(
        Author, verbose_name='Authors', related_name='books', blank=True
    )

    class StatusCode(models.IntegerChoices):
        R0 = 0, 'Not available'
        R1 = 1, 'Available'

    status = models.PositiveIntegerField(choices=StatusCode.choices, default=StatusCode.R1, verbose_name='Availability')

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'
        ordering = ('-pk', )

    def __str__(self):
        return f"Book ({self.pk}) {self.title}"

    def is_available(self):
        return self.status == self.StatusCode.R1

    def get_choice_description(self):
        return dict(Book.StatusCode.choices).get(self.status, 'unknown')

    def to_dict(self):
        return {
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'year': self.year,
            'authors': self.authors.all().values(),
            'status': self.status,
            'status_display': self.get_choice_description(),
            'is_available': self.is_available(),
        }


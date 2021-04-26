import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = "категории"
        ordering = ['id']

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = "жанры"
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    year = models.IntegerField(blank=True, verbose_name='год',
                               validators=[
                                   MinValueValidator(1000),
                                   MaxValueValidator(
                                       datetime.date.today().year)
                               ]
                               )
    description = models.TextField(blank=True, verbose_name='описание')
    genre = models.ManyToManyField(
        Genres, verbose_name='жанр'
    )
    category = models.ForeignKey(
        Categories, verbose_name='категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = "произведения"
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'рейтинг',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['title']
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique Review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['review']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from recipes.models import Recipe


class User(AbstractUser):
    email = models.CharField(
        max_length=254,
        validators=[EmailValidator],
        blank=False,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия'
    )
    # favorites = models.ForeignKey(
    #     Recipe,
    #     related_name='in_favorites',
    #     verbose_name='Избранное',
    # )


class UsersSubscribes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='user',
        verbose_name='Пользователь',
    )
    subscribes = models.ManyToManyField(
        User,
        related_name='subscribes',
        verbose_name='Подписки',
    )

    class Meta:
        unique_together = ('user', 'subscribes')


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='favorited',
        verbose_name='Пользователь',
    )
    favorite_recipes = models.ManyToManyField(
        Recipe,
        related_name='favorite_in',
        verbose_name='Избранное',
    )
    

#     class Meta:
#         verbose_name = _("favorite")
#         verbose_name_plural = _("favorites")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("favorite_detail", kwargs={"pk": self.pk})
# )
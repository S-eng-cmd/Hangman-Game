from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import random
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
import string


class Game(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hangman_games", verbose_name="Користувач"
    )
    word = models.CharField(
        "Загадане слово", max_length=50
    )
    max_tries = models.PositiveIntegerField(
        "Максимальна кількість спроб", default=20, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Гра Шибениця"
        verbose_name_plural = "Гри Шибениця"

    def __str__(self):
        return f"Hangman Game #{self.pk} for {self.user.username}"

    @property
    @admin.display(boolean=True, description='Завершено')
    def is_finished(self):
        return self.tries.count() >= self.max_tries or self.has_won

    @property
    @admin.display(boolean=True, description='Перемога')
    def has_won(self):
        guessed_letters = set(try_obj.letter for try_obj in self.tries.all() if try_obj.is_correct)
        return all(letter in guessed_letters for letter in self.word.lower())

    @property
    @admin.display(description='Кількість спроб')
    def tries_count(self):
        return self.tries.count()

    @property
    @admin.display(description='Залишилось спроб')
    def remaining_tries(self):
        return self.max_tries - self.tries.count()

    def get_display_word(self):
        guessed_letters = set(try_obj.letter for try_obj in self.tries.all() if try_obj.is_correct)
        return ' '.join(letter if letter.lower() in guessed_letters else '_' for letter in self.word)



class Try(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="tries", verbose_name="Гра"
    )
    letter = models.CharField(
        "Літера", max_length=1, validators=[MinLengthValidator(1)]
    )
    is_correct = models.BooleanField(verbose_name="Правильна")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Спроба"
        verbose_name_plural = "Спроби"

    def __str__(self):
        return f"Try {self.letter} for Game #{self.game.pk}"

    def check_if_correct(self):
        return self.letter.lower() in self.game.word.lower()

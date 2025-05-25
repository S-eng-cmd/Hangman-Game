import random
from Hangman.models import Game, Try

class GameService:
    @staticmethod
    def generate_word():
        words = ['Котик', 'Репозиторій', 'Ліцеїст', 'Квіточка', 'Ентропія', 'Термодинаміка', 'Сонечко', 'Гуляки', 'Оптиміст','Канікули', 'Нагеліана', 'Ексцентр', 'Паралелепіпед', 'Дезоксирибоза']
        return random.choice(words).lower()

    @staticmethod
    def evaluate_letter(word, letter):
        letter = letter.lower()
        return letter in word.lower()

    @staticmethod
    def create_game(user):
        word = GameService.generate_word()
        return Game.objects.create(user=user, word=word)

    @staticmethod
    def make_try(game, letter):
        is_correct = GameService.evaluate_letter(game.word, letter)
        return Try.objects.create(game=game, letter=letter.lower(), is_correct=is_correct)

    @staticmethod
    def make_try(game, letter):
        try_obj = Try(game=game, letter=letter)
        try_obj.is_correct = try_obj.check_if_correct()
        try_obj.save()

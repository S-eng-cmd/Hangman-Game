from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TryForm
from .models import Game
from .service import GameService


def index(request):
    current_game = None
    total_games = 0
    avg_tries = 0

    if request.user.is_authenticated:
        # Остання незавершена гра
        game = Game.objects.filter(user=request.user).order_by("id").last()
        current_game = game if game and not game.is_finished else None

        # Статистика
        games = Game.objects.filter(user=request.user)
        total_games = games.count()
        total_tries = sum(game.tries.count() for game in games)
        if current_game:
            # Була незавершена гра, віднімаємо
            total_games -= 1
            total_tries -= current_game.tries.count()

        avg_tries = total_tries / total_games if total_games else 0

    return render(
        request,
        "game/index.html",
        {
            "current_game": current_game,
            "total_games": total_games,
            "avg_tries": round(avg_tries, 2),
        },
    )


def signup(request):
    if request.method == "POST":
        # створити користувача
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def start_game(request):
    game = GameService.create_game(request.user)
    return redirect("play_game", game_id=game.id)




@login_required
def play_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id, user=request.user)

    form = TryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        letter = form.cleaned_data["letter"]
        GameService.make_try(game, letter)
        return redirect("play_game", game_id=game.id)

    tries = game.tries.order_by("-created_at")
    display_word = game.get_display_word()

    return render(
        request, "game/play_game.html", {"game": game, "form": form, "tries": tries, "display_word": display_word}
    )

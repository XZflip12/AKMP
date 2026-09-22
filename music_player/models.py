# pylint: disable=too-many-positional-arguments
"""Модели данных для музыкального плеера."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from linked_list import Composition, PlayList


class PlaybackState(str, Enum):
    """Статусы воспроизведения."""

    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class Track(Composition):
    """Расширенная модель музыкальной композиции."""

    def __init__(
        self,
        title: str = "",
        artist: str = "",
        duration: int = 0,
        track_id: str = "",
        genre: str = "",
        album: str = "",
        file_path: str = "",
    ) -> None:
        super().__init__(title=title, artist=artist, duration=duration)
        self.track_id = track_id
        self.genre = genre
        self.album = album
        self.file_path = file_path

    def __repr__(self) -> str:
        return f"Track(title={self.title!r}, artist={self.artist!r}, album={self.album!r})"


@dataclass
class PlaylistRecord:
    """Плейлист и его метаданные."""

    name: str = ""
    playlist: PlayList = field(default_factory=PlayList)
    description: str = ""


@dataclass
class PlayerSession:
    """Состояние текущего сеанса воспроизведения."""

    state: PlaybackState = PlaybackState.STOPPED
    current_playlist: str = ""
    current_track: str = ""
    volume: int = 100
    playlists: dict[str, PlaylistRecord] = field(default_factory=dict)

    def set_volume(self, value: int) -> None:
        """Устанавливает уровень громкости в диапазоне 0..100."""
        self.volume = max(0, min(100, value))

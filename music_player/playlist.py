"""Логика управления плейлистами."""

from __future__ import annotations

from linked_list import Composition, PlayList

from .models import PlaybackState, PlayerSession


class PlaylistManager:
    """Управляет несколькими плейлистами и состоянием сессии в приложении."""

    def __init__(self) -> None:
        self._playlists: dict[str, PlayList] = {}
        self._session = PlayerSession()

    @property
    def playlists(self) -> dict[str, PlayList]:
        """Возвращает словарь всех зарегистрированных плейлистов."""
        return self._playlists

    @property
    def current_playlist(self) -> PlayList | None:
        """Возвращает активный плейлист текущей сессии."""
        if not self._session.current_playlist:
            return None
        return self._playlists.get(self._session.current_playlist)

    @property
    def current_track(self) -> str | None:
        """Возвращает название текущей воспроизводимой композиции."""
        return self._session.current_track or None

    @property
    def state(self) -> PlaybackState:
        """Возвращает текущее состояние проигрывателя."""
        return self._session.state

    @state.setter
    def state(self, value: PlaybackState) -> None:
        """Устанавливает состояние проигрывателя."""
        self._session.state = value

    def create_playlist(self, name: str) -> PlayList:
        """Создаёт новый плейлист и делает его активным."""
        if name in self._playlists:
            raise ValueError(f"Playlist '{name}' already exists")
        playlist = PlayList()
        self._playlists[name] = playlist
        self._session.current_playlist = name
        return playlist

    def delete_playlist(self, name: str) -> None:
        """Удаляет плейлист по имени."""
        if name not in self._playlists:
            raise ValueError(f"Playlist '{name}' not found")
        del self._playlists[name]
        if self._session.current_playlist == name:
            self._session.current_playlist = ""
            self._session.current_track = ""

    def add_track(self, playlist_name: str, track: Composition) -> None:
        """Добавляет композицию в указанный плейлист."""
        playlist = self.get_playlist(playlist_name)
        playlist.append(track)

    def move_track(
        self, playlist_name: str, track: Composition, new_index: int
    ) -> None:
        """Перемещает композицию внутри плейлиста на новую позицию."""
        playlist = self.get_playlist(playlist_name)
        playlist.move_track(track, new_index)

    def remove_track(self, playlist_name: str, track: Composition) -> None:
        """Удаляет композицию из плейлиста с синхронизацией сессии."""
        playlist = self.get_playlist(playlist_name)
        playlist.remove(track)

        # Синхронизация сессии при удалении активного трека
        if self._session.current_playlist == playlist_name:
            if playlist.current is not None:
                self._session.current_track = playlist.current.title
            else:
                self._session.current_track = ""

    def set_current_track(
            self,
            playlist_name: str,
            track: Composition) -> None:
        """Устанавливает текущую композицию для проигрывания."""
        playlist = self.get_playlist(playlist_name)
        playlist.play_all(track)
        self._session.current_playlist = playlist_name
        self._session.current_track = track.title

    def clear(self) -> None:
        """Очищает все плейлисты и сбрасывает состояние сессии."""
        self._playlists.clear()
        self._session.current_playlist = ""
        self._session.current_track = ""
        self._session.state = PlaybackState.STOPPED

    def get_playlist(self, name: str) -> PlayList:
        """Получает плейлист по имени или вызывает ValueError."""
        if name not in self._playlists:
            raise ValueError(f"Playlist '{name}' not found")
        return self._playlists[name]

# pylint: disable=attribute-defined-outside-init, unused-argument, broad-exception-caught, no-else-return
# pylint: disable=attribute-defined-outside-init, unused-argument, broad-exception-caught
"""PyQt-интерфейс музыкального плеера с темой Gruvbox (Modern UI)."""

from __future__ import annotations

import os

import pygame
from PyQt5.QtCore import QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .models import PlaybackState, Track
from .playlist import PlaylistManager


class GruvboxPalette:
    """Палитра Gruvbox (Dark Hard)."""

    bg_dim = "#1d2021"
    bg0 = "#282828"
    bg1 = "#3c3836"
    bg2 = "#504945"
    bg3 = "#665c54"
    bg4 = "#7c6f64"
    fg = "#ebdbb2"
    fg0 = "#fbf1c7"
    red = "#fb4934"
    green = "#b8bb26"
    yellow = "#fabd2f"
    blue = "#83a598"
    purple = "#d3869b"
    aqua = "#8ec07c"
    gray = "#928374"


MODERN_STYLESHEET = f"""
    QMainWindow {{
        background-color: {GruvboxPalette.bg_dim};
    }}
    QWidget {{
        color: {GruvboxPalette.fg};
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }}

    /* Top Bar */
    QFrame#TitleBar {{
        background-color: {GruvboxPalette.bg0};
        border-bottom: 1px solid {GruvboxPalette.bg1};
    }}
    QLabel#WindowTitle {{
        font-weight: 600;
        font-size: 13px;
        color: {GruvboxPalette.gray};
    }}
    QPushButton#WinControlBtn {{
        background: transparent;
        border: none;
        border-radius: 0px;
        color: {GruvboxPalette.fg};
        font-size: 14px;
    }}
    QPushButton#WinControlBtn:hover {{
        background-color: {GruvboxPalette.bg2};
    }}
    QPushButton#WinCloseBtn {{
        background: transparent;
        border: none;
        border-radius: 0px;
        color: {GruvboxPalette.fg};
        font-size: 14px;
    }}
    QPushButton#WinCloseBtn:hover {{
        background-color: {GruvboxPalette.red};
        color: {GruvboxPalette.bg0};
    }}

    /* Panels & Containers */
    QFrame#Sidebar {{
        background-color: {GruvboxPalette.bg0};
        border-right: 1px solid {GruvboxPalette.bg1};
    }}
    QFrame#MainContent {{
        background-color: {GruvboxPalette.bg_dim};
    }}
    QFrame#PlayerBar {{
        background-color: {GruvboxPalette.bg0};
        border-top: 1px solid {GruvboxPalette.bg1};
    }}
    QFrame#CoverPlaceholder {{
        background-color: {GruvboxPalette.bg2};
        border-radius: 12px;
        border: 1px solid {GruvboxPalette.bg3};
    }}

    /* Typography */
    QLabel#SectionHeader {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: {GruvboxPalette.gray};
    }}
    QLabel#TrackTitle {{
        font-size: 20px;
        font-weight: 700;
        color: {GruvboxPalette.fg0};
    }}
    QLabel#TrackArtist {{
        font-size: 14px;
        color: {GruvboxPalette.gray};
    }}
    QLabel#TimeLabel {{
        font-size: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        color: {GruvboxPalette.gray};
    }}

    /* Lists */
    QListWidget {{
        background: transparent;
        border: none;
        outline: none;
    }}
    QListWidget::item {{
        background: transparent;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 2px;
        color: {GruvboxPalette.fg};
    }}
    QListWidget::item:hover {{
        background-color: {GruvboxPalette.bg1};
    }}
    QListWidget::item:selected {{
        background-color: {GruvboxPalette.bg2};
        color: {GruvboxPalette.green};
        font-weight: 600;
    }}

    /* Standard Buttons & Contrasts Fix */
    QPushButton {{
        background-color: {GruvboxPalette.bg2};
        border: none;
        border-radius: 6px;
        color: {GruvboxPalette.fg0};
        padding: 8px 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {GruvboxPalette.bg3};
    }}
    QPushButton#danger {{
        background-color: {GruvboxPalette.red};
        color: {GruvboxPalette.bg0};
    }}
    QPushButton#danger:hover {{
        background-color: #d33824;
    }}

    /* Icon Buttons */
    QPushButton.IconButton {{
        background: transparent;
        border: none;
        border-radius: 6px;
        padding: 0px;
    }}
    QPushButton.IconButton:hover {{
        background-color: {GruvboxPalette.bg2};
    }}
    QPushButton#PlayPauseBtn {{
        background-color: {GruvboxPalette.green};
        border-radius: 24px;
        padding: 0px;
    }}
    QPushButton#PlayPauseBtn:hover {{
        background-color: {GruvboxPalette.aqua};
    }}

    /* Sliders */
    QSlider::groove:horizontal {{
        height: 4px;
        background: {GruvboxPalette.bg2};
        border-radius: 2px;
    }}
    QSlider::sub-page:horizontal {{
        background: {GruvboxPalette.green};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {GruvboxPalette.fg0};
        width: 12px;
        height: 12px;
        margin: -4px 0;
        border-radius: 6px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {GruvboxPalette.aqua};
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }}
    QMessageBox {{
        background-color: {GruvboxPalette.bg0};
    }}
    QMessageBox QLabel {{
        color: {GruvboxPalette.fg};
    }}
    QMessageBox QPushButton {{
        background-color: {GruvboxPalette.bg2};
        color: {GruvboxPalette.fg0};
        border: 1px solid {GruvboxPalette.bg3};
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 600;
        min-width: 70px;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {GruvboxPalette.bg3};
    }}
"""


class MusicPlayerUI(QMainWindow):
    """Главное окно приложения с современным интерфейсом."""

    def __init__(self, manager: PlaylistManager | None = None) -> None:
        super().__init__()
        self.manager = manager or PlaylistManager()
        self.selected_playlist_name: str | None = None
        self.audio = None

        self._track_length_cache: dict[str, float] = {}
        self._start_offset: float = 0.0
        self._is_user_seeking: bool = False
        self._current_track: Track | None = None
        self._drag_pos: QPoint = QPoint()

        self.position_timer = QTimer(self)
        self.position_timer.setInterval(250)
        self.position_timer.timeout.connect(self._update_seek_position)

        self._init_audio()
        self._init_window_frame()
        self.setStyleSheet(MODERN_STYLESHEET)

        self._build_ui()
        self._load_demo_data()

    def _init_audio(self) -> None:
        try:
            pygame.init()
            pygame.mixer.init()
            self.audio = pygame.mixer
        except Exception:
            self.audio = None

    def _init_window_frame(self) -> None:
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.resize(1100, 700)
        self.setMinimumSize(900, 550)

    # --- Иконки из assets ---
    def _icon_path(self, name: str) -> str:
        candidates = [
            os.path.join(os.getcwd(), "assets", f"{name}.svg"),
            os.path.join(os.getcwd(), "assets", name),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return ""

    def _set_svg_icon(
            self,
            widget: QPushButton,
            icon_name: str,
            *,
            size: int = 24) -> None:
        icon_path = self._icon_path(icon_name)
        if icon_path:
            widget.setIcon(QIcon(icon_path))
            widget.setIconSize(QSize(size, size))
            widget.setText("")
        widget.setFixedSize(size + 12, size + 12)

    # --- Перетаскивание кастомного окна ---
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and event.y() < 40:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton and not self._drag_pos.isNull() and event.y() < 40:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_pos = QPoint()

    # --- Сборка UI ---
    def _build_ui(self) -> None:
        root_widget = QWidget()
        root_layout = QVBoxLayout(root_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Top Title Bar
        title_bar = self._build_title_bar()
        root_layout.addWidget(title_bar)

        # 2. Main Area (Sidebar + Content)
        work_area = QWidget()
        work_layout = QHBoxLayout(work_area)
        work_layout.setContentsMargins(0, 0, 0, 0)
        work_layout.setSpacing(0)

        sidebar = self._build_sidebar()
        content = self._build_main_content()

        work_layout.addWidget(sidebar)
        work_layout.addWidget(content, 1)

        root_layout.addWidget(work_area, 1)

        # 3. Bottom Player Bar
        player_bar = self._build_player_bar()
        root_layout.addWidget(player_bar)

        self.setCentralWidget(root_widget)

    def _build_title_bar(self) -> QFrame:
        title_bar = QFrame()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(38)

        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setSpacing(8)

        app_title = QLabel("PLAYER")
        app_title.setObjectName("WindowTitle")

        btn_minimize = QPushButton("—")
        btn_minimize.setObjectName("WinControlBtn")
        btn_minimize.setFixedSize(46, 38)
        btn_minimize.clicked.connect(self.showMinimized)

        btn_close = QPushButton("✕")
        btn_close.setObjectName("WinCloseBtn")
        btn_close.setFixedSize(46, 38)
        btn_close.clicked.connect(self.close)

        layout.addWidget(app_title)
        layout.addStretch(1)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)

        return title_bar

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        playlists_label = QLabel("ПЛЕЙЛИСТЫ")
        playlists_label.setObjectName("SectionHeader")

        add_btn = QPushButton()
        add_btn.setProperty("class", "IconButton")
        add_btn.setToolTip("Создать плейлист")
        self._set_svg_icon(add_btn, "square-plus", size=20)
        add_btn.clicked.connect(self._add_playlist)

        header_row.addWidget(playlists_label)
        header_row.addStretch(1)
        header_row.addWidget(add_btn)
        layout.addLayout(header_row)

        self.playlists = QListWidget()
        self.playlists.itemClicked.connect(self._on_playlist_selected)
        layout.addWidget(self.playlists)

        remove_btn = QPushButton("Удалить плейлист")
        remove_btn.setObjectName("danger")
        remove_btn.clicked.connect(self._remove_playlist)
        layout.addWidget(remove_btn)

        return sidebar

    def _build_main_content(self) -> QFrame:
        content = QFrame()
        content.setObjectName("MainContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 16)
        layout.setSpacing(16)

        # Track Header Info
        track_info_layout = QHBoxLayout()
        track_info_layout.setSpacing(20)

        self.cover_art = QFrame()
        self.cover_art.setObjectName("CoverPlaceholder")
        self.cover_art.setFixedSize(80, 80)
        cover_label = QLabel("♫", self.cover_art)
        cover_label.setAlignment(Qt.AlignCenter)
        cover_label.setStyleSheet(
            f"font-size: 32px; color: {GruvboxPalette.gray};")
        cover_layout = QVBoxLayout(self.cover_art)
        cover_layout.addWidget(cover_label)

        text_details = QVBoxLayout()
        text_details.setAlignment(Qt.AlignVCenter)
        self.current_title = QLabel("Выберите трек")
        self.current_title.setObjectName("TrackTitle")
        self.current_artist = QLabel("Исполнитель")
        self.current_artist.setObjectName("TrackArtist")

        text_details.addWidget(self.current_title)
        text_details.addWidget(self.current_artist)

        track_info_layout.addWidget(self.cover_art)
        track_info_layout.addLayout(text_details)
        track_info_layout.addStretch(1)

        layout.addLayout(track_info_layout)

        # Actions Row
        actions_row = QHBoxLayout()
        actions_row.setSpacing(8)

        add_track_btn = QPushButton("+ Добавить трек")
        add_track_btn.clicked.connect(self._add_track)

        remove_track_btn = QPushButton("Удалить")
        remove_track_btn.clicked.connect(self._remove_track)

        self.move_up_btn = QPushButton()
        self.move_up_btn.setProperty("class", "IconButton")
        self._set_svg_icon(self.move_up_btn, "square-caret-up", size=22)
        self.move_up_btn.clicked.connect(self._move_up)

        self.move_down_btn = QPushButton()
        self.move_down_btn.setProperty("class", "IconButton")
        self._set_svg_icon(self.move_down_btn, "square-caret-down", size=22)
        self.move_down_btn.clicked.connect(self._move_down)

        actions_row.addWidget(add_track_btn)
        actions_row.addWidget(remove_track_btn)
        actions_row.addStretch(1)
        actions_row.addWidget(self.move_up_btn)
        actions_row.addWidget(self.move_down_btn)

        layout.addLayout(actions_row)

        # Track List
        self.track_list = QListWidget()
        self.track_list.itemDoubleClicked.connect(
            self._on_track_double_clicked)
        layout.addWidget(self.track_list)

        return content

    def _build_player_bar(self) -> QFrame:
        player_bar = QFrame()
        player_bar.setObjectName("PlayerBar")
        player_bar.setFixedHeight(88)

        layout = QHBoxLayout(player_bar)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(24)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(6)

        controls_row = QHBoxLayout()
        controls_row.setSpacing(16)

        self.prev_button = QPushButton()
        self.prev_button.setProperty("class", "IconButton")
        self._set_svg_icon(self.prev_button, "circle-left", size=28)
        self.prev_button.clicked.connect(self._previous_track)

        self.play_button = QPushButton()
        self.play_button.setObjectName("PlayPauseBtn")
        self._set_play_icon(False)
        self.play_button.clicked.connect(self._toggle_playback)

        self.next_button = QPushButton()
        self.next_button.setProperty("class", "IconButton")
        self._set_svg_icon(self.next_button, "circle-right", size=28)
        self.next_button.clicked.connect(self._next_track)

        controls_row.addStretch(1)
        controls_row.addWidget(self.prev_button)
        controls_row.addWidget(self.play_button)
        controls_row.addWidget(self.next_button)
        controls_row.addStretch(1)

        progress_row = QHBoxLayout()
        progress_row.setSpacing(12)

        self.current_time_label = QLabel("00:00")
        self.current_time_label.setObjectName("TimeLabel")

        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 100)
        self.seek_slider.sliderPressed.connect(self._on_seek_pressed)
        self.seek_slider.sliderReleased.connect(self._on_seek_released)

        self.total_time_label = QLabel("00:00")
        self.total_time_label.setObjectName("TimeLabel")

        progress_row.addWidget(self.current_time_label)
        progress_row.addWidget(self.seek_slider, 1)
        progress_row.addWidget(self.total_time_label)

        center_layout.addLayout(controls_row)
        center_layout.addLayout(progress_row)

        volume_layout = QHBoxLayout()
        volume_layout.setSpacing(8)

        vol_icon = QLabel("🔊")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)

        volume_layout.addWidget(vol_icon)
        volume_layout.addWidget(self.volume_slider)

        layout.addLayout(center_layout, 1)
        layout.addLayout(volume_layout)

        return player_bar

    # --- Аудио / Плеер Логика ---
    @staticmethod
    def _format_time(seconds: float) -> str:
        total_seconds = max(0, int(seconds))
        minutes, seconds_left = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds_left:02d}"

    def _track_duration_seconds(self, track: Track | None) -> float:
        if track is None or not getattr(track, "file_path", None):
            return 0.0

        file_path = track.file_path
        if file_path in self._track_length_cache:
            return self._track_length_cache[file_path]

        if self.audio is None:
            return 0.0

        result = 0.0
        try:
            sound = pygame.mixer.Sound(file_path)
            result = float(sound.get_length())
        except Exception:
            pass

        if result > 0:
            self._track_length_cache[file_path] = result
        return result

    def _mixer_position_seconds(self) -> float:
        if self.audio is None or not self.audio.music.get_busy():
            return self._start_offset
        try:
            pos_ms = self.audio.music.get_pos()
            if pos_ms >= 0:
                return self._start_offset + (float(pos_ms) / 1000.0)
        except Exception:
            pass
        return self._start_offset

    def _sync_seek_slider(self, track: Track | None = None) -> None:
        if self._is_user_seeking:
            return

        current_track = track or self._get_selected_track()
        total_duration = self._track_duration_seconds(current_track)

        if total_duration <= 0:
            self.seek_slider.setRange(0, 100)
            self.seek_slider.setValue(0)
            self.current_time_label.setText("00:00")
            self.total_time_label.setText("00:00")
            return

        self.seek_slider.setRange(0, int(total_duration))
        current_pos_seconds = min(
            max(self._mixer_position_seconds(), 0.0), total_duration)

        self.seek_slider.blockSignals(True)
        self.seek_slider.setValue(int(current_pos_seconds))
        self.seek_slider.blockSignals(False)

        self.current_time_label.setText(self._format_time(current_pos_seconds))
        self.total_time_label.setText(self._format_time(total_duration))

    def _update_seek_position(self) -> None:
        if self.selected_playlist_name is None or self.audio is None:
            self.position_timer.stop()
            return

        track = self._get_selected_track()
        if track is None:
            self.position_timer.stop()
            return

        if self.audio.music.get_busy():
            self._sync_seek_slider(track)
        else:
            self.position_timer.stop()

    def _play_track_file(self, track: Track, start_from: float = 0.0) -> None:
        if self.audio is None or not getattr(track, "file_path", None):
            return
        try:
            self.audio.music.stop()
            self.audio.music.load(track.file_path)
            self.audio.music.set_volume(self.volume_slider.value() / 100.0)
            self._current_track = track
            self._start_offset = start_from

            try:
                self.audio.music.play(start=start_from)
            except Exception:
                self.audio.music.play()
                self._start_offset = 0.0

            self._sync_seek_slider(track)
            self.position_timer.start(250)
        except Exception:
            pass

    def _set_play_icon(self, playing: bool) -> None:
        icon_name = "circle-pause" if playing else "circle-play"
        self._set_svg_icon(self.play_button, icon_name, size=36)
        self.play_button.setProperty("is_playing", playing)

    def _on_seek_pressed(self) -> None:
        self._is_user_seeking = True

    def _on_seek_released(self) -> None:
        self._is_user_seeking = False
        if self.audio is None:
            return

        track = self._get_selected_track()
        if track is None or not getattr(track, "file_path", None):
            return

        seek_seconds = float(self.seek_slider.value())
        self._play_track_file(track, start_from=seek_seconds)
        self.manager.state = PlaybackState.PLAYING
        self._set_play_icon(True)

    def _toggle_playback(self) -> None:
        if self.selected_playlist_name is None:
            return

        is_playing = bool(self.play_button.property("is_playing"))
        if not is_playing:
            selected_track = self._get_selected_track()
            if selected_track is not None:
                self.manager.set_current_track(
                    self.selected_playlist_name, selected_track)
                if self._current_track == selected_track and self.audio is not None:
                    try:
                        if not self.audio.music.get_busy():
                            self._play_track_file(
                                selected_track, start_from=self._start_offset)
                            self.manager.state = PlaybackState.PLAYING
                            self._set_play_icon(True)
                            return
                        else:
                            self.audio.music.unpause()
                            self.position_timer.start(250)
                            self.manager.state = PlaybackState.PLAYING
                            self._set_play_icon(True)
                            return
                    except Exception:
                        pass
                self._play_track_file(
                    selected_track, start_from=self._start_offset)
            self.manager.state = PlaybackState.PLAYING
            self._set_play_icon(True)
        else:
            if self.audio is not None and self.audio.music.get_busy():
                self._start_offset = self._mixer_position_seconds()
                self.audio.music.pause()
            self.position_timer.stop()
            self.manager.state = PlaybackState.PAUSED
            self._set_play_icon(False)

    def _load_demo_data(self) -> None:
        demo_data = {
            "Рок": [
                ("Bohemian Rhapsody", "Queen"),
                ("Back in Black", "AC/DC"),
                ("Paint It Black", "The Rolling Stones"),
            ],
            "Джаз": [
                ("So What", "Miles Davis"),
                ("Take Five", "Dave Brubeck"),
                ("Blue in Green", "Miles Davis"),
            ],
            "Подкасты": [
                ("Python Weekly", "Python Community"),
                ("Deep Dive", "Engineering Podcast"),
                ("Dev Notes", "Software Team"),
            ],
        }
        self.manager.clear()
        for playlist_name, tracks in demo_data.items():
            self.manager.create_playlist(playlist_name)
            for title, artist in tracks:
                self.manager.add_track(
                    playlist_name,
                    Track(
                        title=title,
                        artist=artist,
                        track_id=f"{playlist_name}:{title}",
                        genre="demo",
                    ),
                )

        self._refresh_playlist_list()
        if self.playlists.count():
            self.playlists.setCurrentRow(0)
            self._on_playlist_selected(self.playlists.currentItem())

    def _refresh_playlist_list(self) -> None:
        self.playlists.clear()
        for playlist_name in self.manager.playlists:
            self.playlists.addItem(QListWidgetItem(playlist_name))

    def _set_track_info(self, track: Track | None) -> None:
        if track is None:
            self.current_title.setText("Выберите трек")
            self.current_artist.setText("Исполнитель")
            return
        self.current_title.setText(track.title)
        self.current_artist.setText(track.artist)

    def _select_track_item(self, track: Track) -> None:
        for index in range(self.track_list.count()):
            item = self.track_list.item(index)
            if item.data(Qt.UserRole) == track:
                self.track_list.setCurrentItem(item)
                return

    def _get_selected_track(self) -> Track | None:
        item = self.track_list.currentItem()
        if item is None:
            return None
        return item.data(Qt.UserRole)

    def _refresh_tracks_for_current_playlist(self) -> None:
        self.track_list.clear()
        if (
            not self.selected_playlist_name
            or self.selected_playlist_name not in self.manager.playlists
        ):
            self._set_track_info(None)
            return

        playlist = self.manager.playlists[self.selected_playlist_name]
        for track in playlist:
            item = QListWidgetItem(f"{track.title}  —  {track.artist}")
            item.setData(Qt.UserRole, track)
            self.track_list.addItem(item)

        current = playlist.current
        if current is not None:
            self._select_track_item(current)
            self._set_track_info(current)
        elif self.track_list.count() > 0:
            first_track = self.track_list.item(0).data(Qt.UserRole)
            self._set_track_info(first_track)

    def _on_playlist_selected(self, item: QListWidgetItem) -> None:
        if item is None:
            return
        self.selected_playlist_name = item.text()
        self.manager._session.current_playlist = self.selected_playlist_name
        self._refresh_tracks_for_current_playlist()

        outline = self.manager.playlists.get(self.selected_playlist_name)
        if outline is not None and not outline.current and self.track_list.count() > 0:
            first_track = self.track_list.item(0).data(Qt.UserRole)
            self.manager.set_current_track(
                self.selected_playlist_name, first_track)
            self._set_track_info(first_track)

    def _on_track_double_clicked(self, item: QListWidgetItem) -> None:
        if item is None or self.selected_playlist_name is None:
            return
        track = item.data(Qt.UserRole)
        self.manager.set_current_track(self.selected_playlist_name, track)
        self._set_track_info(track)
        self._play_track_file(track)
        self.manager.state = PlaybackState.PLAYING
        self._set_play_icon(True)

    def _previous_track(self) -> None:
        if self.selected_playlist_name is None:
            return
        playlist = self.manager.playlists[self.selected_playlist_name]
        if not playlist:
            return
        previous = playlist.previous_track()
        if previous is None:
            return
        self.manager.set_current_track(self.selected_playlist_name, previous)
        self._set_track_info(previous)
        self._select_track_item(previous)
        self._play_track_file(previous)
        self.manager.state = PlaybackState.PLAYING
        self._set_play_icon(True)

    def _next_track(self) -> None:
        if self.selected_playlist_name is None:
            return
        playlist = self.manager.playlists[self.selected_playlist_name]
        if not playlist:
            return
        next_track = playlist.next_track()
        if next_track is None:
            return
        self.manager.set_current_track(self.selected_playlist_name, next_track)
        self._set_track_info(next_track)
        self._select_track_item(next_track)
        self._play_track_file(next_track)
        self.manager.state = PlaybackState.PLAYING
        self._set_play_icon(True)

    def _move_up(self) -> None:
        if self.selected_playlist_name is None:
            return
        current_item = self.track_list.currentItem()
        if current_item is None:
            return
        current_index = self.track_list.currentRow()
        if current_index <= 0:
            return
        track = current_item.data(Qt.UserRole)
        self.manager.move_track(
            self.selected_playlist_name, track, current_index - 1)
        self._refresh_tracks_for_current_playlist()
        self._select_track_item(track)

    def _move_down(self) -> None:
        if self.selected_playlist_name is None:
            return
        current_item = self.track_list.currentItem()
        if current_item is None:
            return
        current_index = self.track_list.currentRow()
        if current_index < 0 or current_index >= self.track_list.count() - 1:
            return
        track = current_item.data(Qt.UserRole)
        self.manager.move_track(
            self.selected_playlist_name, track, current_index + 1)
        self._refresh_tracks_for_current_playlist()
        self._select_track_item(track)

    def _on_volume_changed(self, value: int) -> None:
        if self.audio is not None:
            self.audio.music.set_volume(value / 100.0)

    def _add_playlist(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Выберите папку для плейлиста")
        if not folder:
            return
        playlist_name = os.path.basename(folder).strip()
        if not playlist_name:
            QMessageBox.warning(self, "Плейлист", "Папка не выбрана.")
            return
        if playlist_name in self.manager.playlists:
            QMessageBox.warning(
                self, "Плейлист", "Плейлист с таким именем уже существует.")
            return
        playlist = self.manager.create_playlist(playlist_name)
        for file_name in sorted(os.listdir(folder)):
            lower_name = file_name.lower()
            if lower_name.endswith((".mp3", ".wav", ".ogg", ".flac", ".m4a")):
                file_path = os.path.join(folder, file_name)
                track = Track(
                    title=os.path.splitext(file_name)[0],
                    artist="Локальный файл",
                    track_id=f"{playlist_name}:{file_name}",
                    genre="local",
                    file_path=file_path,
                )
                playlist.append(track)
        self._refresh_playlist_list()
        self.playlists.setCurrentRow(self.playlists.count() - 1)
        self._on_playlist_selected(self.playlists.currentItem())

    def _remove_playlist(self) -> None:
        current_row = self.playlists.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Удаление", "Сначала выберите плейлист.")
            return
        playlist_name = self.playlists.item(current_row).text()
        self.manager.delete_playlist(playlist_name)
        self._refresh_playlist_list()
        self.selected_playlist_name = None
        if self.playlists.count() > 0:
            self.playlists.setCurrentRow(0)
            self._on_playlist_selected(self.playlists.currentItem())
        else:
            self.track_list.clear()
            self._set_track_info(None)

    def _add_track(self) -> None:
        if self.selected_playlist_name is None:
            QMessageBox.warning(self, "Добавление трека",
                                "Сначала выберите плейлист.")
            return

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите музыкальные файлы",
            os.getcwd(),
            "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a)",
        )
        if not file_paths:
            return

        for file_path in file_paths:
            track = Track(
                title=os.path.splitext(
                    os.path.basename(file_path))[0],
                artist="Локальный файл",
                track_id=f"{
                    self.selected_playlist_name}:{
                    os.path.basename(file_path)}",
                genre="local",
                file_path=file_path,
            )
            self.manager.add_track(self.selected_playlist_name, track)
        self._refresh_tracks_for_current_playlist()

    def _remove_track(self) -> None:
        current_item = self.track_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Удаление", "Сначала выберите трек.")
            return

        track = current_item.data(Qt.UserRole)
        self.manager.remove_track(self.selected_playlist_name, track)
        self._refresh_tracks_for_current_playlist()


def run_app() -> None:
    """Создаёт и запускает приложение PyQt."""
    app = QApplication([])
    window = MusicPlayerUI()
    window.show()
    app.exec_()

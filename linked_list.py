"""Модуль базовых классов двусвязного кольцевого списка и плейлиста."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class LinkedListItem(Generic[T]):
    """Узел двусвязного списка с автосвязыванием соседей."""

    def __init__(self, data: T | None = None) -> None:
        self.data: T | None = data
        self._next: LinkedListItem[T] | None = None
        self._previous: LinkedListItem[T] | None = None

    @property
    def next_item(self) -> LinkedListItem[T] | None:
        """Возвращает следующий узел."""
        return self._next

    @next_item.setter
    def next_item(self, value: LinkedListItem[T] | None) -> None:
        """Устанавливает следующий узел и связывает его с текущим."""
        self._next = value
        if value is not None and value._previous is not self:
            value._previous = self

    @property
    def previous_item(self) -> LinkedListItem[T] | None:
        """Возвращает предыдущий узел."""
        return self._previous

    @previous_item.setter
    def previous_item(self, value: LinkedListItem[T] | None) -> None:
        """Устанавливает предыдущий узел и связывает его с текущим."""
        self._previous = value
        if value is not None and value._next is not self:
            value._next = self

    def __repr__(self) -> str:
        return f"LinkedListItem(data={self.data!r})"


class LinkedList(Generic[T]):
    """Кольцевой двусвязный список."""

    def __init__(self, first_item: LinkedListItem[T] | None = None) -> None:
        self.first_item: LinkedListItem[T] | None = first_item

    @property
    def last(self) -> LinkedListItem[T] | None:
        """Возвращает последний узел списка."""
        if self.first_item is None:
            return None
        return self.first_item.previous_item

    def _get_node_at(self, index: int) -> LinkedListItem[T]:
        """Возвращает узел по указанному индексу."""
        size = len(self)
        if index < 0:
            index += size
        if index < 0 or index >= size or self.first_item is None:
            raise IndexError("List index out of range")

        current = self.first_item
        for _ in range(index):
            if current is not None:
                current = current.next_item
        if current is None:
            raise IndexError("List index out of range")
        return current

    def append_left(self, item: T) -> None:
        """Добавляет элемент в начало списка."""
        new_node = LinkedListItem(item)
        if self.first_item is None:
            new_node.next_item = new_node
            new_node.previous_item = new_node
            self.first_item = new_node
        else:
            last_node = self.last
            new_node.next_item = self.first_item
            if last_node is not None:
                last_node.next_item = new_node
            self.first_item = new_node

    def append_right(self, item: T) -> None:
        """Добавляет элемент в конец списка."""
        if self.first_item is None:
            self.append_left(item)
            return

        new_node = LinkedListItem(item)
        last_node = self.last
        if last_node is not None:
            last_node.next_item = new_node
        new_node.next_item = self.first_item

    def append(self, item: T) -> None:
        """Добавляет элемент в конец списка (алиас для append_right)."""
        self.append_right(item)

    def remove(self, item: T) -> None:
        """Удаляет первое вхождение элемента со значением item."""
        if self.first_item is None:
            raise ValueError(f"Element {item!r} is not in the list")

        current = self.first_item
        size = len(self)
        target_node: LinkedListItem[T] | None = None

        for _ in range(size):
            if current is not None and current.data == item:
                target_node = current
                break
            if current is not None:
                current = current.next_item

        if target_node is None:
            raise ValueError(f"Element {item!r} is not in the list")

        if size == 1:
            self.first_item = None
        else:
            prev_node = target_node.previous_item
            next_node = target_node.next_item
            if prev_node is not None:
                prev_node.next_item = next_node
            if target_node is self.first_item:
                self.first_item = next_node

    def insert(self, previous: LinkedListItem[T], item: T) -> None:
        """Вставляет элемент справа от узла previous."""
        if self.first_item is None:
            self.append_left(item)
            return

        new_node = LinkedListItem(item)
        next_node = previous.next_item

        previous.next_item = new_node
        new_node.next_item = next_node

    def move_track(self, item: T, new_index: int) -> None:
        """Перемещает элемент внутри списка на позицию new_index."""
        if item in self:
            self.remove(item)

        size = len(self)
        if size == 0 or new_index <= 0:
            self.append_left(item)
            return

        if new_index >= size:
            self.append_right(item)
            return

        prev_node = self._get_node_at(new_index - 1)
        self.insert(prev_node, item)

    def __len__(self) -> int:
        if self.first_item is None:
            return 0
        count = 1
        current = self.first_item.next_item
        while current is not None and current is not self.first_item:
            count += 1
            current = current.next_item
        return count

    def __iter__(self) -> Iterator[LinkedListItem[T]]:
        if self.first_item is None:
            return
        current = self.first_item
        size = len(self)
        for _ in range(size):
            if current is None:
                break
            yield current
            current = current.next_item

    def __getitem__(self, index: int) -> LinkedListItem[T]:
        return self._get_node_at(index)

    def __contains__(self, item: object) -> bool:
        if self.first_item is None:
            return False
        current = self.first_item
        size = len(self)
        for _ in range(size):
            if current is not None and current.data == item:
                return True
            if current is not None:
                current = current.next_item
        return False

    def __reversed__(self) -> Iterator[LinkedListItem[T]]:
        last_node = self.last
        if last_node is None:
            return
        current = last_node
        size = len(self)
        for _ in range(size):
            if current is None:
                break
            yield current
            current = current.previous_item

    def __repr__(self) -> str:
        return f"LinkedList({[item.data for item in self]!r})"


class Composition:
    """Базовый класс музыкальной композиции."""

    def __init__(
        self,
        title: str = "",
        artist: str = "",
        duration: int = 0,
        file_path: str = "",
    ) -> None:
        self.title = title
        self.artist = artist
        self.duration = duration
        self.file_path = file_path

    def __repr__(self) -> str:
        return f"Composition(title={self.title!r}, artist={self.artist!r})"


class PlayList(LinkedList[Composition]):
    """Класс плейлиста, наследующий кольцевой двусвязный список."""

    def __init__(
        self,
        name: str = "",
        first_item: LinkedListItem[Composition] | None = None,
    ) -> None:
        super().__init__(first_item)
        self.name = name
        self._current_node: LinkedListItem[Composition] | None = first_item

    @property
    def current(self) -> Composition | None:
        """Возвращает текущую воспроизводимую композицию."""
        if self._current_node is None:
            return None
        return self._current_node.data

    @current.setter
    def current(
        self, value: Composition | LinkedListItem[Composition] | None
    ) -> None:
        """Устанавливает текущую композицию."""
        if value is None:
            self._current_node = None
        elif isinstance(value, LinkedListItem):
            self._current_node = value
        else:
            curr = self.first_item
            size = len(self)
            found = None
            for _ in range(size):
                if curr is not None and curr.data == value:
                    found = curr
                    break
                if curr is not None:
                    curr = curr.next_item
            self._current_node = found

    def play_all(
        self, track: Composition | LinkedListItem[Composition] | None = None
    ) -> None:
        """Устанавливает активный трек для воспроизведения."""
        if track is None:
            self._current_node = self.first_item
            return

        if isinstance(track, LinkedListItem):
            self._current_node = track
            return

        if self.first_item is not None:
            current_node = self.first_item
            size = len(self)
            for _ in range(size):
                if current_node is not None and (
                    current_node.data == track or current_node is track
                ):
                    self._current_node = current_node
                    break
                if current_node is not None:
                    current_node = current_node.next_item

    def next_track(self) -> Composition | None:
        """Переходит к следующему треку по кольцу и возвращает его."""
        if self._current_node is None:
            self._current_node = self.first_item

        if self._current_node is not None and self._current_node.next_item is not None:
            self._current_node = self._current_node.next_item
            return self._current_node.data
        return None

    def prev_track(self) -> Composition | None:
        """Переходит к предыдущему треку по кольцу и возвращает его."""
        if self._current_node is None:
            self._current_node = self.first_item

        if (
            self._current_node is not None
            and self._current_node.previous_item is not None
        ):
            self._current_node = self._current_node.previous_item
            return self._current_node.data
        return None

    def previous_track(self) -> Composition | None:
        """Алиас для prev_track."""
        return self.prev_track()

    def remove(self, item: Composition) -> None:
        """Удаляет трек из плейлиста и обновляет ссылку на текущий трек."""
        target_node: LinkedListItem[Composition] | None = None
        if self.first_item is not None:
            curr = self.first_item
            for _ in range(len(self)):
                if curr is not None and curr.data == item:
                    target_node = curr
                    break
                if curr is not None:
                    curr = curr.next_item

        super().remove(item)

        if self._current_node is target_node:
            if self.first_item is None:
                self._current_node = None
            else:
                self._current_node = (
                    target_node.next_item
                    if target_node is not None
                    else self.first_item
                )

    def __iter__(self) -> Iterator[Composition]:
        """Итератор по объектам Composition (а не по узлам)."""
        if self.first_item is None:
            return
        current = self.first_item
        size = len(self)
        for _ in range(size):
            if current is None or current.data is None:
                break
            yield current.data
            current = current.next_item
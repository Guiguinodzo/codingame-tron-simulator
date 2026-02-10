from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTextEdit
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtCore import Qt


class PlayersLogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tabs = QTabWidget(self)
        self.text_edits: list[QTextEdit] = []
        self.step_positions: dict[tuple[int, int], tuple[int, int]] = {}

        for i in range(4):
            edit = QTextEdit()
            edit.setReadOnly(True)

            self.text_edits.append(edit)
            self.tabs.addTab(edit, f"Player {i+1}")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

    # -----------------------------------------------------

    def fill_texts(self):
        self.step_positions.clear()

        total_steps = self.get_total_step_number()

        for player_id, edit in enumerate(self.text_edits):
            edit.clear()
            cursor = edit.textCursor()

            for step in range(total_steps):
                text = self.get_player_stderr_at(step, player_id)

                if not text:
                    continue

                start = cursor.position()
                block = f"[STEP {step}]\n{text}\n\n"

                cursor.insertText(block)

                length = len(block)
                self.step_positions[(player_id, step)] = (start, length)

    # -----------------------------------------------------

    def highlight_step(self, step: int):
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor(0, 246, 255, 80))

        clear_format = QTextCharFormat()
        clear_format.setBackground(Qt.transparent)

        for player_id, edit in enumerate(self.text_edits):
            cursor = edit.textCursor()

            # clear previous highlights
            cursor.select(QTextCursor.Document)
            cursor.setCharFormat(clear_format)

            key = (player_id, step)
            if key not in self.step_positions:
                continue

            start, length = self.step_positions[key]

            cursor.setPosition(start)
            cursor.setPosition(start + length, QTextCursor.KeepAnchor)
            cursor.setCharFormat(highlight_format)

            # scroll to position
            view_cursor = edit.textCursor()
            view_cursor.setPosition(start)
            edit.setTextCursor(view_cursor)
            edit.ensureCursorVisible()

    # -----------------------------------------------------
    # Ces méthodes existent déjà chez toi, ici juste pour type

    def get_player_stderr_at(self, step: int, player_id: int) -> str:
        raise NotImplementedError

    def get_total_step_number(self) -> int:
        raise NotImplementedError

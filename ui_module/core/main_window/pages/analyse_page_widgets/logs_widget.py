from html import escape

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel, QComboBox

from ui_module.utils.world import World


class LogsWidget(QWidget):
    group_id_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.text_edit.setStyleSheet("""
        QTextEdit {
            background: transparent;
            border: 1px solid rgba(0, 246, 255, 120);
            border-radius: 8px;
            color: rgb(180, 255, 255);
            font-family: Consolas, Courier, monospace;
            font-size: 13px;
            selection-background-color: rgba(0, 246, 255, 120);
        }

        /* ========= TRON SCROLLBAR ========= */

        QTextEdit QScrollBar:vertical {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(0,0,0,200),
                stop:0.5 rgba(0,246,255,30),
                stop:1 rgba(0,0,0,200)
            );
            width: 14px;
            margin: 2px;
            border-radius: 7px;
            border: 1px solid rgba(0,246,255,120);
        }

        QTextEdit QScrollBar::handle:vertical {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(0,246,255,200),
                stop:0.5 rgba(125,249,255,255),
                stop:1 rgba(0,246,255,200)
            );
            min-height: 30px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,180);
        }

        QTextEdit QScrollBar::handle:vertical:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(0,246,255,255),
                stop:0.5 rgba(180,255,255,255),
                stop:1 rgba(0,246,255,255)
            );
            border: 1px solid white;
        }

        QTextEdit QScrollBar::handle:vertical:pressed {
            background: rgba(180,255,255,255);
        }

        QTextEdit QScrollBar::add-line:vertical,
        QTextEdit QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QTextEdit QScrollBar::add-page:vertical,
        QTextEdit QScrollBar::sub-page:vertical {
            background: transparent;
        }
        """)

        self.hide_h_widget = QWidget()
        h_layout = QHBoxLayout(self)
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("Overlay: ")
        self.label.setStyleSheet("color:#7df9ff; font-size:14px;")
        self.combo_box = QComboBox()
        h_layout.addWidget(self.label)
        h_layout.addWidget(self.combo_box)
        h_layout.addStretch(1)
        self.hide_h_widget.setLayout(h_layout)
        self.hide_h_widget.setVisible(False)
        self.activate_combo_box = True
        self.combo_box.currentIndexChanged.connect(self._combo_box_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(self.hide_h_widget)
        layout.addWidget(self.text_edit)

        self.world = World()

        # step -> (player_id, text)
        self.logs_by_step: dict[int, tuple[int, str]] = {}

    # -----------------------------------------------------

    def fill_texts(self):

        self.logs_by_step.clear()

        total_steps = self.world.simulator.get_total_step_number()

        for step in range(total_steps):
            step_details = self.world.simulator.get_step_details(step)
            if not step_details.logs:
                continue
            text = "\n".join(step_details.logs)
            self.logs_by_step[step] = (step_details.player_id, text)

    # -----------------------------------------------------

    def _combo_box_changed(self, index):
        if index == 0:
            self.group_id_changed.emit(None)
        else:
            self.group_id_changed.emit(self.combo_box.currentText())

    def highlight_step(self, step: int):

        if step not in self.logs_by_step:
            self.text_edit.clear()
            return

        player_id, text = self.logs_by_step[step]

        group_ids = ["Default"]
        step_details = self.world.simulator.get_step_details(step)
        for instruction_set in step_details.instructions:
            if instruction_set.get_group_id() is not None:
                group_ids.append(instruction_set.get_group_id())

        self.hide_h_widget.setVisible(len(group_ids) > 1)
        if len(group_ids) > 1:
            self.activate_combo_box = False
            self.combo_box.clear()
            for text in group_ids:
                self.combo_box.addItem(text)
            self.combo_box.setCurrentIndex(0)
            self.activate_combo_box = True

        color_name = self.world.player_settings.get_color(player_id).name()

        html = f"""
        <div style="color:#9ff;">

            <div style="
                font-size:18px;
                letter-spacing:2px;
                color:#00f6ff;
                text-shadow: 0 0 6px #00f6ff;
                margin-bottom:6px;
            ">
                <span style="color:{color_name}; text-shadow:0 0 6px {color_name};">
                    PLAYER {player_id + 1}
                </span>
                <span>
                    (decision time: {step_details.duration*1000:.3f} ms)
                </span>
            </div>

            <hr style="
                border:none;
                height:1px;
                background: linear-gradient(to right, transparent, #00f6ff, transparent);
                margin-bottom:10px;
            ">

            <pre style="
                margin:0;
                white-space:pre-wrap;
                font-size:13px;
            ">{escape(text)}</pre>

        </div>
        """

        self.text_edit.setHtml(html)


from html import escape

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

from ui_module.utils.world import World


class LogsWidget(QWidget):
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

        layout = QVBoxLayout(self)
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

    def highlight_step(self, step: int):

        if step not in self.logs_by_step:
            self.text_edit.clear()
            return

        player_id, text = self.logs_by_step[step]
        step_details = self.world.simulator.get_step_details(step)

        html = f"""
        <div style="color:#9ff;">

            <div style="
                font-size:18px;
                letter-spacing:2px;
                color:#00f6ff;
                text-shadow: 0 0 6px #00f6ff;
                margin-bottom:6px;
            ">
                PLAYER {player_id + 1} (decision time: {step_details.duration*1000:.3f} ms)
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


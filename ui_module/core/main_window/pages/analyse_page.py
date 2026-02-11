from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSplitter

from ui_module.core.main_window.pages.analyse_page_widgets.board_game_widget import BoardGameWidget
from ui_module.core.main_window.pages.analyse_page_widgets.logs_widget import LogsWidget
from ui_module.core.main_window.pages.analyse_page_widgets.players_settings_widget import PlayersSettingsWidget
from ui_module.utils.world import absolute_path_str, World
from ui_module.utils.qt.qt_utils import put_in_frame

class AnalysePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("AnalysePage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet(f"""
            QWidget#AnalysePage {{
                background-image: url("{absolute_path_str("ui_files/images/background_1.png")}");
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_widget = QWidget()
        main_layout.addWidget(main_widget)
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(20, 20, 20, 20)
        h_layout.setSpacing(20)

        left_widget = QSplitter(Qt.Vertical)

        self.board_game_widget = BoardGameWidget()

        self.logs_widget = LogsWidget()

        self.board_game_widget.state_changed.connect(self.logs_widget.highlight_step)

        World().simulator.finished.connect(self.logs_widget.fill_texts)

        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(put_in_frame(self.logs_widget))
        bottom_widget.setLayout(bottom_layout)

        left_widget.addWidget(put_in_frame(self.board_game_widget))
        left_widget.addWidget(bottom_widget)

        left_widget.setChildrenCollapsible(False)

        left_widget.setStyleSheet("""
            QSplitter::handle {
                background: rgba(0,0,0,0);
            }

            QSplitter::handle:hover {
                background: rgba(0,0,0,0);
            }

            QSplitter::handle:vertical {
                height: 20px;
            }
        """)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)

        QTimer.singleShot(0, lambda: left_widget.setSizes([1, 200]))

        self.players_settings_widget = PlayersSettingsWidget()

        right_layout.addWidget(put_in_frame(self.players_settings_widget))

        self.players_settings_widget.start_simulation.connect(self.board_game_widget.simulator_started)

        right_widget.setLayout(right_layout)

        h_layout.addWidget(left_widget)
        h_layout.addWidget(right_widget)

        h_layout.setStretch(0, 2)
        h_layout.setStretch(1, 1)
        main_widget.setLayout(h_layout)

        self.setLayout(main_layout)
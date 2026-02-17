from pathlib import Path

THEME_DIR = Path(__file__).parent / "themes"

def load_theme(name: str) -> str:
    path = THEME_DIR / f"{name}.qss"
    return path.read_text(encoding="utf-8")

def get_str_path(name: str) -> str:
    path = THEME_DIR / f"{name}.qss"
    return path

NAVY_LITE = """QWidget {
    background-color: #2e3440; /* main background */
    color: #d8dee9;            /* default text color */
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 12pt;
    }

    /* ==== Buttons ==== */
    QPushButton, QToolButton {
        background-color: #4c566a;  /* default button bg */
        color: #eceff4;             /* default button text */
        border: 3px solid red;
        border-radius: 4px;
        padding: 5px 12px;
    }

    QPushButton:hover, QToolButton:hover {
        background-color: #5e81ac; /* hover accent */
    }

    QPushButton:pressed, QToolButton:pressed {
        background-color: #81a1c1; /* pressed accent */
    }

    QPushButton:disabled, QToolButton:disabled {
        background-color: #3b4252;
        color: #4c566a;
    }

    /* ==== Checked/Selected Buttons ==== */
    QToolButton:checked {
        background-color: #5e81ac;  /* theme accent */
        color: #eceff4;
    }

    /* ==== Labels ==== */
    QLabel {
        color: #d8dee9;
    }

    /* ==== Scrollbars ==== */
    QScrollBar:vertical {
        background: #3b4252;
        width: 8px;
    }

    QScrollBar::handle:vertical {
        background: #5e81ac;
        border-radius: 4px;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }

    /* ==== SVG / Icons ==== */
    QToolButton svg, QLabel svg {
        fill: currentColor;
        stroke: currentColor;
    }

        QHeaderView::section {
    background-color: #3b4252;
    color: #eceff4;
    padding: 4px;
    border: 3px solid red;
}

    QTabWidget::pane {
    border: 3px solid red;
}

    QTabBar::tab {
        background: #3b4252;
        padding: 6px 12px;
    }

    QTabBar::tab:selected {
        background: #5e81ac;
    }

        QMenu {
        background-color: #2e3440;
        border: 3px solid red;
    }

    QMenu::item:selected {
        background-color: #5e81ac;
    }

    QPushButton:default { border: 3px solid red; }
    QPushButton:checked { background: #81a1c1; }
    QWidget:!enabled { color: #4c566a; }

    """

ORANGE_STAR = """QWidget {
    background-color: #f4f1ec;   /* warm neutral */
    color: #3a2f1d;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 12pt;
}

/* ==== Buttons ==== */
QPushButton, QToolButton {
    background-color: #fde68a;   /* light amber */
    color: #3a2f1d;
    border: 3px solid red;
    border-radius: 6px;
    padding: 6px 14px;
}

QPushButton:hover, QToolButton:hover {
    background-color: #fbbf24;   /* amber */
}

QPushButton:pressed, QToolButton:pressed {
    background-color: #d97706;   /* deep orange */
    color: #ffffff;
}

QPushButton:disabled, QToolButton:disabled {
    background-color: #e5e1d8;
    color: #9a8f7a;
}

/* ==== Checked ==== */
QToolButton:checked {
    background-color: #d97706;
    color: white;
}

/* ==== Labels ==== */
QLabel {
    color: #3a2f1d;
}

/* ==== Scrollbars ==== */
QScrollBar:vertical {
    background: #ede9e3;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: #f59e0b;
    border-radius: 4px;
}

/* ==== Tabs ==== */
QTabBar::tab {
    background: #ede9e3;
    padding: 6px 12px;
}

QTabBar::tab:selected {
    background: #f59e0b;
    color: #1f1608;
}

/* ==== Menus ==== */
QMenu {
    background-color: #ffffff;
    border: 3px solid red;
}

QMenu::item:selected {
    background-color: #fde68a;
}

    """

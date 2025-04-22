import sys
import pyperclip  # For Copying Link
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QWidget, QAction, QTabWidget, QFileDialog, QMenu
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Custom Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        self.dark_mode_enabled = False  # Dark Mode Flag

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.create_new_tab("https://www.google.com")

        # Menu Bar
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.create_new_tab("https://www.google.com"))
        self.file_menu.addAction(new_tab_action)

        history_action = QAction("History", self)
        history_action.triggered.connect(self.show_history)
        self.file_menu.addAction(history_action)

        self.apply_light_mode()

    def create_new_tab(self, url):
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Navigation Bar
        nav_bar = QHBoxLayout()
        button_style = """
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 20px;
                padding: 10px;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """

        back_btn = QPushButton("◀")
        forward_btn = QPushButton("▶")
        reload_btn = QPushButton("⟳")
        home_btn = QPushButton("🏠")
        dark_mode_btn = QPushButton("Dark Mode")
        copy_link_btn = QPushButton("📋")  # Copy Button
        new_tab_btn = QPushButton("➕")  # Open in New Tab Button

        for btn in [back_btn, forward_btn, reload_btn, home_btn, copy_link_btn, new_tab_btn]:
            btn.setStyleSheet(button_style)

        dark_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)

        dark_mode_btn.clicked.connect(self.toggle_dark_mode)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(lambda: self.navigate_to_url(browser))

        nav_bar.addWidget(back_btn)
        nav_bar.addWidget(forward_btn)
        nav_bar.addWidget(reload_btn)
        nav_bar.addWidget(home_btn)
        nav_bar.addWidget(dark_mode_btn)
        nav_bar.addWidget(copy_link_btn)
        nav_bar.addWidget(new_tab_btn)
        nav_bar.addWidget(self.url_bar)

        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(lambda qurl: self.url_bar.setText(qurl.toString()))
        browser.page().profile().downloadRequested.connect(self.download_file)

        back_btn.clicked.connect(browser.back)
        forward_btn.clicked.connect(browser.forward)
        reload_btn.clicked.connect(browser.reload)
        home_btn.clicked.connect(lambda: browser.setUrl(QUrl("https://www.google.com")))

        copy_link_btn.clicked.connect(lambda: self.copy_link(browser))
        new_tab_btn.clicked.connect(lambda: self.create_new_tab(self.url_bar.text()))

        layout.addLayout(nav_bar)
        layout.addWidget(browser)
        new_tab.setLayout(layout)

        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)

    def navigate_to_url(self, browser):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        browser.setUrl(QUrl(url))
        self.save_history(url)

    def copy_link(self, browser):
        url = browser.url().toString()
        pyperclip.copy(url)

    def save_history(self, url):
        with open("history.txt", "a") as file:
            file.write(url + "\n")

    def show_history(self):
        history_tab = QWidget()
        layout = QVBoxLayout()

        try:
            with open("history.txt", "r") as file:
                history_data = file.readlines()
        except FileNotFoundError:
            history_data = []

        for url in history_data:
            url_button = QPushButton(url.strip())
            url_button.clicked.connect(lambda _, u=url.strip(): self.create_new_tab(u))
            layout.addWidget(url_button)

        history_tab.setLayout(layout)
        index = self.tabs.addTab(history_tab, "History")
        self.tabs.setCurrentIndex(index)

    def download_file(self, download_item):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.url().fileName())
        if file_path:
            download_item.setPath(file_path)
            download_item.accept()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def toggle_dark_mode(self):
        if self.dark_mode_enabled:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()
        self.dark_mode_enabled = not self.dark_mode_enabled

    def apply_dark_mode(self):
        dark_theme = """
            QMainWindow { background-color: #121212; color: white; }
            QTabWidget::pane { background: #1e1e1e; }
            QTabBar::tab { background: #333; color: white; padding: 10px; }
            QTabBar::tab:selected { background: #444; }
            QLineEdit { background: #333; color: white; border: 1px solid gray; }
            QPushButton { background: #444; color: white; padding: 5px; }
            QPushButton:hover { background: #555; }
        """
        self.setStyleSheet(dark_theme)

    def apply_light_mode(self):
        light_theme = """
            QMainWindow { background-color: white; color: black; }
            QTabWidget::pane { background: #ddd; }
            QTabBar::tab { background: #eee; color: black; padding: 10px; }
            QTabBar::tab:selected { background: #ccc; }
            QLineEdit { background: white; color: black; border: 1px solid gray; }
            QPushButton { background: #ddd; color: black; padding: 5px; }
            QPushButton:hover { background: #bbb; }
        """
        self.setStyleSheet(light_theme)

app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())

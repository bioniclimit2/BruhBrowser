import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *

# --- THE NEW TAB PAGE (PYTHON-GENERATED HTML) ---
def get_new_tab_html():
    return """
    <html>
        <head>
            <style>
                body {
                    background: radial-gradient(circle, #1e1e1e 0%, #121212 100%);
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                h1 { font-size: 48px; margin-bottom: 10px; letter-spacing: -1px; }
                .search-box {
                    width: 500px;
                    padding: 15px 25px;
                    border-radius: 30px;
                    border: 1px solid #444;
                    background: #2a2a2a;
                    color: white;
                    font-size: 18px;
                    outline: none;
                    transition: 0.3s;
                }
                .search-box:focus { border-color: #0078d4; box-shadow: 0 0 15px rgba(0,120,212,0.3); }
                .footer { position: absolute; bottom: 20px; color: #555; font-size: 12px; }
            </style>
        </head>
        <body>
            <h1>BruhBrowser</h1>
            <p style="color: #888;">Where do you want to go today?</p>
            <input type="text" class="search-box" placeholder="Search Google..." onkeydown="if (event.key === 'Enter') window.location.href = 'https://www.google.com/search?q=' + this.value">
            <div class="footer">Built with Python & Chromium</div>
        </body>
    </html>
    """

class BruhBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BruhBrowser")
        self.resize(1280, 800)
        
        # UI Container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- NAVBAR ---
        self.navbar = QWidget()
        self.navbar.setFixedHeight(60)
        self.navbar.setObjectName("navbar")
        nav_layout = QHBoxLayout(self.navbar)
        nav_layout.setContentsMargins(15, 0, 15, 0)

        # Navigation Buttons (Using cleaner symbols)
        self.back_btn = self.create_nav_btn("⟵", lambda: self.tabs.currentWidget().back())
        self.forward_btn = self.create_nav_btn("⟶", lambda: self.tabs.currentWidget().forward())
        self.reload_btn = self.create_nav_btn("↻", lambda: self.tabs.currentWidget().reload())
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or Search...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.add_tab_btn = self.create_nav_btn("+", self.add_new_tab)

        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addSpacing(10)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addSpacing(10)
        nav_layout.addWidget(self.add_tab_btn)

        # --- TABS ---
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True) # ENABLE CLOSE BUTTONS
        self.tabs.setMovable(True)     # Allow dragging tabs around
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_ui_on_tab_change)
        
        self.main_layout.addWidget(self.navbar)
        self.main_layout.addWidget(self.tabs)

        self.apply_styles()
        self.add_new_tab() # Start with one tab

    def create_nav_btn(self, text, slot):
        btn = QPushButton(text)
        btn.setFixedSize(38, 38)
        btn.clicked.connect(slot)
        return btn

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QWidget#navbar { background-color: #1e1e1e; border-bottom: 1px solid #333; }
            
            QLineEdit {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 19px;
                padding: 8px 20px;
                font-size: 14px;
            }

            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border-radius: 19px;
                font-size: 20px;
            }
            QPushButton:hover { background-color: #333; }

            QTabBar::tab {
                background-color: #1e1e1e;
                color: #888;
                padding: 12px 25px;
                border-right: 1px solid #2a2a2a;
            }
            QTabBar::tab:selected {
                background-color: #121212;
                color: white;
                border-bottom: 2px solid #0078d4;
            }
            
            /* The 'X' Close Button Styling */
            QTabBar::close-button {
                image: url(close_icon.png); /* Fallback to system default if no image */
                subcontrol-position: right;
                margin-left: 5px;
            }
            QTabBar::close-button:hover {
                background-color: #ff4d4d;
                border-radius: 10px;
            }
        """)

    def add_new_tab(self):
        browser = QWebEngineView()
        
        # Load our Python-generated New Tab HTML
        browser.setHtml(get_new_tab_html())
        
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        # Logic to update URL bar and title
        browser.urlChanged.connect(lambda qurl: self.on_url_changed(qurl, browser))
        browser.titleChanged.connect(lambda title: self.on_title_changed(title, browser))

    def on_url_changed(self, qurl, browser):
        if self.tabs.currentWidget() == browser:
            url_str = qurl.toString()
            # Don't show the messy data:text html in the bar
            if "data:text/html" in url_str:
                self.url_bar.setText("")
            else:
                self.url_bar.setText(url_str)

    def on_title_changed(self, title, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            display_title = (title[:12] + '..') if len(title) > 12 else title
            self.tabs.setTabText(index, display_title or "New Tab")

    def navigate_to_url(self):
        text = self.url_bar.text()
        if "." not in text: # If it's a search term
            url = f"https://www.google.com/search?q={text}"
        elif not text.startswith("http"):
            url = "https://" + text
        else:
            url = text
        self.tabs.currentWidget().setUrl(QUrl(url))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            # If it's the last tab, just reset it to the new tab page
            self.tabs.currentWidget().setHtml(get_new_tab_html())

    def update_ui_on_tab_change(self, i):
        if i != -1:
            browser = self.tabs.widget(i)
            url = browser.url().toString()
            self.url_bar.setText("" if "data:text/html" in url else url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("BruhBrowser")
    window = BruhBrowser()
    window.show()
    sys.exit(app.exec())
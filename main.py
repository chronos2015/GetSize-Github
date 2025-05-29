
import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class GitHubSizeChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GetGithubSize")
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("GitHubユーザー名:")
        self.layout.addWidget(self.label)
        
        self.user_input = QLineEdit(self)
        self.layout.addWidget(self.user_input)

        self.repo_label = QLabel("リポジトリ名:")
        self.layout.addWidget(self.repo_label)
        
        self.repo_input = QLineEdit(self)
        self.layout.addWidget(self.repo_input)

        self.button = QPushButton("サイズを取得")
        self.button.clicked.connect(self.get_repo_size)
        self.layout.addWidget(self.button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def format_size(self, size_kb):
        if isinstance(size_kb, int):
            if size_kb < 1024:  # 1MB未満ならKB単位
                return f"{size_kb} KB"
            elif size_kb < 1024 * 1024:  # 1GB未満ならMB単位
                return f"{size_kb / 1024:.2f} MB"
            else:  # それ以上はGB単位
                return f"{size_kb / (1024 * 1024):.2f} GB"
        else:
            return "不明"

    def get_repo_size(self):
        user = self.user_input.text().strip()
        repo = self.repo_input.text().strip()

        if not user or not repo:
            self.result_label.setText("ユーザー名とリポジトリ名を入力してください")
            return

        url = f"https://api.github.com/repos/{user}/{repo}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            size_kb = data.get("size", "不明")
            self.result_label.setText(f"リポジトリサイズ: {self.format_size(size_kb)}")
        else:
            self.result_label.setText("リポジトリ情報を取得できませんでした")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitHubSizeChecker()
    window.show()
    sys.exit(app.exec())
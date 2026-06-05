# main.py
# Entry point for the CPU Scheduling Simulator.
# Launches the main application window.

from ui.main_window import MainWindow


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
for /r "gui"  %%d in (*.*) do python -m PyQt5.uic.pyuic gui\%%~nd.ui -o views\%%~nd.py

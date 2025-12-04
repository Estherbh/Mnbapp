@echo off
REM Script de test local pour Virunga Dashboard
REM Usage: double-cliquer ou executer dans cmd

echo ============================================================
echo TEST LOCAL - VIRUNGA DASHBOARD
echo ============================================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo Installez Python depuis : https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Verifier si l'environnement virtuel existe
if not exist ".conda\python.exe" (
    echo [INFO] Environnement virtuel non trouve
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree
)

REM Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call .conda\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo [ATTENTION] Impossible d'activer l'environnement conda
    echo [INFO] Tentative avec venv...
    if exist ".venv\Scripts\activate.bat" (
        call .venv\Scripts\activate.bat
    )
)

echo.

REM Verifier si Streamlit est installe
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Streamlit non installe
    echo [INFO] Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Impossible d'installer les dependances
        pause
        exit /b 1
    )
    echo [OK] Dependances installees
)

echo [OK] Streamlit detecte
echo.

REM Verifier les fichiers requis
echo [INFO] Verification des fichiers...
if not exist "virunga_app.py" (
    echo [ERREUR] virunga_app.py non trouve
    pause
    exit /b 1
)
if not exist "users.json" (
    echo [ATTENTION] users.json non trouve
    echo [INFO] Utilisez generate_hash.py pour creer un utilisateur
    echo.
)

echo [OK] Fichiers principaux presents
echo.

REM Lancer l'application
echo ============================================================
echo LANCEMENT DE L'APPLICATION
echo ============================================================
echo.
echo L'application va s'ouvrir dans votre navigateur...
echo.
echo Pour arreter : Ctrl+C dans cette fenetre
echo.
echo ============================================================
echo.

streamlit run virunga_app.py

pause

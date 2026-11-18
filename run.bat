@echo off
REM Tao env (neu chua co), cai thu vien, roi chay app Streamlit.
set CONDA_DIR=D:\mini_conda
set ENV_NAME=img-sharpener
set PY=%CONDA_DIR%\envs\%ENV_NAME%\python.exe

cd /d "%~dp0"

if not exist "%PY%" (
    echo [1/3] Tao conda env %ENV_NAME% ...
    call "%CONDA_DIR%\Scripts\conda.exe" create -n %ENV_NAME% python=3.11 -y --override-channels -c conda-forge
)

echo [2/3] Cai thu vien ...
"%PY%" -m pip install -r requirements.txt

echo [3/3] Chay app tai http://localhost:8501 ...
start "" cmd /c "timeout /t 6 >nul & start http://localhost:8501"
"%PY%" -m streamlit run app.py --server.headless true

pause

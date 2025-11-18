@echo off
echo Ejecutado por Task Scheduler: %date% %time% >> log_ejecucion.txt
"C:\Users\Usuario\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\Usuario\Desktop\Curso Titularizado Python\retail-sales-dashboard automatic\Src\update_dataset.py"

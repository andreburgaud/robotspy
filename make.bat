@echo off

if {%1} == {} (
    goto USAGE
)

if {%1} == {help} (
    goto USAGE
)

if {%1} == {clean} (
    goto CLEAN
)

if {%1} == {fmt} (black robots) & (goto :EOF)
if {%1} == {attributions} (pip-licenses -d -u -f markdown -o license > ATTRIBUTIONS.md) & (goto :EOF)
if {%1} == {lint} (pylint robots) & (goto :EOF)
if {%1} == {test} (pytest tests -vv) & (goto :EOF)
if {%1} == {tree} (pipdeptree) & (goto :EOF)
if {%1} == {type} (mypy robots) & (goto :EOF)

:CLEAN
rmdir /q /s .cache build dist robotspy.egg-info .pytest_cache robots\__pycache__ tests\__pycache__
del /q *.bak
goto :EOF

:USAGE
echo.
echo Usage:
echo.  make ^<task^>
echo.
echo The tasks are:
echo.
echo attributions       Generate attribution list for software used by robotspy
echo make clean         Delete temp files (*.pyc), caches (__pycache__)
echo make fmt           Format Python files using Black (Assuming Black installed globally)
echo make help          Display this help message
echo make lint          Lint Python file using Pylint (Assuming Pylint installed globally)
echo make test          Execute tests
echo make tree          Display the dependency tree (using pipdeptree)

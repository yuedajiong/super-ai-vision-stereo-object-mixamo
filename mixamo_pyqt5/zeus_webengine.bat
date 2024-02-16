for /L %%i in (1, 1, 1) do (python -Bu zeus_webengine.py %%i)

ping 0 -n 33 > nul


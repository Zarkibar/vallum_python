@echo off
call .\venv\Scripts\activate

color 02

echo This is vallum...
ping 127.0.0.1 -n 2 > nul
echo You can use this program in a minute
ping 127.0.0.1 -n 3 > nul
echo But vallum needs to ask you some questions first
ping 127.0.0.1 -n 4 > nul
echo You ready?
timeout /t 10

set /p server_ip="What's the server ip: "
echo.
set /p username="What's your username: "
echo.
set /p ques1="Do you prefer Dark Mode or Light Mode? "
echo.
set /p ques2="Do you ever talk to yourself? "
echo.
set /p ques3="How do you decide whether to trust someone? "
echo.
set /p ques4="If you were Neo, what pill would you choose and why? "
echo.
set /p ques5="What is your idea of a perfect day? "
echo.
set /p ques6="What is your idea of a perfect life? "
echo.
set /p ques7="Is free will a paradox? "
echo.
echo One last question
ping 127.0.0.1 -n 4 > nul
set /p ques8="Are you gay? "


python client.py "%server_ip%" "%username%" "%ques1%" "%ques2%" "%ques3%" "%ques4%" "%ques5%" "%ques6%" "%ques7%" "%ques8%"
pause

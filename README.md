# Rset
(updates discontinued permentantly, if you want to get past the endless queue, play a different server, trust me.)
## **Never** lose a prized vehicle to a server restart again. 
 This lightweight utility tracks server restart times with high precision,<br>  enabling you to secure your gear before the restart, <br>  and ensuring you are the first one in the queue.
<br><br>**Designed in-time with, and for, the _Escape from Dayz_ by Goon DayZ server.**
## **Preview**
<img width="720" height="186" alt="0 1 002" src="https://github.com/user-attachments/assets/7059c73f-138c-49c4-86f6-0f18b03370bd" /><br>
With the release binaries you can begin utilizing the utility almost immediately. No assembly needed.

## **How to use**
* Simply download the binary from the releases and run it anywhere to start the application. 
* Make sure DayZ is in windowed mode if you want the app to overlay.
* In the settings page ([+] button), you can toggle notification beeps, and the classic mode for the progress bar in the theme of the [alpha](https://imgur.com/a/WwhVPsn) version of the utility.
<br><br><br><br><br>
# **Nerd stuff**
<br><br>
## **Building from source**
Install Python version 3.11<br><br>
Install the requirements with<br>
```py/python -m pip install pyinstaller```<br><br>
Make sure to install requirements to the correct version if you have multiple python versions.<br> > ```py/python -3.11 -m pip install pyinstaller```<br><br>
Alternatively install the requirements from the requirements file.<br>
```py/python -3.11 -m pip install -r requirements.txt```<br><br>
Compile using PyInstaller,<br>
> (Replace "PATH_TO" with the corresponding path, and enter only 'py' or 'python', not 'py/python')<br><br>
> eg. ```py/python -3.11 C:\PATH_TO\Python\Python311\Lib\site-packages\PyInstaller\__main__.py  --noconsole --onefile --collect-all imgui --add-binary "C:\PATH_TO\Python\Python311\Lib\site-packages\glfw\glfw3.dll;." C:\PATH_TO\Rset.py```
<br><br>
## **Release Binary Virus Total + Analysis**
[Detect It Easy](https://github.com/horsicq/Detect-It-Easy)
<img width="1711" height="615" alt="die" src="https://github.com/user-attachments/assets/15205ee8-f6bd-4d95-8c12-69a3879a86a1" />
[Virus total](https://www.virustotal.com/gui/file/ea5d6a38f71d92534a0b1e909797296abf502a2187dbc59e9d1a3be9053dff9a)<br>
<img width="791" height="1239" alt="vt" src="https://github.com/user-attachments/assets/a5ad8293-4578-48e2-b8bd-e38a14d3c8e0" />

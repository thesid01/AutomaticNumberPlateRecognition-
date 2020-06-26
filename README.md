# AutomaticNumberPlateRecognition-

#### How to get Started
* Download pytesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki) and install it.
* make a virtual environment using virtualenv using python3 only (use your location of pyhton3 installation)

````
virtualenv -p 'C:\Users\thesid01\AppData\Local\Programs\Python\Python36-32\python.exe' venv
````
* Start virtualEnvironment
````
.\venv\Scripts\activate
````
* install dependencies
````
pip3 install -r .\requirements.txt
````
Run ````python main.py```` to detect number plates

Uncomment line number 76 in main.py to view images and bounding box.
Number Plate detected text will be printed in console.
Detected plate data will be saved in CSV file.
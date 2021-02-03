# Raw Image Viewer
![demo_1080i](https://github.com/s94285/RawImageViewer/blob/master/screenshots/demo_1080i.png)
![demo_1080p](https://github.com/s94285/RawImageViewer/blob/master/screenshots/demo_1080p.png)
![demo_4K](https://github.com/s94285/RawImageViewer/blob/master/screenshots/demo_4K.png)
## Features
- For reviewing dumped images and delete unwanted images
- View folders and image list on left
- Preview selected raw image on right
- Use folder path to navigate using address bar
- Select one or more images and use delete key to move them into trashcan
- Auto detect resolution by file size
- Currently support 1920x1080/1920x540/3840x2160 8bits gray scaled raw images
## Usage
- requires pyqt5, send2trash, tested on python3.7  
- run from command line: `python3 rawImageViewer.py`
## Windows Executable File
- In Release  
`nuitka --standalone --onefile --show-progress --show-memory --output-dir=dist --windows-company-name=s94285 --windows-file-version=0.1 --plugin-enable=qt-plugins --include-qt-plugins=sensible,styles rawImageViewer.py`
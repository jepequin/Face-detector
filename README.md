# Face detection with OpenCV

This is code for the project of the final course in the Python 3 Programming Specialization, offered by University of Michigan via Coursera (https://www.coursera.org/learn/python-project). The goal of this project is learning how to work with third party libraries, this includes finding the appropriate module for solving the problem at hand, consulting its documentation (online or via the help function), looking for relevant methods, etc.  

## Description

A zip file of images (to be processed) is given. The files inside are newspaper images. Our mission is to write python code which allows one to search through the images looking for the occurrences of faces inside of those containing a given keyword (chosen by the user). For instance, if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper pages which mentions "pizza" (one contact sheet per page). 

We use the three libraries introduced in the course: OpenCV for face detection, Tesseract for optical character recognition, and Pillow to composite images together into contact sheets. We also use the zipfile library for extracting zip files, and os for navigating through folders and creating paths.

Each page of the newspapers is saved as a single PNG image in a file called images.zip. These newspapers are in english, and contain a variety of stories, advertisements and images.

The code proceeds as follows:

-	Together the zipfile and os libraries allow us to extract the newspaper pages from the image.zip file. It is important that (after unzipping) the newspaper pages are contained in a folder inside the directory where our script is located.
-	Using the tesseract library we fetch the text of every page and keep only those containing the keyword. 
-	For each remaining page we perform page segmentation to locate boxes containing text (again with tesseract), which we then proceed to erase (using the rectangle method from opencv). This leaves us with pages containing only images.
-	Using opencv we detect face occurrences inside these pages. We opt for a Haar cascade classifier, and we set the minimal number of neighbors (minNeighbors) to zero. This is important to avoid excessive false-positive detections.
-	Finally, pillow allows us to create a contact sheet of faces appearing inside these pages.

As a footnote we stress that, although it is true that pattern detection (like facial features) can be better accomplished using neural networks, the usage of libraries such as opencv for this purpose can still be justified in some cases. For instance, when limited computing capacity is a constraint. Using the pretrained opencv classifiers allows us to get fast results without the need of setting up and training a network. Also, as mentioned above, the main goal of this project is not to get the most accurate face detector. Instead, it is to get used to dealing with third party libraries.

## Author

Jesua Epequin (100%). Contact me at jesua.epequin@gmail.com    
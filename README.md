## **Distance Matrix**

A simple code to create distance/duration matrices between origin/destination points. It utilizes [Google Maps Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/), which allows its standard users to make 100 elements per request. Therefore I subdivided the matrices into 10 by 10 blocks.

It works on MacOS and Ubuntu with Python3.

## *Example Run*

- You need to have pandas, googlemaps and numpy installed. You can use pip to do so.

`sudo pip3 install pandas googlemaps numpy`

- You should enter destination and origin points into their respective csv files. There are sample files in this repo which you can use for testing.

- Then run `main.py` to create the matrices. The output will be written into `output.txt`.

`python3 main.py`

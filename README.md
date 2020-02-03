# date-extractor
if you need the receipt image data then please refer to this link to access the data: https://drive.google.com/open?id=1HCsoLKtz0FeCvLKmVfQnHrbcSMjrFZak
And unzip it in the project folder. 
Project tree structure should look like:
--images(folder)
--multiple_receipt.py
--requirement.txt
--single_receipt.py


## single_receipt.py
If you want to get the date of a  single receipt image then you can use this single_recepit.py 
steps:

1.Add that receipt image in the images folder.

2.Run the single_recepit.py and it will ask to enter the name of the image 

3.Enter the correct image/filename 

4.Then it will return the date format in YYYY-mm-dd 


## multiple_receipt.py
If you want to get the date of multiple receipt images then you should use  this multiple_reciept.py

So, if you refer to the data which I had mentioned then you will notice the total receipt as 595.
Steps:

1.execute the multiple_receipt.py

2.it might take 10-30 minutes according to your computer speed 

3.after finishing the execution, it will create result.xls file 

4.open the file result.xls and you will notice three columns as filename, image_date, and recp_date

a.**image_date** means whatever date which the model had captured while reading the receipt image, which could be in any formate 

b.**recp_date** is the column for storing the date into YYYY-mm-dd format.

c.I create this two date column as we can compare the actual date and converted date 

5.when you scroll down you will notice the accuracy of the current model.

***Lets say we used the data which i had mentioned **

Total receipt 595

Date found: 391

real accuracy:  82.02%

but the model might mention accuracy as  65.714% = 391/595*100

**Here is the reason why its 82.02%**

as in that data, not all images are clear and some of them don't even have the date and some images are not clear at all (like even human cant easily identify it)

so, if the model correctly identifys date then the count will increase by 1(one) but if it didn't recognize then count won't be increased. 

so what about receipt which doesn't even have a date, so the model won't show any date for those types of images. so we have to count +1 for it as the model did it correctly, saying the receipt doesn't have a date at all. 

About 26 images are not having the date and for 71 images the dates are not visible as well as confusing for a human to identify it.

So, the total count should be == date found + date not mentioned and date not clear : 391 + 26 + 71 = 488

488/595*100 = 82.016..

That's why the actual accuracy is 82.02%


###### **Note:**

multiple_recipt.py is used to find accuracy for multiple images

single_receipt.py is used to find dates in a single image

Images should be in the images folder only.


Use RESTful API for making it work locally on your laptop using a web browser. (working on the process...)

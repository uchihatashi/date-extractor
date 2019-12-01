# date-extractor
Please refer the link to access the images : https://drive.google.com/open?id=1HCsoLKtz0FeCvLKmVfQnHrbcSMjrFZak

Total receipt : 595
Date found : 391
Accuracy : 65.71428571
Here if the receipt is not having any date it is +1 for the count and if the date is present and it is not recognized then it is -1
And also if the date is present and it is recognized then +1 for the count.

About 26 images are not having date and for 71 images the dates are not visible aa well as confusing
So, date found + date not mentioned and date not clear : 391 + 26 + 71 = 488
488/595*100 = 82.016..
That's why the new accuracy is 82.02%


multiple_recipt.py is to find accuracy for multiple images
single_receipt.py is to find dates in single image

Note: images should be present in images folder only.

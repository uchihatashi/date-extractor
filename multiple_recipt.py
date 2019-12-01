#libraries or dependencies 
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance
import cv2
import datefinder
import datetime
import os
import pandas as pd


def get_string(img_path, types = 0):
    try:
        # to read image using opencv
        img = cv2.imread(img_path)

        #to enhance the sharpness when its required 
        if(types == 2): 
            im_pil = Image.fromarray(img)  #converting cv2 to pillow format using arrays
            enhancer_object = ImageEnhance.Sharpness(im_pil)
            out = enhancer_object.enhance(5.0) #shapness increased by 5.0 points
            img = np.asarray(out)  #converting pillow to cv2 format using arrays

        if(types == 3):            
            im_pil = Image.fromarray(img) #converting cv2 to pillow format using arrays
            enhancer_object = ImageEnhance.Sharpness(im_pil)
            out = enhancer_object.enhance(3.0) #shapness increased by 5.0 points
            img = np.asarray(out) #converting pillow to cv2 format using arrays

        # Converting to gray scale 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #to reduce the size of image by 80% height and width
        if(types == 1):
            img = cv2.resize(img, (0,0), fx=0.8, fy=0.8) 

        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        # Using Morphology Transformations 
        line = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel) # cv2.MORPH_CLOSE is useful to remove small holes

        # Recognize text using tesseract ... locating the path of pytesseract
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        result = pytesseract.image_to_string(line)
        return result

    except Exception as e:
        print("error occured in get_string \n{}".format(e))


# this main_function will help us classifying all different types of date formates
def main_function(para):
    try:
        # some flags to help 
        fa_Date,found_date = 0,0
        count_date = para.count("date") # counting date word is the receipt 
        _new_para = para 

        if(count_date == 1): # if date word count is only 1 then it could be the receipt date 
            found_date = 1 
        # if date word count is more then 1 then there could be other dates too but we need to figure out 
        # which is required. ie: "candidate" ist not a date but have date word in it 
        elif(count_date >1): 
            i = 0          
            startpt = _new_para.find("date") # find() will help use getting index of first match 
            while (i < count_date):
                # here we will find the actuat date word only not the mix one like "candidate" 
                if (startpt == 0):
                    found_date = 1
                    break 
                elif (_new_para[startpt-1:startpt].isalpha()):  
                    _new_para = _new_para[startpt+4:]
                    startpt = _new_para.find("date")
                    i += 1
                # this will check _date is alpabet of not, if yes then it shoud not be a date word 
                elif (_new_para[startpt+4:startpt+5].isalpha()): # this will check date_ is alpabet or not 
                    _new_para =  _new_para[startpt+4:]
                    startpt = _new_para.find("date")
                    i += 1                    
                else: # if both side of _date_ word is not a alphabet then its it a date word only  
                    found_date = 1
                    break

        if (found_date ==1): # if found_date is 1 then we should check after that date is a date or not
            if (_new_para.find('date')!= -1): 
                
                """print("\n*********** found date word ************") # you can activate print to check how it works 
                print(_new_para)"""
                startpt = _new_para.find('date') + 4 # as date have 4 character, so i ahevto start index after 4
                
                # i am only taking 26 characters after "date word"
                date_store = _new_para[startpt : startpt+26]  
                new_date = finding_date(date_store) # own defined function 

                if (str(new_date) != "no date"): # if the return of finding date is a date then we have to validate is it a right date or not
                    date_conformation = YMD_validator(new_date) # own defined function 
                    if (date_conformation == 1): # if return of YMD_validator() is 1 then is measns its a correct date 
                        fa_Date = 1
                        return 1, date_store, new_date.strftime('%Y-%m-%d') 
                    """else:
                        print("after date, image is not clear")"""
                        
        if(fa_Date == 0): # if fa_Date is 0 then it means we haven't found date word or after date word is not clear 
            #print("****** didnt found a word *DATE* *********")

            #extracting line by line 
            only_lines = para.split("\n")
            for a_line in only_lines:
                # as date can come in many different format. so it is always seperated by those 6 seperators 
                date_seps = ["’","'",",","-","/","."]
                # as total character in date is YYYY-MM-DD = 10 but some time date could be in MM-DD-YY, so lowest is 8
                if (len(a_line) >= 8): 

                    for date_sep in date_seps:
                        count_date_sep = a_line.count(date_sep)
                        #if count_date_sep in a line is zero then there is no reason in going in the next loop
                        if (count_date_sep != 0):

                            #as some date comes as jun16'19, sep 29,2018 or jun16’19 
                            if (date_sep == "’" or date_sep == "," or date_sep == "'" ):
                                startpt = a_line.find(date_sep) 
                                new_date_conf, date_store = date_taker(a_line, 2, startpt,date_sep) #own defined function
                                
                                if (str(new_date_conf) != "failed"): # if new_date_conf is not failed then it's a correct date 
                                    return 1, date_store, new_date_conf

                            else: 
                                # as other date comes in this format MM-dd-yyyy, MM/dd/YYYY, or MM.dd.YYYY 
                                startpt = a_line.find(date_sep) # gives index of the current seperator  
                                
                                if (count_date_sep == 2):
                                    second_available = 0
                                    """ as date formate is always in dd-mm-yyyy or yyyy-XX-xx 
                                    so after first this "-" second shoud be after 2 index of it"""
                                    
                                    if (len(a_line) >= startpt+5): #to prevent error 
                                        second_available = a_line[ startpt+1 : startpt+6 ].find( date_sep ) # after first this "-" it takes 4 more characte to check the next this "-" 
                                    else:
                                        second_available = a_line[ startpt+1 : len(a_line) ].find( date_sep )
                                    # if second_available is not present then it will return -1
                                    if (second_available != -1):
                                        new_date_conf,date_store = date_taker(a_line, 1, startpt, date_sep) # own defined function
                                        if (str(new_date_conf) != "failed"):  # if new_date_conf is not failed then it's a correct date   
                                            return 1, date_store, new_date_conf

                                elif (count_date_sep >= 3): # sometime there could be more than two seperators, so we have to know which is used for the date and which are not used
                                    date_store, new_date_conf = _3ormore(a_line,date_sep,startpt) # own defined function
                                    if (new_date_conf != "failed"):  # if new_date_conf is not failed then it's a correct date 
                                        return 1, date_store, new_date_conf
                                        
        return 0, "image not clear", "null" # if date is not found then it will return null as no date in the receipt 
    except Exception as e:
        print("error occured in main_function \n{}".format(e))
        return 0, "image not clear", "null"


# sometime there could be more than two seperators, so we have to know which is used for the date and which are not
def _3ormore(a_line,date_sep,startpt):
    try:
        for i, c in enumerate(a_line, start=0):
            if date_sep == c: # if they found date_sep (seperator) then they will go in and check it

                if (len(a_line) >= i+5): # to prevent error 
                    second_available = a_line[ i+1 : i+5 ].find(date_sep)
                else:
                    second_available = a_line[ i+1 : len(a_line) ].find(date_sep)

                if (second_available != -1):

                    new_date_conf, date_store = date_taker(a_line, 1, i, date_sep) # own defined function
                    if (str (new_date_conf) != "failed"):
                        return date_store, new_date_conf

        return "null", "failed"
    except Exception as e:
        print("error occured in _3ormore \n{}".format(e))
        return "null", "failed"


# this function is used to take the uncleard text and extract some text, which is usually the "date" and if no specific date is found then it will retun "failed" 
def date_taker(unclean_txt, type, startpt,date_sep): 
    try:
        if (type == 1):
            #type 1 is for dates which have format of MM-DD-YYYY or YYYY-DD-MM or DD-jun-YYYY in "-", "/", or "." or even YYYY-DD-MM too
            #so max character after first this '-' is "- DD- YYYY" (8+1+1+1) = 11 as some time space use to come
            
            if (startpt == 1):
                date_store = unclean_txt[startpt-1 : startpt+10]
            else:
                date_store = unclean_txt[startpt-2 : startpt+10]

            new_date = finding_date( date_store ) # own defined function
            if (str(new_date) != "no date"): # if new_date is not the "no date" then it will go for the YMD_validator() to valid the date 
                date_conformation = YMD_validator( new_date ) # own defined function
                if (date_conformation == 1): # if YMD_validator() retruns 1 then it means this is the receipt date 
                    return new_date.strftime('%Y-%m-%d'), date_store

            # some time failure comes because of space between the date or after date some digits use to come. so i need to remove unwanted digits
            if(date_store.count(" ")==2): # if the space count is only 2 then the ending space might be the problem 
                f_space = date_store.rfind(" ") # rfind finds the word from the reversed 
                new_date_str = date_store[:f_space]

                new_date = finding_date(new_date_str) # own defined function
                if (str(new_date) != "no date"):
                    date_conformation = YMD_validator(new_date) # own defined function
                    if (date_conformation == 1):
                        return new_date.strftime('%Y-%m-%d'), date_store

            elif(date_store.count(" ")==1):
                f_space = date_store.find(" ")
                
                if (date_store[f_space-1 : f_space+1].find(date_sep) != -1):  # checks the date_sep i there or not between the space if yes then itis a normal date 
                    new_date_str = date_store[:f_space] + date_store[f_space+1:len(date_store)]
                    new_date = finding_date(new_date_str) # own defined function
                    if (str(new_date) != "no date"):
                        date_conformation = YMD_validator(new_date) # own defined function
                        if (date_conformation == 1):
                            return new_date.strftime('%Y-%m-%d'), date_store
                elif ( f_space > 7 ): # as most of the next space might come at ending part ie: dd-mm-YY 1000 so 7 is the best choice 
                    new_date_str = date_store[:f_space]
                    new_date = finding_date(new_date_str) # own defined function
                    if (str(new_date) != "no date"):
                        date_conformation = YMD_validator(new_date) # own defined function
                        if (date_conformation == 1):
                            return new_date.strftime('%Y-%m-%d'), date_store

            else:
                #as i mention one date format which is yyyy-dd-mm so (startpt-2) wont work on this. So, we have to use this one 
                date_store = unclean_txt[startpt-5 : startpt+7]
                new_date = finding_date(date_store) # own defined function
                if (str(new_date) != "no date"):
                    date_conformation = YMD_validator(new_date) # own defined function
                    if (date_conformation == 1):
                        return new_date.strftime('%Y-%m-%d'), date_store
        
        else: #type == 2
            # as second case is for jun16'19 or sep 29,2018. so, at that index ", or '" 
            # subtract 7 at start and at end add 5 
            if(startpt < 7): #to prevent error
                date_store = unclean_txt[:startpt+6]
            else:
                date_store = unclean_txt[startpt-7 : startpt+6]

            new_date = finding_date(date_store) # own defined function
            if (str(new_date) != "no date"):
                date_conformation = YMD_validator(new_date) # own defined function
                if (date_conformation == 1):
                    return new_date.strftime('%Y-%m-%d'), date_store

            #for other case like this "september 29, 2019"
            date_store = unclean_txt[startpt-13 : startpt+6]

            new_date = finding_date(date_store) # own defined function
            if (str(new_date) != "no date"):
                date_conformation = YMD_validator(new_date) # own defined function
                if (date_conformation == 1):
                    return new_date.strftime('%Y-%m-%d'), date_store

        return "failed", unclean_txt

    except Exception as e:
        print("error occured in date_taker \n{}".format(e))
        return "failed", "unclean_txt"

# finding_date() will help finding date from unclear date from date_taker() and give the proper date in YYYY-MM-DD or no date if not found
def finding_date(date_store):
    try:
        # datefinder is a library with helps to finding date in a raw text but it have lots of limitation if other digits comes in a raw text
        # so date_taker() helps removing the other digits from the raw text
        matches = datefinder.find_dates(date_store)
        for match in matches:
            return(match)        
        return "no date"
    
    except Exception as e:
        print("error occured in finding_date \n{}".format(e))
        return "no date"

# on of the limitation of datefinder is: if we give just a number like 1-31 it will conside it as day and it will give result of that day 
# with current month and year. or some time giving 22-22 it give 2022-11-22 which is alos wrong 
# So to prevent it I used YMD_validator()
def YMD_validator(new_date):
    try:
        now = datetime.datetime.now()
        datee = datetime.datetime.strptime(str (new_date), "%Y-%m-%d %H:%M:%S")

        # as there is no chance of having bill year which is higher than 2019 and lower than 1998
        if (datee.year <= now.year and datee.year > (now.year - 20)):
            # as we dont have any bill which has same month and year of now (2019/11)
            if(datee.year == now.year and  datee.month == now.month):
                return 0 # wrong date
            else:
                return 1 # right date and terminate"
           
        return 0    
    except Exception as e:
        print("error occured in YMD_validator \n{}".format(e))
        return 0


n, date_found = 0, 0 # n is the total count of receipts 
store_res = pd.DataFrame(columns = ['filename','image_date','recp_date']) # store_re is a dataframe which we will use to store each 'filename','image_date','recp_date'
# store_result() helps to store all the result of found date and also not found dates
def store_result(filename,img_date,recp_date):
    try:
        global n, date_found
        if recp_date != "null": # if the receipt date is found then it will store and date_found will be incrememt by 1, so we can find the accuracy
            store_res.loc[n] = [filename] + [img_date] + [recp_date]
            date_found += 1 
        else:
            store_res.loc[n] = [filename] + [img_date] + [recp_date]
        n += 1 

    except Exception as e:
        print("error occured in date_result \n{}".format(e))


# here our main founction starts 
try:
    print(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))
    # to make a base path 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "images")

    #walking intp the base path
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("jpeg") or file.endswith("jpg"):
                paths = os.path.join(root, file)

                print("\n\n+++++++++++  no: {} new image {} \n".format(n, file))    
                para = get_string(paths).lower() # get_string() we are extractiion string from the receipt and they type is 0 which is default 
                #print(para)                
                checkme, date_store, new_date_conf = main_function(para) 

                if(checkme == 0):
                    para = get_string(paths, types=1).lower() # get_string() type is 1 means to reduce the size of image by 80% height and width
                    """print("--------------------------getting new string from type 1")
                    print(para)"""
                    checkme, date_store, new_date_conf = main_function(para)

                    if checkme == 0:
                        para = get_string(paths, types=2).lower() # get_string() type is 2 means to enhance the sharpness by 5.0 points
                        """print("----------------------------------------getting enhance string with type 2")
                        print(para)"""                        
                        checkme, date_store, new_date_conf = main_function(para)

                        if checkme == 0:
                            para = get_string(paths, types=3).lower() # get_string() type is 3 means to enhance the sharpness by 3.0 points
                            """print("----------------------------------------getting enhance string with type 3")
                            print(para) """                           
                            checkme, date_store, new_date_conf = main_function(para)
                            
                            if checkme == 0:
                                print("\n***********date not found***************")
                                store_result(file, date_store, new_date_conf) # 0, "image not clear", "null"

                if(checkme == 1): # if check me is 1 then we had found date 
                    print("\n***********date found***************")
                    print("\ndate on receipt = {} \nconverted date = {}".format(date_store, new_date_conf))
                    store_result(file, date_store, new_date_conf)

    print(store_res) # printing the dataframe which have the data
    print("Total receipt: {}  Date found: {} ".format(n,date_found))
    accuracy = date_found / n * 100 # finding the accuracy
    print("accuracy of the model is :{}".format(accuracy))
    store_res.loc[n] = ["Total receipt"] + ["Date found"] + ["accuracy"] # adding the final result to th store_res 
    store_res.loc[n+1] = [n] + [date_found] + [accuracy]    
    store_res.to_excel('result.xls') # converting dataframe to xls format
    
    print(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")) #printing the end time  

except Exception as e:
    print("error occured in main function \n{}".format(e))


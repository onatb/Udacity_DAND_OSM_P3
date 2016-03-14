#This code standardizes phone numbers

def update_phone(phone):
    #This function gets the non-standart phone number and returns the standardized version
    phone=phone.replace("-"," ").replace("(","").replace(")","")
    if phone[:2]=="00":
        phone=phone[0:2].replace("00","+")+phone[2:]
    elif phone[0]=="0":
        if phone[1]==" ":
            phone=phone[0].replace("0","+90")+phone[1:]
        else:
            phone=phone[0].replace("0","+90 ")+phone[1:]
    if phone.find(" ")==-1:
        phone=phone[:3]+" "+phone[3:6]+" "+phone[6:9]+" "+phone[9:11]+" "+phone[11:]
    if phone[4]=="0":
        phone=phone[:4]+phone[5:]
    if phone[11]!=" ":
        phone=phone[:11]+" "+phone[11:]
    if phone[14]!=" ":
        phone=phone[:14]+" "+phone[14:]
    return phone

for _, element in ET.iterparse(OSMFILE):
    if element.tag=="way":
        for tag in element.iter("tag"):
            if tag.attrib['k']=="phone":
                print update_phone(tag.attrib['v'])

from locale import currency
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ebaysdk import response
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from ebaysdk.policies import Connection as Policies
from django.db import connection
import json

@api_view(['GET', 'POST'])
def getPolicy(request):
  
    if request.method == 'POST':
        token1 = request.POST.get('user_token')
        # token1 = 'AgAAAA**AQAAAA**aAAAAA**KlviYQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6MHlYapDpOEqAydj6x9nY+seQ**d8oGAA**AAMAAA**zSMLmj+enSYAP9QMNZTqiPqso2+OtzbE7iPpz1p82DWfR0Og+7kXbyiEoGG6x0RkMYQcZ9ZXPkqfDHnRCVu4zKQry7gFq2ean5Kxu4g8B6Hj76Eu3Li6mTu/d1+jJwbGSl8IVjE2Ieo7MZRDUQwjnuYOSElFw5gTfLSY5Wa1ZdEGnaqltPY0yGtvtUYmkVvNCCy/5vdA/wqce0ixfiM4QnCj3vdWQzFasm33RhNiaisTxz9Cr6KkkD8IM2fR4JhUHhB/c2xS9hhxDMA6E4lnsxh82LMKh+O8xro3A+++j9iJUna6mCnc82DuhQGLM5sTCSaZeJlhr+RgjWKekbFz0pqXLq4Se/Y2GcR040ipKCbMy72vyfeQzMcfY0gsXGXOsBrHt9wHpAhWNU1wZnZjjyb8ycDn//ggxK5QkfmrOiJb3yHLXS/Fhrh1ZZ9bIrjR4i8s0h+DMegLFU7VOsXjVnkATJdb0R2qP7Uakm1Tg0Wb9Lk+pTLev5fgdyrIrkoFLVF35E+TfL8Ye1RQBArDYV9iDd3Ct4c35h97wqOYmGwG8Kv23NpGFwFSHiqmbY5uWnK9YI44ny6vECQPabrynYC5T5f4KyEb6GJHbKi0IC2uhTthSVmbGEnrbQ1lHGo2u65ZirBfZZJpc/88VD4EZ7vd/8ke8ypzwKGIwMpf4+NrjC8Pt1y4b/Gshkm+cE8TpDJnEP8jCLPWdvS2XHhGTS92ius3ebA/BfVyXAqIPveJeyWaV/7CZefs7cq/kZwX'
        api = Policies(domain='svcs.ebay.com',appid='arsensah-myapp-PRD-41d9f5f51-f3aac787',
        certid='PRD-1d9f5f511ac9-005d-4560-8eee-672f',devid='96d594f7-cbdf-434d-b1ed-42d5b1a26adc',
        token=token1, config_file=None)
        res = api.execute('getSellerProfiles')
        result = res.dict()
        paymentProfiles = result['paymentProfileList']['PaymentProfile']
        returnProfiles = result['returnPolicyProfileList']['ReturnPolicyProfile']
        shippingProfiles = result['shippingPolicyProfile']['ShippingPolicyProfile']
        print("payment=>",paymentProfiles)
        print("payment=>",returnProfiles)
        print("payment=>",shippingProfiles)
        paymentlist = []
        returnlist = []
        shippinglist = []
        businessPolicyObject = {}
        with connection.cursor() as cursor:
            cursor.execute("select * from description")
            row = cursor.fetchall()
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
        
        descriptionlist=[]
        for result in row:
           descriptionlist.append(dict(zip(row_headers,result)))
        try:
            for payment in paymentProfiles:

                businessPolicyObject = {'policyName':payment['profileName'],'policyID':payment['profileId']}
                paymentlist.append(businessPolicyObject)
        except:
                businessPolicyObject = {'policyName':payment['profileName'],'policyID':payment['profileId']}
                paymentlist.append(businessPolicyObject)
                pass           
        try:    
            for returnPolicy in returnProfiles:

                businessPolicyObject = {'policyName':returnPolicy['profileName'],'policyID':returnPolicy['profileId']}
                returnlist.append(businessPolicyObject)
        except:
                businessPolicyObject = {'policyName':returnProfiles['profileName'],'policyID':returnProfiles['profileId']}
                returnlist.append(businessPolicyObject)
                pass
        try:
            for shipping in shippingProfiles:
            
                businessPolicyObject = {'policyName':shipping['profileName'],'policyID':shipping['profileId']}
                shippinglist.append(businessPolicyObject)
        except:
                businessPolicyObject = {'policyName':shipping['profileName'],'policyID':shipping['profileId']}
                shippinglist.append(businessPolicyObject)
                pass
        # data = request.POST.get('user_id')
        data = {'paymentlist':paymentlist,'returnlist':returnlist,'shippinglist':shippinglist,'description':descriptionlist}
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def getProduct (request):
    with connection.cursor() as cursor:
        cursor.execute("select * from product_information where flag='0'")
        row = cursor.fetchall()
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
    
        productlist=[]
        for result in row:
           productlist.append(dict(zip(row_headers,result)))
        
    
    return Response(productlist,status=status.HTTP_201_CREATED)  

@api_view(['POST'])
def removeProduct(request):
    store_token = request.POST.get('store_token')
    item_id = request.POST.get('item_id')
    try:    
        api = Trading(domain='api.ebay.com',appid='arsensah-myapp-PRD-41d9f5f51-f3aac787',
        certid='PRD-1d9f5f511ac9-005d-4560-8eee-672f',devid='96d594f7-cbdf-434d-b1ed-42d5b1a26adc',
        token=store_token, config_file=None,siteid=0)
        request={
                        "ItemID":"{}".format(item_id),
                        "EndingReason":"NotAvailable"
                    }
        response=api.execute("EndFixedPriceItem",request)
        print(response.dict())
        print(response.reply)
        with connection.cursor() as cursor:
            cursor.execute("update product_information set flag='3' where itemID=%s",[item_id])
    except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
    
    response = {"result":"true"}

    return Response(response,status.HTTP_200_OK)


@api_view(['POST'])
def listProduct(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from business_policy")
        row = cursor.fetchall()
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
    
        businessPolicy=[]
        for result in row:
           businessPolicy.append(dict(zip(row_headers,result)))
    
    token1 = businessPolicy[0]['user_token']
    
    ebay_categoryID = request.POST.get('ebay_category')
    currency_rating = businessPolicy[0]['currency_rating']
    price_time = businessPolicy[0]['price_time']
    description = businessPolicy[0]['description']
    product_state = businessPolicy[0]['product_state']

    asin = request.POST.get('asin')
    with connection.cursor() as cursor:
        cursor.execute("select image_url from product_image where asin=%s",[asin])
        row = cursor.fetchall()
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
    
        product_image_list=[]
        image_url_array = []
        for result in row:
           product_image_list.append(dict(zip(row_headers,result)))
        for product_image in product_image_list:
           image_url_array.append(product_image['image_url'])

    print(image_url_array)       
    api = Trading(domain='api.ebay.com',appid='arsensah-myapp-PRD-41d9f5f51-f3aac787',
        certid='PRD-1d9f5f511ac9-005d-4560-8eee-672f',devid='96d594f7-cbdf-434d-b1ed-42d5b1a26adc',
        token=token1, config_file=None,siteid=0)
    request1 = {
            "CategorySpecific":{
                "CategoryID":"{}".format(ebay_categoryID)
            }

        }
    try:         
        response1=api.execute("GetCategorySpecifics", request1)
        # print(response.dict())
    except:
    
        pass
    result = response1.dict()
  
    requiredItem = {}
    requiredList = []
    for item in result['Recommendations']['NameRecommendation']:
        if item['ValidationRules']['UsageConstraint'] == 'Required':
            
            if(len(item['ValueRecommendation'])==2):
                requiredItem = {"name":item['Name'],"value":item['ValueRecommendation']['Value']}
                requiredList.append(requiredItem)
            else:
                requiredItem = {"name":item['Name'],"value":item['ValueRecommendation'][0]['Value']}
                requiredList.append(requiredItem)
            
    print("requiredlist",requiredList)
    print("price",request.POST.get('price'),"currency_rating",currency_rating)
    item_price = int(request.POST.get('price'))/int(currency_rating)
    item_price = item_price * float(price_time)
    item_title = request.POST.get('title')
    item_title = (item_title[:70] +'...') if len(item_title) > 70 else item_title
    print("item title=>",item_title)
    # list new product
    try:    
                    api = Trading(domain='api.ebay.com',appid='arsensah-myapp-PRD-41d9f5f51-f3aac787',
                    certid='PRD-1d9f5f511ac9-005d-4560-8eee-672f',devid='96d594f7-cbdf-434d-b1ed-42d5b1a26adc',
                    token=token1, config_file=None,siteid=0)
                    request1 = {
                        "Item":{
                                        "Title":"{}".format(item_title),
                                         "BestOfferDetails":{
                                            "BestOfferEnabled":"true"
                                        },
                                        "Description":"{}".format(description),
                                        "ListingDuration":"GTC",
                                        "ListingType":"FixedPriceItem",
                                        "Location":"Beverly Hills",
                                        "StartPrice":"{}".format(item_price),
                                        "Country":"JP",
                                        "Currency":"USD",
                                        "Quantity":"{}".format(request.POST.get('quantity')),
                                        "ConditionID":"{}".format(product_state),
                                        "ProductListingDetails":{
                                            "ItemSpecifics":{
                                               "Brand":"CONTINENTAL",
                                               "IncludeeBayProductDetails":"true",
                                               "Mount":"Canon EF",
                                               "Type":"standard"
                                            }
                                                     
                                        },
                                        "ItemSpecifics":{
                                            "NameValueList":{}
                                        },
                                        "PaymentMethods":"PayPal",
                                        "PayPalEmailAddress":"kevinzoo.lancer@gmail.com",
                                        "DispatchTimeMax":"1",
                                        "ShipToLocations":"None",
                                        "ReturnPolicy":{
                                            "ReturnsAcceptedOption":"ReturnsNotAccepted"
                                        },
                                        "PrimaryCategory":{
                                            "CategoryID":"{}".format(request.POST.get('ebay_category'))
                                        },
                                        "PictureDetails":{
                                            "PictureURL":image_url_array,
                                        },
                                        "ItemCompatibilityList":{
                                                "Compatibility":{
                                                    "NameValueList":[
                                                        {"Name":"Year","Value":"2010"},
                                                        {"Name":"Make","Value":"Hummer"},
                                                        {"Name":"Model","Value":"H3"}
                                                    ],
                                                    "CompatibilityNotes":"An example compatibility"
                                                }
                                        },
                                      
                                        "SellerProfiles":{

                                                "SellerPaymentProfile":{
                                                   
                                                        "PaymentProfileName":"{}".format(businessPolicy[0]['payment_name']),  
                                                        "PaymentProfileID":"{}".format(businessPolicy[0]['payment_id'])
                                                        },
                                                        "SellerReturnProfile":{
                                                  
                                                        "ReturnProfileName":"{}".format(businessPolicy[0]['return_name']),  
                                                        "ReturnProfileID":"{}".format(businessPolicy[0]['return_id'])
                                                        },
                                                        "SellerShippingProfile":{
                                                      
                                                        "ShippingProfileName": "{}".format(businessPolicy[0]['shipping_name']),
                                                        "ShippingProfileID":"{}".format(businessPolicy[0]['shipping_id']) 
                                                        },
                                        } ,
        
    
                                        
                                        "Site":"US"

                                }
                                        
                
                    }

                    i=0
                    request1['Item']['ItemSpecifics']['NameValueList']={}
                    itemList=[]
                    for item in requiredList:
                        itemList.append({"Name":item['name'],"Value":item['value']})
                        i=i+1
                    print(itemList)    
                    request1['Item']['ItemSpecifics']['NameValueList']=itemList    
                    response=api.execute("AddItem", request1)
                    response = response.dict()
                    itemID = response['ItemID']
                    if(response['Ack']!='Error'):
                        with connection.cursor() as cursor:
                            cursor.execute("update product_information set flag='1' where asin=%s",[asin])
                            cursor.execute("update product_information set itemID=%s where asin=%s",[itemID,asin])
                    else:
                        with connection.cursor() as cursor:
                             cursor.execute("update product_information set flag='2' where asin=%s",[asin])
                    # print(response.reply)
    except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
    response = {"result":"true"}

    return Response(response,status.HTTP_200_OK)

@api_view(['POST'])
def getOrders(request):
    
    token1 = request.POST.get('user_token')
    transaction_array = []
    val = {}
    try:
        # api = Trading(debug=opts.debug, config_file=opts.yaml, appid=opts.appid, domain=opts.domain,
        #               certid=opts.certid, devid=opts.devid, warnings=True, timeout=20)
        api = Trading(domain='api.ebay.com',appid='arsensah-myapp-PRD-41d9f5f51-f3aac787',
        certid='PRD-1d9f5f511ac9-005d-4560-8eee-672f',devid='96d594f7-cbdf-434d-b1ed-42d5b1a26adc',
        token=token1, config_file=None,siteid=0)             

        response = api.execute('GetOrders', {'NumberOfDays': 1})
        response = response.dict()
        order_array = response['OrderArray']['Order']
        for order in order_array:
            transactions = order['TransactionArray']['Transaction']
            if hasattr(transactions, "__len__"):
               buyer_email = transactions[0]['Buyer']['Email']
            else:
               buyer_email = transactions['Buyer']['Email']
            # else:
            #   
            order_id = order['OrderID']
            item = {'order_id':order_id,'buyer_email':buyer_email}
            transaction_array.append(item)
        print(transaction_array)    
        return Response(transaction_array,status.HTTP_200_OK)    
               

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        pass
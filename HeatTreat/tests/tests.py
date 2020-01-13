# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:08:23 2019

@author: stefflc

First Unit Test for save method
10-16-19 - Initial release of the tests.py - mainly tests $http.post requests from $scope.createTTPI in HeatTreat.JS
10-17-19 - add test_post_update which now attempts to check update requests $http.put from $scope.update in HeatTreat.JS


"""

from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest

from ..models import HeatTreat #Relative import up two levels
from ..views import operator_TTPI_view
# from HeatTreat import HeatTreat
import pyodbc


"""
in dir with manage.py run:
    python manage.py test HeatTreat
    """
class TestHeatTreat_save(TestCase):


    #Runs before EACH test
    '''Basically replicate the JSON that HeatTreat.js would send over for a save() method call 
     see $scope.createTTPI = function(...)
     which then calls 
     $scope.postTreats(TTPIname)

     http://127.0.0.1:8000/HeatTreat/AddTTPI/


     '''


    #### This will will create its own self-contained SQLite database for testing
    #### However this calls the live Visual database so data wanders, not the best test

    ##Setup creates an object before EACH test
    def setUp(self):
        # pass
        self.HT = HeatTreat()

        self.HT.locked = False
        # self.HT.operator = "DANIEL-MORENO"
        self.HT.workOrder = "TEST-BOLT/113"
        self.HT.genBy = "DANIEL-MORENO" #genBy : operator.operatorName
        self.HT.genDate = "2019-10-14"
        self.HT.specNumber = "AS7471"
        self.HT.specRevision = "H"
        self.HT.specMaterial = "Waspaloy"
        self.HT.specMaterialSpec = "AMS5708"
        self.HT.specMaterialSpecRevision = "M"
        # self.HT.tempSetPoint =
        self.HT.genDate = "2019-10-14" #Today
        self.HT.partNumber = "99"
        self.HT.customer = "99"
        self.HT.rev = ""
        self.HT.PO =  "INTERNAL" #99 unless user defined (Optional field), INTERNAL for "TEST%" like work order #s
        self.HT.heatNumber = "99"
        self.HT.WOop = "99" #99 unless user defined (Optional field).
        self.HT.numLoads = 1
        self.HT.loadNumber = 1
        # self.HT.save()


    def tearDown(self):
        pass


    def test_Update_viaSave(self):
        pass

    def test_createTTPI_viaSave(self):

        self.HT.save()


        record = HeatTreat.objects.get(pk=self.HT.id) #This should get the most recent one
        self.assertFalse(record.locked)
        self.assertEqual("TEST-BOLT/113", record.workOrder)
        self.assertEqual("JR618/1", record.heatNumber)
        self.assertEqual(90, record.WOop) #80, 90, 210 are matches depending on Visual status
        self.assertEqual(1, record.numLoads)
        self.assertEqual(1, record.loadNumber)
        self.assertEqual("MSA140818-1-07W018", record.partNumber)
        self.assertIsNotNone(self.HT.rev)
        self.assertEqual("NC", record.rev)

    def test_createTTPI_wHT_viaSave(self):

        self.HT.heatNumber = "ABCDEFG"


        self.HT.save()
        record = HeatTreat.objects.get(pk=self.HT.id) #This should get the most recent one


        self.assertFalse(record.locked)
        self.assertEqual("TEST-BOLT/113", record.workOrder)
        self.assertEqual("ABCDEFG", record.heatNumber)
        self.assertEqual(90, record.WOop) #80, 90, 210 are matches depending on Visual status
        self.assertEqual(1, record.numLoads)
        self.assertEqual(1, record.loadNumber)
        self.assertEqual("MSA140818-1-07W018", record.partNumber)
        self.assertIsNotNone(self.HT.rev)
        self.assertEqual("NC", record.rev)
        record.delete()

    def test_createTTPI_wOP_viaSave(self):

        self.HT.WOop = "120"


        self.HT.save()
        record = HeatTreat.objects.get(pk=self.HT.id) #This should get the most recent one


        self.assertFalse(record.locked)
        self.assertEqual("TEST-BOLT/113", record.workOrder)
        self.assertEqual("JR618/1", record.heatNumber)
        self.assertEqual(120, record.WOop) #80, 90, 210 are matches depending on Visual status
        self.assertEqual(1, record.numLoads)
        self.assertEqual(1, record.loadNumber)
        self.assertEqual("MSA140818-1-07W018", record.partNumber)
        self.assertIsNotNone(self.HT.rev)
        self.assertEqual("NC", record.rev)

    def test_createTTPI_wOP_wHT_viaSave(self):


        #make changes
        self.HT.heatNumber = "ABCDEFG"
        self.HT.WOop = "120" #99 unless user defined (Optional field).

        #apply changes and instantiate original self.HT from setup()
        self.HT.save()
        #get those changes
        record = HeatTreat.objects.get(pk=self.HT.id) #This should get the most recent one

        #compare
        self.assertFalse(record.locked)
        self.assertEqual("TEST-BOLT/113", record.workOrder)
        self.assertEqual("ABCDEFG", record.heatNumber)
        self.assertEqual(120, record.WOop) #80, 90, 210 are matches depending on Visual status
        self.assertEqual(1, record.numLoads)
        self.assertEqual(1, record.loadNumber)
        self.assertEqual("MSA140818-1-07W018", record.partNumber)
        self.assertIsNotNone(self.HT.rev)
        self.assertEqual("NC", record.rev)

    def test_findRevision(self):

        self.HT.save()
        self.HT.cursor = self.getCursor()
        self.HT.base = "TEST-BOLT"
        self.HT.lot = "113"
        self.HT.split = "0"
        self.HT.findRevision(self.HT.cursor)
        self.assertEqual("NC", self.HT.rev)

    def test_findRevisionFail(self):
        self.HT.save()
        self.HT.cursor = self.getCursor()
        self.HT.base = "testbolt"
        self.HT.lot = "113"
        self.HT.split = "0"
        #use context manager to test error
        with self.assertRaises(NameError):
            self.HT.findRevision(self.HT.cursor)
        # self.assertRaises(NameError)

    # def test_genByFail(self):
    #     self.fakeSetup()
    #     self.HT.genBy = ""
    #     self.HT.save()

    #     record = HeatTreat.objects.get(pk=self.HT.id) #This should get the most recent one

    def test_checkForDuplicates(self):

        #TEST-BOLT/113 exists due to save
        self.HT.save()

        #Running checkForDuplicates will find the 1 existing TEST-BOLT
        ## and will flag as not being able to proceed with a 2nd
        with self.assertRaises(NameError):
            self.HT.checkForDuplicates()

    '''
    Heat Number passed in should be 99 - lookup will be performed
    Or pass in manager provided value, and just keep that value
    '''
    def test_findHeatNumber(self):
        self.HT.save()

        self.HT.findHeatNumber(self.getCursor())
        self.assertEqual("JR618/1", self.HT.heatNumber)
        self.assertNotEqual("FROG", self.HT.heatNumber)

    def test_findHeatNumber2(self):
        self.HT.heatNumber = "FROG"
        self.HT.findHeatNumber(self.getCursor())
        self.assertEqual("FROG", self.HT.heatNumber)

        self.HT.heatNumber = ""
        with self.assertRaises(NameError):
            self.HT.findHeatNumber(self.getCursor())

    def test_findOperationNumber(self):
        self.HT.save()
        self.HT.findOperationNumber(self.getCursor())
        self.assertEqual(90, self.HT.WOop)

        self.HT.WOop = 888
        self.HT.findOperationNumber(self.getCursor())
        self.assertEqual(888, self.HT.WOop)

        self.HT.WOop = ""
        with self.assertRaises(NameError):
            self.HT.findOperationNumber(self.getCursor())

        self.HT.WOop = None
        with self.assertRaises(NameError):
            self.HT.findOperationNumber(self.getCursor())

    def getCursor(self):
        server = 'MSAVMFG1'
        database = 'VMLIVE'

        try:
            username = 'stefflc'
            password = 'buttpain1'
            cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = cnxn.cursor()
            return cursor
        except:
            print("server connection error")


class TestHeatTreat_otherMethods(TestCase):

    def test_findBaseLotSplit(self):
        self.HT2 = HeatTreat()

        self.HT2.workOrder = "TEST-BOLT/113"
        self.HT2.findBaseLotSplit()

        self.assertEqual("TEST-BOLT", self.HT2.base)
        self.assertEqual("113", self.HT2.lot)


        self.HT2.workOrder = "12-1234/1.0"
        self.HT2.findBaseLotSplit()
        self.assertEqual("12-1234", self.HT2.base)
        self.assertEqual("1", self.HT2.lot)
        self.assertEqual("0", self.HT2.split)

        self.HT2.workOrder = "DANIEL-MORENO"
        with self.assertRaises(NameError):
            self.HT2.findBaseLotSplit()

        self.HT2.workOrder = "FROG/MAN.WALKING"
        self.HT2.findBaseLotSplit()
        self.assertEqual("FROG", self.HT2.base)
        self.assertEqual("MAN", self.HT2.lot)
        self.assertEqual("WALKING", self.HT2.split)

    def test_findPartNumber(self):
        self.HT2 = HeatTreat()
        self.HT2.base = "TEST-BOLT"
        self.HT2.lot = "113"
        self.HT2.split = "0"

        self.HT2.findPartNumber(self.getCursor())

        self.assertEqual("MSA140818-1-07W018", self.HT2.partNumber)


        self.HT2 = HeatTreat()
        self.HT2.base = "TEST-BOLT"
        self.HT2.lot = "113"
        # self.HT2.split = "0"

        #split missing, assert error
        with self.assertRaises(NameError):
            self.HT2.findPartNumber(self.getCursor())

        self.HT2 = HeatTreat()
        self.HT2.base = "TEST-BOLT"
        # self.HT2.lot = "113"
        self.HT2.split = "0"

        #split missing, assert error
        with self.assertRaises(NameError):
            self.HT2.findPartNumber(self.getCursor())

        self.HT2 = HeatTreat()
        self.HT2.base = "FROG"
        self.HT2.lot = "MAN"
        self.HT2.split = "WALKING"

        #split missing, assert error
        with self.assertRaises(NameError):
            self.HT2.findPartNumber(self.getCursor())

    def test_findCustomer1(self):
        self.HT2 = HeatTreat()
        self.HT2.base = "TEST-BOLT"
        self.HT2.lot = "113"
        self.HT2.split = "0"
        self.HT2.PO = "1234"
        with self.assertRaises(NameError) as ex:
            self.HT2.findCustomer(self.getCursor())
        print("findcustomer1 ex: ", ex.exception)

    def test_findCustomer2(self):
        self.HT2 = HeatTreat()
        self.HT2.base = "TEST-BOLT"
        self.HT2.lot = "113"
        self.HT2.split = "0"
        self.HT2.PO = "INTERNAL"
        self.HT2.findCustomer(self.getCursor())
        self.assertEqual(self.HT2.customer, "INTERNAL")

        self.HT2 = HeatTreat()
        self.HT2.PO = "INTERNAL"
        self.HT2.findCustomer(self.getCursor())
        self.assertEqual(self.HT2.customer, "INTERNAL")

    def test_findCustomer3(self):
        self.HT2 = HeatTreat()
        self.HT2.base = "19-2513"
        self.HT2.lot = "2"
        self.HT2.split = "0"
        self.HT2.PO = "00FB634"
        self.HT2.findCustomer(self.getCursor())
        self.assertEqual(self.HT2.customer, "BOEING DISTRIBUTION SERVICES INC.")


    def getCursor(self):
        server = 'MSAVMFG1'
        database = 'VMLIVE'

        try:
            username = 'stefflc'
            password = 'buttpain1'
            cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = cnxn.cursor()
            return cursor
        except:
            print("server connection error")
'''
Test the save method of the models.py class HeatTreat
as if the $scope.update = function(data) function was invoked

Most of the other tests are related to $scope.createTTPI function for
creating a model from scratch

Test this part of the code -

if(self.dateOut and self.timeOut and self.soakTimeStart and self.dateIn):

'''
class TestHeatTreat_updateSave(TestCase):
    pass

class HTMLTest(TestCase):


    def test_basic_internal(self):
        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "AS7471",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        response = c.post(url, TTPIname)
        response.status_code
        print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)
        # print("response.client: ", response.client)
        # print("response.context: ", response.context)
        # print("response.json: ", response.json)
        # print("response.request: ", response.request)
        # print("response.templates: ", response.templates)
        # print("response.content: ", response.content)

    def test_basic_external(self):
        TTPIname ={
            "workOrder" : "19-2080/1",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "PWA96",
            "specRevision" : "R",
            "specMaterial" : "Inconel 718",
            "specMaterialSpec" : "AMS5662",
            "specMaterialSpecRevision" : "N",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "4014918",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        response = c.post(url, TTPIname)
        response.status_code
        print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)
        # print("response.client: ", response.client)
        # print("response.context: ", response.context)
        # print("response.json: ", response.json)
        # print("response.request: ", response.request)
        # print("response.templates: ", response.templates)
        # print("response.content: ", response.content)



    '''
    https://docs.djangoproject.com/en/2.2/topics/testing/tools/

    '''
    def test_basic_failRev(self):
        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "AS7471",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : "",
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        response = c.post(url, TTPIname)
        response.status_code
        # print("response: ", response.status_code)
        self.assertEqual(response.status_code, 400) #201 created
        self.assertIsNotNone(response.content)
        # print("response.content: ", response.content)


    '''
    Sending a blank string has interesting consequences
    It doesn't appear that the model .save is ever invoked
    in fact the HTTPResponse is just 400. It doesn't even go to the model!
    '''
    def test_basic_failWO(self):
        TTPIname ={
            "workOrder" : "",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "AS7471",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        response = c.post(url, TTPIname)
        response.status_code
        print("response: ", response.status_code)
        self.assertEqual(response.status_code, 400) #201 created
        self.assertIsNotNone(response.content)
        # print("response.content: ", response.content)

    def test_basic_failWO2(self):
        TTPIname ={
            "workOrder" : None,
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "AS7471",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        # c.post(url, TTPIname)
        with self.assertRaises(TypeError) as cm:
            c.post(url, TTPIname)
        print("cm: ", cm.exception)

    def test_basic_failWO3(self):
        #Beware: True gets transformed into string when it gets into the models.pyodbc
        #I.E. True is no longer a boolean inside models.py
        workOrders = ["1234", 1234, "Fred", True]
        try:
            for wo in workOrders:

                TTPIname ={
                    "workOrder" : wo,
                    "genBy" : "DANIEL-MORENO",
                    "specNumber" : "AS7471",
                    "specRevision" : "H",
                    "specMaterial" : "Waspaloy",
                    "specMaterialSpec" : "AMS5708",
                    "specMaterialSpecRevision" : "M",
                    "genDate" : "2019-10-14",
                    "partNumber" : 99,
                    "customer" : 99,
                    "rev" : 99,
                    "PO": "INTERNAL",
                    "heatNumber": "99",
                    "WOop" : "99",
                    "numLoads": 1,
                    "loadNumber": 1,
                }
                url = '/HeatTreat/treats/'
        

                c = Client()
                # c.post(url, TTPIname)
                with self.assertRaises(NameError) as cm:
                    # print("wo: ", wo)
                    c.post(url, TTPIname)
                print("cm: ", cm.exception)

        except AssertionError as err:
            print("err: ", err)


    # def test_findAllids(self):
    #     c = Client()
    #     url = '/HeatTreat/treats/'
    #     response = c.get(url)
    #     print("response get: ", response.content)


    def test_Spec1(self):

        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "1234",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        response = c.post(url, TTPIname)
        response.status_code
        # print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)


    def test_Spec2(self):

        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : 1234,
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        # c.post(url, TTPIname)
        response = c.post(url, TTPIname)
        response.status_code
        # print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)



    def test_Spec3(self):
        #Beware: True gets transformed into string when it gets into the models.pyodbc
        #I.E. True is no longer a boolean inside models.py


        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "Fred",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        response = c.post(url, TTPIname)
        response.status_code
        # print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)

    def test_post_get_delete(self):

        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : 1234,
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        # c.post(url, TTPIname)
        response = c.post(url, TTPIname)
        response.status_code
        # print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)


        # response2 = c.get(url)
        response2 = c.get('/HeatTreat/treats/1/')
        print("response2 code: ", response2.status_code)
        '''https://httpstatuses.com/200'''
        self.assertEqual(response2.status_code, 200) #request succeeded OK
        self.assertNotEqual(response2.content, "")
        self.assertNotEqual(response2.content, [])
        # print("response2: ", response2.content)

        # The “204 No Content” status code is often used with DELETE requests when no response body is sent.
        response3 = c.delete('/HeatTreat/treats/1/')
        # print("response3 code: ", response3.status_code)
        self.assertEqual(response3.status_code, 204) #successful delete

        response4 = c.get('/HeatTreat/treats/1/')
        # print("response4 code: ", response4.status_code)
        self.assertEqual(response4.status_code, 404) #not found - it's been deleted


    def test_post_update(self):
        TTPIname ={
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : 1234,
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : 99,
            "customer" : 99,
            "rev" : 99,
            "PO": "INTERNAL",
            "heatNumber": "99",
            "WOop" : "99",
            "numLoads": 1,
            "loadNumber": 1,
        }
        url = '/HeatTreat/treats/'


        c = Client()
        # c.post(url, TTPIname)
        response = c.post(url, TTPIname)
        response.status_code
        # print("response1: ", response.status_code)
        self.assertEqual(response.status_code, 201) #201 created
        self.assertIsNotNone(response.content)

        updateData ={
            # "id":1,
            "workOrder" : "TEST-BOLT/113",
            "genBy" : "DANIEL-MORENO",
            "specNumber" : "AS7471",
            "specRevision" : "H",
            "specMaterial" : "Waspaloy",
            "specMaterialSpec" : "AMS5708",
            "specMaterialSpecRevision" : "M",
            "genDate" : "2019-10-14",
            "partNumber" : "MSA140818-1-07W018",
            "customer" : "INTERNAL",
            "rev" : "INTERNAL",
            "PO": "INTERNAL",
            "heatNumber": "JR618/1",
            "WOop" : "80",
            "numLoads": 1,
            "loadNumber": 1,
            "numPans": "12",
        }

        dataSlug = {
                'numPans':12,
                }
        response = c.put('/HeatTreat/treats/1/', updateData, content_type = 'application/json' )
        # response = c.put('/HeatTreat/treats/1/', dataSlug )
        print("response.statuscode: ", response.status_code)
        print("response.content: ", response.content)





    ##this does not test product users, you have to make your own user in the test instance
    # def test_login(self):
    #     c = Client()
    #     c.login(username = 'stefflc', password = '')


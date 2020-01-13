from django.db import models
from django import forms
from django.db.models import Max
import pyodbc
from datetime import date, datetime, timedelta
from django.core.validators import MinValueValidator
from django.utils import timezone




# Create your models here.

#//04_03_19
#//Add to HeatTreat Save Method - checks for duplicate if trying to save a new WO
#04_08_19
##Add soakTimeMinusTol, PlusTol calculations into save method
##04/23/19 iin HeatTreat Save method ensure soakTimeMinus, PlusTol are set to 0 if they are exactly correct (not over, not under)

##04/23/19 - Added code to check if soak start < time in (E.g. 1:36 AM < 11:45PM) to assume that sok start has crossed midnight.
## Add 1 day to soak start such that soak start is > time in

##04/24/19 - Fixed an issue with operatorDoneDateTime where it would update anytime, not just when operator was done.
##05/02/19 - Fixed an issue with creating new specifications - duplicate check was not working

##05/28/19 - Update duplicate checking for multiple load orders. Now verifies on load - so every order can only have 1 load #1, 1 load #2, etc.
##Without new checking 18-4241/1 might get to load 6 due to asynchronous processing of POST request before it sees load 1 and catches for duplicate.

##09/05/19 - update REV to only get one result otherwise ERROR

##09/09/19 - add logic for approving specs to the class spec etc. This wil llock spec correctly.
##09/19/19 - postItNote added for use on a "post It Note (tm)" style sticky note

##09/25/19 - Update to allow Work Order lots that start with "TEST" to get through as these are itnernal and have no customer info

##09/27/19 - Add some fixes/logic to Heat lot, wo op to work with new Create TTPI such that if person manually enters heat lot
## or WO Operation# it will accept without warning

##10/16/19 - Rearrange HeatTreat class into individual functions for unit testing.
## Also fix issue with revision - was showing as "" which will cause problems during  a $scope.update call from .JS file

##10/17/19 - Fix error I made with if part number = 99 and not duplicate
#Cannot add an "else: raise NameError because the $Scope.update function uses this pathway



class HeatTreat(models.Model):
    ## All main properties of Solution Treat Orders table
    workOrder = models.CharField("Work Order", max_length=50) #0
    partNumber = models.CharField("Part Number", max_length=100) #1
    customer = models.CharField(max_length=250)#2
    rev = models.CharField(max_length=10) #3
    PO = models.CharField("Purchase Order", max_length=250) #4
    VF1Cap = models.BooleanField("VF1 Spec. Capacity", default=False) #5
    VF2Cap = models.BooleanField(default=False)#6
    TMQ1Cap = models.BooleanField(default=False) #7
    TMQ2Cap = models.BooleanField(default=False) #8
    TMQ3Cap = models.BooleanField(default=False) #9

    heatNumber = models.CharField("HEAT lot Number", max_length=20) #10
    WOop = models.IntegerField("Work Order Operation", blank=True) #11
    loadNumber = models.IntegerField("Heat Treat Load Number", blank = True, null = True, default = 1) #12
    numLoads = models.IntegerField("Number of Loads", blank = True, null = True, default = 1) #13
    coupons = models.BooleanField("Were Coupons Used?", default=True) #14
    couponInit = models.CharField("Initials",max_length=5, null = True, blank=True) #15
    visInspComplete = models.BooleanField("Visual Inspection Completed?", default=False) #16


    ##Below are not strictly required
    numPans = models.PositiveSmallIntegerField("Number of Pans", blank=True, null = True)  ## 0 to 32767 #17
    quantityLot = models.PositiveSmallIntegerField("Quantity parts per heat treat lot", blank=True, null = True) #18
    weightLot = models.PositiveIntegerField("Weight per heat treat lot", blank=True, null = True) #19
    dateTimeIn = models.DateTimeField("Date and Time of Heat Treat start", blank=True, null = True) #20
    
    dateIn = models.DateField("Date of Heat Treat Start", blank=True, null = True) #21
    timeIn = models.TimeField("Time of Heat Treat Start", blank = True, null = True) #22
#    timeIn = forms.TimeField(input_formats='%H:%M')
    ## https://docs.djangoproject.com/en/dev/ref/forms/fields/#datetimefield
    ## Try to use input_formats '%H:%M' # '14:30'
    
    
    furnaceNo = models.CharField("Furnace Number used for Heat Treat", max_length=50, blank=True, null = True) #23
    operatorIn = models.CharField("Operator who began heat treat", max_length=50, blank=True, null = True) #24
    preHeatStart = models.TimeField(blank=True, null = True) #25
    preHeatEnd = models.TimeField(blank=True, null = True) #26
    soakTimeStart = models.TimeField("Some time begin", blank=True, null = True) #27
    soakTimeEnd = models.TimeField("Soak time end", blank=True, null = True) #28
    dateTimeOut = models.DateTimeField("Date and Time out", blank=True, null = True) #29
    dateOut = models.DateField(blank=True, null=True) #30
    timeOut = models.TimeField(blank=True, null=True) #31
    operatorOut = models.CharField(max_length=50, blank=True, null = True) #32
    
    
    
    
    cleaningReqChoices =( ('Yes', 'Yes'), ('No', 'No'),('YES', 'YES'),('NO','NO'), )
    cleaningReq = models.CharField("Is cleaning required before heat treat?", max_length=3, choices=cleaningReqChoices, default='Yes', null = True) #33

    #VF Stuff
    VFPHTSetPoint = models.PositiveSmallIntegerField(blank = True, null = True) #34
    VFSoak = models.PositiveSmallIntegerField(blank = True, null = True) #35
    VFMinusTimeTol = models.PositiveSmallIntegerField(blank = True, null = True) #36
    VFPlusTimeTol = models.PositiveSmallIntegerField(blank = True, null = True) #37


    tempSetPointLow = models.PositiveSmallIntegerField(blank=True, null = True) #38
    tempSetPointHigh = models.PositiveSmallIntegerField(blank=True, null = True) #39
    tempSetPoint = models.PositiveSmallIntegerField(blank=True, null = True) #40
    tempSetPointPref = models.PositiveSmallIntegerField("Preferred Temp. for Work Order",blank=True, null = True) #40 #Preferred temp is independent of preferred temp on specification
    uniformityTol = models.PositiveSmallIntegerField("Soak temperature +/- tolerance", blank=True, null = True) #41
    soakTime = models.PositiveSmallIntegerField(blank=True, null = True , validators=[MinValueValidator(0)]) #42
    overrideSoakTime = models.PositiveSmallIntegerField(blank=True, null = True , validators=[MinValueValidator(0)]) #For use on 6-4 Titanium, spec RPS12.01 that have soak time based on part thickness. Cannot use Specications class as spec is not dependent upon thickness. 
    soakTimePref = models.PositiveSmallIntegerField(blank=True, null = True , validators=[MinValueValidator(0)]) #42
    soakTimeMinusTol = models.PositiveSmallIntegerField(blank=True, null = True) #43
    soakTimePlusTol = models.PositiveSmallIntegerField(blank=True, null = True) #44
    overrideSoakTimePlusTol = models.PositiveSmallIntegerField(blank=True, null = True) #For use on 6-4 Titanium, spec RPS12.01 that have soak time based on part thickness. Cannot use Specications class as spec is not dependent upon thickness. 
    VFVacPressure = models.PositiveSmallIntegerField("VF(Vacuum Furnace) Vacuum Pressure, in microns", blank=True, null = True) #45
    partialPressure = models.NullBooleanField(default=False, null = True) #46########################################################
    TMQHeatEnv = models.PositiveSmallIntegerField(blank=True, null = True) #47
    TMQTenPurge = models.NullBooleanField("10 Minute Purge performed for TMQ furnace? ", blank=True, null = True) #48 #####################
    channelOne = models.IntegerField("First Thermocouple Channel#", blank=True, null = True) #49 
    channelTwo = models.IntegerField("Second Thermocouple Channel#", blank=True, null = True) #50
    

    
    #Choice goes on the left, data to save in model goes on right (choice, model data)
    #blank (' ', ' ') is required so that user can save model before quench Method is chosen
#    quenchChoices = ( ('Oil', 'OIL'), ('OIL','OIL'),('oil','OIL'),('GFC','GFC'),
#                 ('gfc','GFC'),('Gfc','GFC'),('Water','WATER'),
#                 ('water','WATER'),('WATER','WATER'),('Air','AIR'),('air','AIR'),(' ',' ')) #Original set
    quenchChoices = (  ('OIL','OIL'),('GFC','GFC'),
                 ('WATER','WATER'),('AIR','AIR'),(' ',' ')) #Original set    
#    
#    
#    
    quenchMethod = models.CharField("Quench Method", max_length=5, choices=quenchChoices,default=" ", blank=True, null = True) #51
#    quenchMethod = models.CharField(max_length=5,default=" ", blank=True, null = True) #51

    
    agitReq = models.NullBooleanField("Is Agitation Required", blank=True, null = True) #52 ############
    tempBeforeQuench = models.PositiveSmallIntegerField(blank=True, null = True) #53
    tempAfterQuench = models.PositiveSmallIntegerField(blank=True, null = True) #54
    WQuenchDelay = models.PositiveSmallIntegerField("Titanium Quench Delay, in seconds", blank=True, null = True)  ## W = Titanium; Actual recorded delay from user
    WQuenchDelaySpec = models.PositiveSmallIntegerField("Titanium Quench Delay allowed for this order, based on thickness", blank=True, null = True)  #maximum quench delay based on thickness , for this specific WO
    
    
 
    #provides model validation and only allows these choices
    #partsCleanedChoices =( ('Yes', 'Yes'), ('No', 'No'),('YES', 'YES'),('NO','NO'), )
    #partsCleaned = models.CharField(max_length=3, choices=partsCleanedChoices, default='Yes', null = True) #56

    partsCleaned = models.CharField("Parts Cleaned after quench", max_length=3, default='No', blank = True, null = True) #56
    
    
    
    
    goodCond = models.NullBooleanField("Are Parts in Good Condition?", blank=True, null = True) #57 ####################
    PWAMCL = models.NullBooleanField(blank=True, null = True) #58
    PWABatchControl = models.NullBooleanField(blank=True, null = True) #59
    genBy = models.CharField(max_length=50, blank=True, null = True) #60
    genDate = models.DateField(blank=True, null = True) #61
    reviewBy = models.CharField(max_length=50, blank=True, null = True) #62
    reviewDate = models.DateField(blank=True, null = True) #63

    ##spec prefixes all appear to be from Solution Treat Specs table as well, but duplicated on Solution Treat Orders
    specNumber = models.CharField("Specification Numbe associated with TTPI", max_length=50, blank=True) #64
    specRevision = models.CharField(max_length=50, blank=True) #65
    specMaterial = models.CharField(max_length=50, blank=True) #66
    specMaterialSpec = models.CharField(max_length=50, blank=True) #67
    specMaterialSpecRevision = models.CharField(max_length=50, blank=True) #68
    locked = models.BooleanField("Is this TTPI locked, preventing further revision?", default = False) #69
#    class MyForm(forms.Form):
#        timeIn = forms.TimeField(input_formats='%H:%M')
    operatorDone = models.BooleanField("Has the operator completed their work?", blank=True, default=False)
    operatorDoneDateTime = models.DateTimeField("Time operator completed worked", null = True, blank=True)
    certCreated = models.BooleanField(default=False) ### PrintCert override save method should change this to True. Then ViewSet can use this variable for showing HeatTreat object(s) without PrintCert associated object(s)

    postItNote = models.CharField(max_length = 1000, blank = True)
    ###
    #soakTime = Date Out, Time Out - Date In, Soak Start



    def save(self,*args, **kwargs):
        # print("save method------------------------")
        # print("type of partNumber: ", type(self.partNumber))



        # if self.workOrder:
        #     pass
            # print("------------------------------------------------------------Entering save method")
####################Add validation to not do anything if WO number and exact load number already exists
            ###Multiple loads will have many TTPI to one WO, but 1:1 on load NU
        # print("self.timeOut: ", self.timeOut)
        # print("type self.timeOut: ", type(self.timeOut))
        
        

        
        if(self.dateOut and self.timeOut and self.soakTimeStart and self.dateIn):
            
            if(self.operatorDone):
                self.operatorDoneDateTime = timezone.now()
            
            DTOut = datetime.combine(self.dateOut, self.timeOut)
            DTIn = datetime.combine(self.dateIn, self.soakTimeStart)
            # print("dateTimeOut: ", DTOut)
            # print("dateTimeIn: ", DTIn)
            
            ''' If soak Start time is before Time In this means that soak start crossed Midnight.(or operator completely messed up time)'''
            if(self.soakTimeStart < self.timeIn): 
                DTIn = DTIn + timedelta(days = 1)
            timeDelta = DTOut - DTIn
            # print("timeDelta: ", timeDelta)
            timeDeltaMinutes = divmod(timeDelta.total_seconds(), 60)[0]

            # print("timeDeltaMinutes: ", timeDeltaMinutes)
            self.soakTime = timeDeltaMinutes
            if(self.soakTime <0):
                self.soakTime = 0
                raise ValueError("Soak Duration cannot be negative time!!!!!!")
            
            spec = SolutionTreatSpecs.objects.filter(specNumber = self.specNumber).filter(specRevision = self.specRevision).filter(specMaterial = self.specMaterial).filter(specMaterialSpec = self.specMaterialSpec).filter(specMaterialSpecRevision = self.specMaterialSpecRevision)
            spec = spec[0]
            # print("this spec: ", spec)
            # print("spec.specSoakTime: ", spec.specSoakTime)
            # print("spec.specSoakMinusTimeTol: ", spec.specSoakMinusTimeTol)
            # print("spec.specSoakPosTimeTol: ", spec.specSoakPosTimeTol)
            
            
            ''' If self.overrideSoakTime is true, 6-4 Titanium or spec number RPS 12.01 is being used which requires soak Time by thickness 
            (manager manually entered) rather than soak time by specification'''
            if(self.overrideSoakTime):
                actualSpecSoakTime = self.overrideSoakTime
                try:
                    actualspecPosTimeToal = self.overrideSoakTimePlusTol
                except:
                    raise ValueError("Override process time present, but override + Time Tolerance NOT present.")
            else:
#                print("alf5")
                actualSpecSoakTime = spec.specSoakTime
                actualspecPosTimeToal = spec.specSoakPosTimeTol
     
            
            '''Calculate Process Soak Time automatically for the "Actual Values" column of Solution Treat TTPI'''    
            if (self.soakTime < (actualSpecSoakTime - spec.specSoakMinusTimeTol) ):
                ##console.log("too low");
                self.soakTimeMinusTol = (actualSpecSoakTime - self.soakTime);
                # print("self.soakTimeMinusTol: ", self.soakTimeMinusTol)
                self.soakTimePlusTol = 0;
                # print("You are -"+str(self.soakTimeMinusTol)+" vs soak time. Spec allows -"+str(spec.specSoakMinusTimeTol));
#                print("alf4")
            
            
            
            elif (self.soakTime > (actualSpecSoakTime + actualspecPosTimeToal)):
#                //console.log("too high");
                self.soakTimePlusTol =( self.soakTime - actualSpecSoakTime   );
                self.soakTimeMinusTol = 0; 
                # print("You are +"+str(self.soakTimePlusTol)+" vs soak time. Spec allows +"+str(actualspecPosTimeToal)) ;
#                print("alf6")
            
            else:
#                console.log("just right");
#                print("alf7")
                # print("self.soakTimePlusTol: ", self.soakTimePlusTol)
                if(self.soakTime > actualSpecSoakTime):
                    self.soakTimePlusTol = self.soakTime - actualSpecSoakTime;
                    print("self.soakTimePlusTol = self.soakTime - actualSpecSoakTime: ",self.soakTimePlusTol, " = ", self.soakTime, "-", actualSpecSoakTime  )
                    self.soakTimeMinusTol = 0
                
                elif (self.soakTime < actualSpecSoakTime):
                    self.soakTimeMinusTol = spec.specSoakTime - self.soakTime;
                    self.soakTimePlusTol = 0
                else:
                    self.soakTimeMinusTol =0
                    self.soakTimePlusTol = 0
        
    
    
            
            
            
            
            super(HeatTreat, self).save(*args, **kwargs)


        #Create new TTPI portion 
        ##Javascript will set variables to 99 on POST request, then do Visual search to find correct value(s)
        # print(self.partNumber)
        # print(type(self.partNumber))
        
        ''' Check for duplicates before creating a new WO ####'''
        self.notDuplicateWO = False
        
        if self.partNumber == "99":
            self.checkForDuplicates()

        if self.partNumber == "99" and self.notDuplicateWO:
            ## Connect to the Visual Database
            server = 'MSAVMFG1'
            database = 'VMLIVE'
#            database = 'MSA712'
            try:
                username = 'stefflc'
                password = 'buttpain1' 
                cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
                cursor = cnxn.cursor()  
            
            except:
                print("server connection error")


            self.findBaseLotSplit()
            self.findPartNumber(cursor)
            self.findCustomer(cursor)
            self.findRevision(cursor)
            #find and do HEAT#
            self.findHeatNumber(cursor)
            self.findOperationNumber(cursor)

            cnxn.close()
        # else:
            #cannot use else here, this will catch a regular $http.put request from $scope.update = function(data)
            # in HeatTreat.JS
        #     raise NameError("Either unfound duplicate or partNumber was not passed 99")
        super(HeatTreat, self).save(*args, **kwargs)




    def __str__(self):
        return self.workOrder

    def testOutput():
        print("We're in the models.py file")
        return

    def findRevision(self, cursor):
        cursor.execute("SELECT WORK_ORDER.DRAWING_REV_NO FROM WORK_ORDER WHERE WORK_ORDER.BASE_ID = ? AND WORK_ORDER.LOT_ID = ? AND WORK_ORDER.SPLIT_ID = ? AND DRAWING_REV_NO IS NOT NULL", (self.base, self.lot, self.split))
        poREV = cursor.fetchall()
        # print("PO REV: ~~", poREV)
        try:
            self.rev = poREV[0][0]
        except IndexError:
            raise NameError("Error finding PO drawing revision E.G.: NC")
            self.rev = "REV ERROR"
        except Exception:
            raise NameError("Unknown error find PO drawing rev.")

    def checkForDuplicates(self):
        '''load number is necessary to ensure duplicate loads are not created
            but to also not get a false positive on multiple load orders'''
        checkWorkOrder = HeatTreat.objects.filter(workOrder = self.workOrder, loadNumber = self.loadNumber)
        # print("checkWorkOrder revised: ", checkWorkOrder)
#            print("checkwororder1: ", checkWorkOrder)
        if(checkWorkOrder):
            # print("checkWorkOrder: ", checkWorkOrder)
            # print("Duplicate exists")
            raise NameError("Duplicate Exists. Cannot create work order: "+ str(self.workOrder)+ " Load: "+ str(self.loadNumber) )
        else:
            # print("-----------------------------------------------------not duplicate")
            self.notDuplicateWO = True
        #################################
    def findBaseLotSplit(self):
        # print("self.workOrder: ", self.workOrder)
        # print("typeselfworkorder: ", type(self.workOrder))
        if(self.workOrder == None):
            raise NameError("Error - workorder is None")
        elif(self.workOrder == ""):
            raise NameError("Error - workorder is blank")
        elif(self.workOrder == "True"):
            raise NameError("Error - looks like Boolean")
        else:
            try:
                self.base,self.lotsplit = self.workOrder.split("/")
            except:
                raise NameError("Error - work order missing '/' ")
    
            try :
                self.lot,self.split = self.lotsplit.split(".")
            except :  
                self.lot = self.lotsplit
                self.split = '0'

    def findPartNumber(self, cursor):
        #Do visual to find Part Number
        try:
            cursor.execute("SELECT WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID, WORK_ORDER.SPLIT_ID, WORK_ORDER.TYPE, PART.MFG_PART_ID FROM PART INNER JOIN WORK_ORDER ON PART.ID = WORK_ORDER.PART_ID WHERE BASE_ID = ? AND LOT_ID = ? AND SPLIT_ID = ? ",(self.base, self.lot, self.split) )

            # print("UH OH execute")

            PN = cursor.fetchall()
            if (PN == []):
                raise NameError("Cannot find work order matching: ", str(self.base) + '/'+str(self.lot)+"."+str(self.split))
            # print("all PN: ", PN)
            # print("Pn4: ", PN[0][4])
        except Exception as ex:
            raise NameError("Cannot find Work Order information. Base, lot, or split is missing.")
            print("error ex: ", ex)
        
        try:
            self.partNumber = PN[0][4]
        except:
            self.partNumber = "PN ERROR"

    def findCustomer(self, cursor):
        # print("self.PO : ", self.PO)
        if(self.PO == "INTERNAL"):
            # print("temp")
            self.customer = "INTERNAL"
    
            try:
                self.findRevision(cursor)
            except:
                self.rev = "REV ERROR"
    
        else: #Do regular stuff
            cursor.execute('''SELECT     CUSTOMER.NAME,  CUSTOMER_ORDER.CUSTOMER_PO_REF, 
                           CUST_ORDER_LINE.LINE_STATUS, CUSTOMER_ORDER.STATUS, 
                           WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID, WORK_ORDER.SPLIT_ID                      
            FROM  CUSTOMER INNER JOIN
                CUSTOMER_ORDER ON CUSTOMER.ID = CUSTOMER_ORDER.CUSTOMER_ID INNER JOIN
                CUST_ORDER_LINE ON CUSTOMER_ORDER.ID = CUST_ORDER_LINE.CUST_ORDER_ID INNER JOIN
                PART ON CUST_ORDER_LINE.PART_ID = PART.ID INNER JOIN
                WORK_ORDER ON PART.ID = WORK_ORDER.PART_ID
            WHERE CUSTOMER_ORDER.STATUS = ? 
                AND CUST_ORDER_LINE.LINE_STATUS = ? 
                AND BASE_ID = ? 
                AND LOT_ID = ? 
                AND SPLIT_ID = ? 
                AND (USER_ORDER_QTY - TOTAL_USR_SHIP_QTY > 0)
                AND CUSTOMER_ORDER.CUSTOMER_PO_REF = ?
            GROUP BY CUSTOMER.NAME, CUSTOMER_ORDER.CUSTOMER_PO_REF,
                CUST_ORDER_LINE.LINE_STATUS,
                CUSTOMER_ORDER.STATUS, WORK_ORDER.BASE_ID,
            WORK_ORDER.LOT_ID, WORK_ORDER.SPLIT_ID''',('R','A',self.base,self.lot,self.split, self.PO))
            
            customers = cursor.fetchall()
            # if(customers == []):


            # print("length: ", len(customers))
            
            try:
                #If 1, do nothing
                if (len(customers) == 1):
                    self.customer = customers[0][0]
                #else, add warning that multiples may exist to user
                elif (len(customers) >1):
                    raise NameError("Multiple customer matches found.")
                else:
                    #Check for assemblies
    
                    cursor.execute('''
                                   SELECT     CUSTOMER.NAME, CUSTOMER_ORDER.ID AS ORDER_ID, CUSTOMER_ORDER.CUSTOMER_PO_REF
                                   FROM         CUSTOMER INNER JOIN
                                       CUSTOMER_ORDER ON CUSTOMER.ID = CUSTOMER_ORDER.CUSTOMER_ID
                                   WHERE     (CUSTOMER_ORDER.ID = ?) AND (CUSTOMER_ORDER.CUSTOMER_PO_REF = ?)
                                   ''', (self.base, self.PO))
                    checkAssembly = cursor.fetchall()
                    if(len(checkAssembly) == 1):
                        self.customer = checkAssembly[0][0]
                    else:
                        raise NameError("No match found between given PO to a customer or assembly...")
    
            except NameError as ey:
                raise NameError(ey) #Essentially re-raises error from lower level
            except Exception as ex:
                print("error: ", ex)
                raise NameError("Unknown error finding customer name.")
                self.customer = "CUSTOMER ERROR" ##Do not change this erro unless you update HTML to highlight a new error
                # self.PO = "PO ERROR" ##Do not change this erro unless you update HTML to highlight a new error

    def findHeatNumber(self, cursor):
            if (self.heatNumber == 99 or self.heatNumber == "99"):
                cursor.execute('''
                               SELECT     TRACE.APROPERTY_1, TRACE.APROPERTY_2, PART.DESCRIPTION, INVENTORY_TRANS.TRANSACTION_DATE, INVENTORY_TRANS.PART_ID, 
                          PART.PRODUCT_CODE, TRACE_INV_TRANS.TRACE_ID, INVENTORY_TRANS.WORKORDER_BASE_ID, INVENTORY_TRANS.WORKORDER_LOT_ID, 
                          INVENTORY_TRANS.WORKORDER_SPLIT_ID, INVENTORY_TRANS.OPERATION_SEQ_NO, INVENTORY_TRANS.TYPE, INVENTORY_TRANS.CLASS, 
                          REQUIREMENT.STATUS
                          FROM         TRACE INNER JOIN
                          TRACE_INV_TRANS ON TRACE.PART_ID = TRACE_INV_TRANS.PART_ID AND TRACE.ID = TRACE_INV_TRANS.TRACE_ID INNER JOIN
                          INVENTORY_TRANS ON TRACE_INV_TRANS.TRANSACTION_ID = INVENTORY_TRANS.TRANSACTION_ID INNER JOIN
                          REQUIREMENT ON TRACE.PART_ID = REQUIREMENT.PART_ID INNER JOIN
                          PART ON TRACE.PART_ID = PART.ID AND REQUIREMENT.PART_ID = PART.ID
                          WHERE     (INVENTORY_TRANS.TYPE = 'O') AND (INVENTORY_TRANS.CLASS = 'I') AND (NOT (REQUIREMENT.STATUS = 'X')) AND (PART.DESCRIPTION LIKE 'RM%' OR  PART.DESCRIPTION LIKE 'BL%')
                          AND INVENTORY_TRANS.WORKORDER_BASE_ID = ? AND INVENTORY_TRANS.WORKORDER_LOT_ID = ? AND INVENTORY_TRANS.WORKORDER_SPLIT_ID = ?
                          GROUP BY  TRACE.APROPERTY_1, TRACE.APROPERTY_2, PART.DESCRIPTION, INVENTORY_TRANS.TRANSACTION_DATE, INVENTORY_TRANS.PART_ID, 
                          PART.PRODUCT_CODE, TRACE_INV_TRANS.TRACE_ID, INVENTORY_TRANS.WORKORDER_BASE_ID, INVENTORY_TRANS.WORKORDER_LOT_ID, 
                          INVENTORY_TRANS.WORKORDER_SPLIT_ID, INVENTORY_TRANS.OPERATION_SEQ_NO, INVENTORY_TRANS.TYPE, INVENTORY_TRANS.CLASS, 
                          REQUIREMENT.STATUS
                          ORDER BY INVENTORY_TRANS.TRANSACTION_DATE DESC
                          ''', (self.base, self.lot, self.split))
                heats = cursor.fetchall()
                try:
                    self.heatNumber = heats[0][0]
                    # print("heats00: ", heats[0][0])
                except:
                    # self.heatNumber = "HEAT ERROR"
                    raise NameError("Cannot find Heat Lot# or error with Heat #. Please try entering Heat#.")
        #            print("HEATS: ", heats)
            elif(self.heatNumber and self.heatNumber != ""):
                pass #just use self.heatNumber
                # self.heatNumber = self.heatNumber
            else:
                raise NameError("Heat Number passed should be 99 or actual value")
                print("heat Number is not 99")

    def findOperationNumber(self, cursor):
        ##Find and do Operation#
        ## Looks for operations that are status R and resource ID = N% or OPHT
        ## IF multiple, list all
        if(self.WOop == 99 or self.WOop == "99"):
            try:
                cursor.execute('''SELECT SEQUENCE_NO, RESOURCE_ID, STATUS, WORKORDER_BASE_ID, WORKORDER_LOT_ID, WORKORDER_SPLIT_ID FROM OPERATION
                               WHERE WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? AND WORKORDER_SUB_ID = '0' AND STATUS = 'R' AND (RESOURCE_ID LIKE 'N%' OR RESOURCE_ID LIKE 'OPHT')
                               ORDER BY SEQUENCE_NO''', (self.base, self.lot, self.split))
            except Exception as ex:
                print("error234", ex)
            try:
                operations = cursor.fetchall()
            
                # print("OPS : ", operations)
            except Exception as ex:
                print("operations error")
                print("ex: ", ex)

            try:
                self.WOop = operations[0][0]

            except Exception as ex:
                print("Ex2: ", ex)

                #This will cancel the whole proess!!
                raise NameError("No operation found, please enter optional Op#.")
                # self.WOop = 999
        elif(self.WOop and self.WOop != ""):
            pass
            # self.WOop == self.WOop
        else:
            raise NameError("Check Work Order Operation#")
            print("Check Work Order Operation #")


class SolutionTreatSpecs(models.Model):
    ##Due to integration with SQLite back end, , validators=[MinValueValidator(0)] is needed to only save >=0 values
    # https://stackoverflow.com/questions/29067045/django-positiveintegerfield-accepting-negatives See this thread
    
    
    
    ##First 5 are absolutely required
    specNumber = models.CharField(max_length=50) #0
    specRevision = models.CharField(max_length=50) #1
    specMaterial = models.CharField(max_length=50) #2
    specMaterialSpec = models.CharField(max_length=50) #3
    specMaterialSpecRevision = models.CharField(max_length=50) #4
    
    
    
    specVF1 = models.NullBooleanField(blank=True, null=True) #5
    specVF2 = models.NullBooleanField(blank=True, null=True) #6
    specTMQ1 = models.NullBooleanField(blank=True, null=True) #7
    specTMQ2 = models.NullBooleanField(blank=True, null=True) #8
    specTMQ3 = models.NullBooleanField(blank=True, null=True) #9
    specCleaning = models.CharField(blank=True, null=True,max_length=3,default="Yes") #10
    
    VFPHTSetPointLow = models.PositiveSmallIntegerField(blank=True, default= 0, null=True, validators=[MinValueValidator(0)]) #11
    VFPHTSetPointHigh = models.PositiveSmallIntegerField(blank=True, default = 0, null=True, validators=[MinValueValidator(0)]) #12
    VFPHTSetPointPref = models.PositiveSmallIntegerField(blank=True, default= 0, null=True, validators=[MinValueValidator(0)]) #13
    VFSoak = models.PositiveSmallIntegerField(blank=True, default= 0, null=True, validators=[MinValueValidator(0)]) #14
    VFSoakPref = models.PositiveSmallIntegerField(blank=True, default= 0, null=True, validators=[MinValueValidator(0)]) #15
    VFMinusTimeTol = models.IntegerField(blank=True, default= 0, null=True) #16
    VFPlusTimeTol = models.PositiveSmallIntegerField(blank=True, default= 0, null=True, validators=[MinValueValidator(0)]) #17
    
    
    specTempSetPointLow = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #18
    specTempSetPointHigh = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #19
    specTempSetPointPref = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #20
    specUniformityTol = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #21
    specUniformityTolPref = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #22
    specSoakTime = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #23
    specSoakTimePref = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #24 
    specSoakMinusTimeTol = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #25
    specSoakPosTimeTol = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #26
    specVFVacPressure = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)]) #27
    specTMQHeatLow = models.PositiveSmallIntegerField(blank=True, null=True,default="25", validators=[MinValueValidator(0)])
    specTMQHeatHigh = models.PositiveSmallIntegerField(blank=True, null=True,default="50", validators=[MinValueValidator(0)])
    specLoadTC = models.CharField(max_length=50, blank=True, null=True)
    specQuenchGFC = models.NullBooleanField(blank=True, null=True)
    specQuenchOil = models.NullBooleanField(blank=True, null=True)
    specQuenchWater = models.NullBooleanField(blank=True, null=True)
    specQuenchAir = models.NullBooleanField(blank=True, null=True)
    specTempBeforeQuenchLow = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specTempBeforeQuenchHigh = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specTempAfterQuenchMax = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specTitaniumQuenchDelayMax = models.PositiveSmallIntegerField(blank=True, null = True, validators=[MinValueValidator(0)])
    specPartsCleanedAfterQuench = models.CharField(max_length=50, blank=True, null=True, default="No")  ##cannot use Boolean
    specMasterReviewed = models.CharField(max_length=50, blank=True, null=True)
    specMasterApproved = models.CharField(max_length=50, blank=True, null=True)
    specFormRevision = models.PositiveSmallIntegerField(blank=True, null=True)
    specFormRevDate = models.DateField(blank=True, null=True)
    mostCurrent = models.BooleanField(default = False)
    specLocked = models.BooleanField(default = False)
    
    def save(self,*args, **kwargs):
        print("save method------------SolutionTreatSpecs------------")
        
        if self.specFormRevision is None:
            phil = SolutionTreatSpecs.objects.filter(specNumber = self.specNumber).filter(specRevision=self.specRevision).filter(specMaterial=self.specMaterial).filter(specMaterialSpec=self.specMaterialSpec)
            try:
                print("phil[0]: ", phil[0]) #This will test an empty queryset I.E. QuerySet [] which wil lbreak
                print("duplicates exist! :", phil) #This will not error out if QuerySet[] exists
                return #do not save
            except:
                print("No duplicates, probably")
                
            self.specFormRevision = 0
            self.mostCurrent = True ##If there is nothing else and program did not return, this is most current
            print(self.specFormRevision)
            
        if self.specFormRevision == 99:
            phil = SolutionTreatSpecs.objects.filter(specNumber = self.specNumber).filter(specRevision=self.specRevision).filter(specMaterial=self.specMaterial).filter(specMaterialSpec=self.specMaterialSpec)
            phil = phil.exclude(specFormRevision = 99) #Remove 99, as this is the one we just copied
            phil = phil.order_by('specFormRevision') #Order by form revision, so last is highest value
            phil = phil.last() #Get last (now highest) value. This is the highest value excluding the 99 we just copied.
            
            phil.mostCurrent = False #Set mostCurrent = False for the spec being copied. Once copied it is no longer most current!
            phil.specLocked = True #Just in case old spec isn't locke, go ahead and lock it for safety!
            
            print(phil)
            self.specFormRevision = phil.specFormRevision + 1 #Now set your 99 (just copied) as being +1 over the previous highest value.
            self.id = None #If you do this, then when you save it will auto increment id and create a copy #This copies incremented specification with its new form revision value
            self.specMasterReviewed = None
            self.specFormRevDate = None
            self.specMasterApproved = None
            self.specFormRevDate = str(date.today().isoformat()) #Should do 2002-12-04 ISO 8601 format
            self.mostCurrent = True
            
            super(SolutionTreatSpecs, phil).save(*args, **kwargs)   #This is required to perform the phil.mostCurrent = False update

        ##This is for use when approving a new specification
        if self.specMasterApproved:
            self.specLocked = True

        super(SolutionTreatSpecs, self).save(*args, **kwargs)
    def __str__(self):
        return self.specNumber

class PrintCert(models.Model):
    workOrder = models.CharField(max_length=50)
    partNumber = models.CharField(max_length=100,blank=True, null = True)
    partRev = models.CharField(max_length=10,blank=True, null = True)
    customer = models.CharField(max_length=50,blank=True, null = True)
    coupons = models.NullBooleanField(default=True,blank=True, null = True)
    
    specNumber = models.CharField(max_length=50,blank=True, null = True) #0
    specRevision = models.CharField(max_length=50,blank=True, null = True) #1
    specMaterial = models.CharField(max_length=50,blank=True, null = True) #2
    specMaterialSpec = models.CharField(max_length=50,blank=True, null = True) #3
    specMaterialSpecRevision = models.CharField(max_length=50,blank=True, null = True) #4
    
    #material  = models.CharField(max_length=50,blank=True, null = True)
    quantityTotal = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad1 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad2 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad3 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad4 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad5 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad6 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad7 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad8 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad9 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad10 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad11 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad12 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad13 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad14 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad15 = models.PositiveSmallIntegerField(blank=True, null = True)
    quantityLoad16 = models.PositiveSmallIntegerField(blank=True, null = True)
    
    
    PO = models.CharField(max_length=100,blank=True, null = True)
    heatNumber = models.CharField(max_length=20,blank=True, null = True)
    weightTotal = models.PositiveIntegerField(blank=True, null = True)
    weightLoad1 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad2 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad3 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad4 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad5 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad6 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad7 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad8 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad9 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad10 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad11 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad12 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad13 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad14 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad15 = models.PositiveIntegerField(blank=True, null = True)
    weightLoad16 = models.PositiveIntegerField(blank=True, null = True)
    #process # ?
    loadsTotal = models.IntegerField(blank = True, null = True, default = 1)

    specTempLow = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specTempHigh  = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specSoakTime  = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specSoakMinusTimeTol  = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    specSoakPosTimeTol  = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
 
    furnaceNoLoad1 = models.CharField(max_length=50, blank=True, null = True)
    soakTempLoad1 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad2 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad3 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad4 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad5 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad6 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad7 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad8 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad9 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad10 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad11 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad12 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad13 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad14 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad15 = models.PositiveSmallIntegerField(blank=True, null = True)
    soakTempLoad16 = models.PositiveSmallIntegerField(blank=True, null = True)
    
    soakTimeStartLoad1 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad2 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad3 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad4 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad5 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad6 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad7 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad8 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad9 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad10 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad11 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad12 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad13 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad14 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad15 = models.TimeField(blank=True, null = True)
    soakTimeStartLoad16 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad1 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad2 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad3 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad4 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad5 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad6 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad7 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad8 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad9 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad10 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad11 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad12 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad13 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad14 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad15 = models.TimeField(blank=True, null = True)
    soakTimeEndLoad16 = models.TimeField(blank=True, null = True)
    SoakTimeLoad1 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad2 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad3 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad4 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad5 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad6 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad7 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad8 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad9 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad10 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad11 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad12 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad13 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad14 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad15 = models.PositiveSmallIntegerField(blank=True, null = True)
    SoakTimeLoad16 = models.PositiveSmallIntegerField(blank=True, null = True)
    
    quenchMethodLoad1 = models.CharField(max_length=5, default=" ", blank=True, null = True)
    
    PWAMCL = models.NullBooleanField(blank=True, null = True)
    PWABatchControl = models.NullBooleanField(blank=True, null = True)
    dateOut = models.DateField(blank=True, null=True)
    dateCertCreated = models.DateTimeField(blank = True, null = True, editable = False )
    dateCertModified = models.DateTimeField(blank = True, null = True)
    certSaved = models.NullBooleanField(blank = True, null = True, default = False)
    certSavedNotes = models.CharField(max_length = 1000, blank = True, null = True)
    overrideSafeguard = models.BooleanField("If yes, allows any input", default = False)
    
#    quenchMethodLoad2 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad3 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad4 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad5 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad6 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad7 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad8 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad9 = models.CharField(max_length=5, default=" ", blank=True, null = True)
#    quenchMethodLoad10 = models.CharField(max_length=5, default=" ", blank=True, null = True)

    def save(self, *args, **kwargs):
        previousCerts = PrintCert.objects.filter(workOrder = self.workOrder)
        if previousCerts and not self.overrideSafeguard:
            self.certSavedNotes = "Cert Already Exists."
        print("Before first if")
        print("previouscerts: ", previousCerts)
        if not previousCerts or self.overrideSafeguard:
            print("hello doggie")
#        if (not):
           
            ##If we cannot find another cert with the same workorder number, then go ahead and add it below. else return and do nothing.
            
            if self.workOrder:
                print("if self workorder")
                orders = HeatTreat.objects.filter(workOrder = self.workOrder)
                    
                
                if(orders is not None):
                    
                    print("Orders: ", orders)
                    print("Orders[o]:", orders[0])
                    print("test1: ", orders[0].specNumber)
                    self.specNumber = orders[0].specNumber
                    self.specRevision = orders[0].specRevision
                    self.specMaterial = orders[0].specMaterial
                    self.specMaterialSpec = orders[0].specMaterialSpec
                    self.specMaterialSpecRevision = orders[0].specMaterialSpecRevision
                    
                    if not self.id:
                        self.dateCertCreated = timezone.now()
                    self.dateCertModified = timezone.now()
                    
                    specs = SolutionTreatSpecs.objects.filter(specNumber=self.specNumber).filter(specRevision = self.specRevision).filter(specMaterial = self.specMaterial).filter(specMaterialSpec = self.specMaterialSpec).filter(specMaterialSpecRevision = self.specMaterialSpecRevision)
                    print("specs: ", specs)
                    SPEC = specs[0]
                    
                    
                    HT = list()
                    for x in range(len(orders)):
                        try:
                            HT.append(orders[x])
                        except:
                            print("HT TOO LONG")                    
                    self.coupons = HT[0].coupons
                    self.partNumber = HT[0].partNumber
                    self.partRev = HT[0].rev
                    self.PO = HT[0].PO
                    self.customer = HT[0].customer
                    self.heatNumber = HT[0].heatNumber
                    self.loadsTotal = HT[0].numLoads
                    self.dateOut = HT[0].dateOut
           
                    self.PWAMCL = HT[0].PWAMCL
                    self.PWABatchControl = HT[0].PWABatchControl
                    
                    self.weightLoad1 = HT[0].weightLot
                    self.furnaceNoLoad1 = HT[0].furnaceNo
                    self.soakTempLoad1 = HT[0].tempSetPoint
                    self.soakTimeStartLoad1 = HT[0].soakTimeStart
                    self.soakTimeEndLoad1 = HT[0].timeOut ##HT[0].soakTimeEnd ##Soak Time is calculated based on Time Out, not Soak End!
                    self.SoakTimeLoad1 = HT[0].soakTime
                    self.quenchMethodLoad1 = HT[0].quenchMethod
                    self.quantityLoad1 = HT[0].quantityLot
                    
                    #spec stuff
                    self.specNumber = SPEC.specNumber
                    self.specRevision = SPEC.specRevision
                    self.specMaterial =  SPEC.specMaterial
                    self.specMaterialSpec = SPEC.specMaterialSpec
                    self.specMaterialSpecRevision = SPEC.specMaterialSpecRevision
                    self.specTempLow = SPEC.specTempSetPointLow
                    self.specTempHigh = SPEC.specTempSetPointHigh
                    '''Override spec time for 6-4 and RPS 12.01 due to spec temp being derived from thickness. I.E. soak time is variable for these specs, not constant '''
                    if(orders[0].overrideSoakTime and orders[0].overrideSoakTime != 0 and orders[0].overrideSoakTime != ""):
                        self.specSoakTime = orders[0].overrideSoakTime
                    else:
                        self.specSoakTime = SPEC.specSoakTime
                    self.specSoakMinusTimeTol = SPEC.specSoakMinusTimeTol
                    '''Override spec time for 6-4 and RPS 12.01 due to spec temp being derived from thickness. I.E. soak time is variable for these specs, not constant '''
                    if(orders[0].overrideSoakTimePlusTol and orders[0].overrideSoakTimePlusTol !=0 and orders[0].overrideSoakTimePlusTol != ""):
#                        print("alf1")
                        self.specSoakPosTimeTol = orders[0].overrideSoakTimePlusTol
                    else:
#                        print("alf2")
                        self.specSoakPosTimeTol = SPEC.specSoakPosTimeTol 
                    
                    self.quantityTotal = self.quantityLoad1
                    self.weightTotal = self.weightLoad1
                    ###This is checked for 1st load (only first load) in HeatTreat.js
                    # if(HT[0].reviewBy is None or HT[0].reviewBy == ""):
                    #     print("reviewby Missing at load 1 ")
                    #     raise NameError("reviewBy signature missing -  error. Check load 1")
                    
                    if(self.loadsTotal > 1):
                        print("total loads = :", self.loadsTotal)
                        for x in range(0, self.loadsTotal):
                            print("HT[x].reviewby: ", HT[x].reviewBy)
                            if(HT[x].reviewBy is None or HT[x].reviewBy == ""):
                                print("reviewby Missing at ", x)
                                raise NameError("reviewBy signature missing -  error. Check load", x+1)
                        
                        
                        
    #                    LOAD_NUMBER = str
                        
                        self.weightLoad2 = HT[1].weightLot
                        self.soakTempLoad2 = HT[1].tempSetPoint
                        self.soakTimeStartLoad2 = HT[1].soakTimeStart
                        self.soakTimeEndLoad2 = HT[1].timeOut
                        self.SoakTimeLoad2 = HT[1].soakTime
    #                    self.quenchMethodLoad2 = HT[1].quenchMethod
                        self.quantityLoad2 = HT[1].quantityLot
                        
                        self.quantityTotal += self.quantityLoad2
                        self.weightTotal += self.weightLoad2
                        if(HT[1].dateOut > self.dateOut):
                            self.dateOut = HT[1].dateOut
                        
                
                        try:
                            self.weightLoad3 = HT[2].weightLot
                            self.soakTempLoad3 = HT[2].tempSetPoint
                            self.soakTimeStartLoad3 = HT[2].soakTimeStart
                            self.soakTimeEndLoad3 = HT[2].timeOut
                            self.SoakTimeLoad3 = HT[2].soakTime
        #                    self.quenchMethodLoad3 = HT[2].quenchMethod
                            self.quantityLoad3 = HT[2].quantityLot
                            
                            self.quantityTotal += self.quantityLoad3
                            self.weightTotal += self.weightLoad3
                            if(HT[2].dateOut > self.dateOut):
                                self.dateOut = HT[2].dateOut
                        except:
                            print("Error in load 3")
                            a = 4
                        try:
                            self.weightLoad4 = HT[3].weightLot
                            self.soakTempLoad4 = HT[3].tempSetPoint
                            self.soakTimeStartLoad4 = HT[3].soakTimeStart
                            self.soakTimeEndLoad4 = HT[3].timeOut
                            self.SoakTimeLoad4 = HT[3].soakTime
    #                        self.quenchMethodLoad4 = HT[3].quenchMethod
                            self.quantityLoad4 = HT[3].quantityLot
                            
                            self.quantityTotal += self.quantityLoad4
                            self.weightTotal += self.weightLoad4
                            
                            if(HT[3].dateOut > self.dateOut):
                                self.dateOut = HT[3].dateOut
                            
                        except:
                            print("Error in load 4")
                            a = 1
                        try:
                            self.weightLoad5 = HT[4].weightLot
                            self.soakTempLoad5 = HT[4].tempSetPoint
                            self.soakTimeStartLoad5 = HT[4].soakTimeStart
                            self.soakTimeEndLoad5 = HT[4].timeOut
                            self.SoakTimeLoad5 = HT[4].soakTime
    #                        self.quenchMethodLoad5 = HT[4].quenchMethod
                            self.quantityLoad5 = HT[4].quantityLot
                            
                            self.quantityTotal += self.quantityLoad5
                            self.weightTotal += self.weightLoad5
                            
                            if(HT[4].dateOut > self.dateOut):
                                self.dateOut = HT[4].dateOut
                            
                        except:
                            print("Error in load 5")
                            b = 2  
                            
                        try:
                            self.weightLoad6 = HT[5].weightLot
                            self.soakTempLoad6 = HT[5].tempSetPoint
                            self.soakTimeStartLoad6 = HT[5].soakTimeStart
                            self.soakTimeEndLoad6 = HT[5].timeOut
                            self.SoakTimeLoad6 = HT[5].soakTime
    #                        self.quenchMethodLoad6 = HT[5].quenchMethod
                            self.quantityLoad6 = HT[5].quantityLot
                            
                            self.quantityTotal += self.quantityLoad6
                            self.weightTotal += self.weightLoad6
                            
                            if(HT[5].dateOut > self.dateOut):
                                self.dateOut = HT[5].dateOut                        
                            
                        except:
                            print("Error in load 6")
                            c = 2
                            
                        try:
                            self.weightLoad7 = HT[6].weightLot
                            self.soakTempLoad7 = HT[6].tempSetPoint
                            self.soakTimeStartLoad7 = HT[6].soakTimeStart
                            self.soakTimeEndLoad7 = HT[6].timeOut
                            self.SoakTimeLoad7 = HT[6].soakTime
    #                        self.quenchMethodLoad7 = HT[5].quenchMethod
                            self.quantityLoad7 = HT[6].quantityLot
                            
                            self.quantityTotal += self.quantityLoad7
                            self.weightTotal += self.weightLoad7
                            
                            if(HT[6].dateOut > self.dateOut):
                                self.dateOut = HT[6].dateOut                        
                            
                        except:
                            print("Error in load 7")
                            c = 2                        
                        try:
                            self.weightLoad8 = HT[7].weightLot
                            self.soakTempLoad8 = HT[7].tempSetPoint
                            self.soakTimeStartLoad8 = HT[7].soakTimeStart
                            self.soakTimeEndLoad8 = HT[7].timeOut
                            self.SoakTimeLoad8 = HT[7].soakTime
    #                        self.quenchMethodLoad8 = HT[5].quenchMethod
                            self.quantityLoad8 = HT[7].quantityLot
                            
                            self.quantityTotal += self.quantityLoad8
                            self.weightTotal += self.weightLoad8
                            
                            if(HT[7].dateOut > self.dateOut):
                                self.dateOut = HT[7].dateOut                        
                            
                        except:
                            print("Error in load 8")

                            c = 2 
                        try:
                            HTObject = HT[8]
                            self.weightLoad9 = HTObject.weightLot
                            self.soakTempLoad9 = HTObject.tempSetPoint
                            self.soakTimeStartLoad9 = HTObject.soakTimeStart
                            self.soakTimeEndLoad9 = HTObject.timeOut
                            self.SoakTimeLoad9 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad9 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad9
                            self.weightTotal += self.weightLoad9
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 9")
                            c = 2 
                        try:
                            HTObject = HT[9]
                            self.weightLoad10 = HTObject.weightLot
                            self.soakTempLoad10 = HTObject.tempSetPoint
                            self.soakTimeStartLoad10 = HTObject.soakTimeStart
                            self.soakTimeEndLoad10 = HTObject.timeOut
                            self.SoakTimeLoad10 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad10 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad10
                            self.weightTotal += self.weightLoad10
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 10")
                            c = 2 
                        try:
                            HTObject = HT[10]
                            self.weightLoad11 = HTObject.weightLot
                            self.soakTempLoad11 = HTObject.tempSetPoint
                            self.soakTimeStartLoad11 = HTObject.soakTimeStart
                            self.soakTimeEndLoad11 = HTObject.timeOut
                            self.SoakTimeLoad11 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad11 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad11
                            self.weightTotal += self.weightLoad11
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 11")
                            c = 2         
                        try:
                            HTObject = HT[11]
                            self.weightLoad12 = HTObject.weightLot
                            self.soakTempLoad12 = HTObject.tempSetPoint
                            self.soakTimeStartLoad12 = HTObject.soakTimeStart
                            self.soakTimeEndLoad12 = HTObject.timeOut
                            self.SoakTimeLoad12 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad12 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad12
                            self.weightTotal += self.weightLoad12
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 12")
                            c = 2  
                        try:
                            HTObject = HT[12]
                            self.weightLoad13 = HTObject.weightLot
                            self.soakTempLoad13 = HTObject.tempSetPoint
                            self.soakTimeStartLoad13 = HTObject.soakTimeStart
                            self.soakTimeEndLoad13 = HTObject.timeOut
                            self.SoakTimeLoad13 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad13 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad13
                            self.weightTotal += self.weightLoad13
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 13")
                            pass
                        try:
                            HTObject = HT[13]
                            self.weightLoad14 = HTObject.weightLot
                            self.soakTempLoad14 = HTObject.tempSetPoint
                            self.soakTimeStartLoad14 = HTObject.soakTimeStart
                            self.soakTimeEndLoad14 = HTObject.timeOut
                            self.SoakTimeLoad14 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad14 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad14
                            self.weightTotal += self.weightLoad14
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 14")
                            pass
                        try:
                            HTObject = HT[14]
                            self.weightLoad15 = HTObject.weightLot
                            self.soakTempLoad15 = HTObject.tempSetPoint
                            self.soakTimeStartLoad15 = HTObject.soakTimeStart
                            self.soakTimeEndLoad15 = HTObject.timeOut
                            self.SoakTimeLoad15 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad15 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad15
                            self.weightTotal += self.weightLoad15
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 15")
                            pass
                        try:
                            HTObject = HT[15]
                            self.weightLoad16 = HTObject.weightLot
                            self.soakTempLoad16 = HTObject.tempSetPoint
                            self.soakTimeStartLoad16 = HTObject.soakTimeStart
                            self.soakTimeEndLoad16 = HTObject.timeOut
                            self.SoakTimeLoad16 = HTObject.soakTime
    #                        self.quenchMethodLoad9 = HT[5].quenchMethod
                            self.quantityLoad16 = HTObject.quantityLot
                            
                            self.quantityTotal += self.quantityLoad16
                            self.weightTotal += self.weightLoad16
                            
                            if(HTObject.dateOut > self.dateOut):
                                self.dateOut = HTObject.dateOut                        
                            
                        except:
                            print("Error in load 16")
                            pass
                            
                    #After all certs have been created, update HeatTreat objects associated and set them to certCreated    
                    ##This triggers if orders is not None
                    for hto in orders:
#                        print("before: ", hto.certCreated)
                        hto.certCreated = True
#                        print("after: ", hto.certCreated)
                        HeatTreat.save(hto) #Call the HeatTreat save so the changes are saved!
                            
                            
                else:
                    raise NameError ("No associated TTPI exists")
            
            else:
                raise NameError("some error here")
#            self.certSaved = True
            self.overrideSafeguard = False
            super(PrintCert, self).save(*args, **kwargs)
        else:
            raise NameError("Work Order cert already exists.")
                
        
        
        
    def __str__(self):
        return self.workOrder


class Operators(models.Model):
    operatorName = models.CharField(blank = True, null = True, max_length = 100)
    operatorID = models.IntegerField()
    field1 = models.CharField(max_length = 100, blank = True, null = True) #Field shown in Access program
    field2 = models.CharField(max_length = 100, blank = True, null = True) #Field shown in Access program
    field3 = models.CharField(max_length = 100, blank = True, null = True) #Field shown in Access program
    field4 = models.CharField(max_length = 100, blank = True, null = True) #Field shown in Access program
    operatorInitials = models.CharField(max_length = 5, blank = True, null = True)
    userActive = models.BooleanField(default=True)
    canReviewTTPI = models.BooleanField(default=False)
    
    def save(self,*args, **kwargs):
        print("save method-------------------Operators-----")
        
        
        if self.operatorID and not self.operatorName:
            server = 'MSAVMFG1'
            database = 'VMLIVE'
#            database = 'MSA712'
            try:
                username = 'tastetf'
                password = 'Vi1234' 
                cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
                cursor = cnxn.cursor()  
            
            except:
                print("server connection error")    
        
            try:
                cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM EMPLOYEE WHERE ID = ? ",(self.operatorID,))
                EmpName = cursor.fetchone()
                
                name = str(str(EmpName[0])+"-"+str(EmpName[1]))
                
                self.operatorName = name
                
            except : 
                self.operatorName = self.operatorName
                
            cnxn.close()
        
        

        super(Operators, self).save(*args, **kwargs)
    def __str__(self):
        return self.operatorName
    
class Furnaces(models.Model):
    furnaceName = models.CharField(max_length = 50)
    furnaceDescription = models.CharField(max_length = 50, null = True)
    furnace1 = models.CharField(max_length = 100, blank = True, null = True) #Extra field
    furnace2 = models.CharField(max_length = 100, blank = True, null = True) #Extra field
    furnace3 = models.CharField(max_length = 100, blank = True, null = True) #Extra field
    furnace4 = models.CharField(max_length = 100, blank = True, null = True) #Extra field
    
    def __str__(self):
        return self.furnaceName
    
class PolarChoice(models.Model):
    yesNoChoice = models.CharField(max_length = 3)
    
    def __str__(self):
        return self.yesNoChoice
    
    
class MaterialList(models.Model):
    materialName = models.CharField(max_length = 100)
    solutionMaterial = models.NullBooleanField("Is this a solution treat material?", max_length = 100, blank = True, null = True, default= False)
    hardenMaterial = models.NullBooleanField("Is this a harden material?", max_length = 100, blank = True, null = True, default= False)
    temperMaterial = models.NullBooleanField("Is this a temper material?", max_length = 100, blank = True, null = True, default= False)
    ageMaterial = models.NullBooleanField("Is this an age material?", max_length = 100, blank = True, null = True, default= False)
    normalMaterial = models.NullBooleanField("Is this a normalize material?", max_length = 100, blank = True, null = True, default= False)
    annealMaterial = models.NullBooleanField("Is this an anneal material?", max_length = 100, blank = True, null = True, default= False)
    

    def save(self,*args, **kwargs):
        print("save method-------------------MaterialList-----")

        super(MaterialList, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.materialName
    
from django.db import models
import pyodbc


# Create your models here.


class AcidClean(models.Model):
    ## All main properties of Solution Treat Orders table
    workOrder = models.CharField(max_length=50)
    partNumber = models.CharField(max_length=100)
    customer = models.CharField(max_length=50)
    rev = models.CharField(max_length=10)
    PO = models.CharField(max_length=100)
    VF1Cap = models.BooleanField(default=False)
    VF1Cap = models.BooleanField(default=False)
    TMQ1Cap = models.BooleanField(default=False)
    TMQ2Cap = models.BooleanField(default=False)
    TMQ3Cap = models.BooleanField(default=False)

    heatNumber = models.CharField(max_length=20)
    WOop = models.IntegerField(blank=True)
    coupons = models.BooleanField(default=True)
    visInspComplete = models.BooleanField(default=False)


    ##Below are not strictly required
    numPans = models.PositiveSmallIntegerField(blank=True)  ## 0 to 32767
    quantityLot = models.PositiveSmallIntegerField(blank=True)
    weightLot = models.PositiveIntegerField(blank=True)
    dateTimeIn = models.DateTimeField(blank=True)
    furnaceNo = models.CharField(max_length=50, blank=True)
    operatorIn = models.CharField(max_length=50, blank=True)
    preHeatStart = models.TimeField(blank=True)
    preHeatEnd = models.TimeField(blank=True)
    soakTimeStart = models.TimeField(blank=True)
    soakTimeEnd = models.TimeField(blank=True)
    dateTimeOut = models.DateTimeField(blank=True)
    operatorOut = models.CharField(max_length=50, blank=True)
    cleaningReq = models.BooleanField(default=True)

    tempSetPointLow = models.PositiveSmallIntegerField(blank=True)
    tempSetPointHigh = models.PositiveSmallIntegerField(blank=True)
    tempSetPoint = models.PositiveSmallIntegerField(blank=True)
    uniformityTol = models.PositiveSmallIntegerField(blank=True)
    soakTime = models.PositiveSmallIntegerField(blank=True)
    soakTimeMinusTol = models.PositiveSmallIntegerField(blank=True)
    soakTimePlusTol = models.PositiveSmallIntegerField(blank=True)
    VFVacPressure = models.PositiveSmallIntegerField(blank=True)
    partialPressure = models.BooleanField(default=False)
    TMQHeatEnv = models.PositiveSmallIntegerField(blank=True)
    TMQTenPurge = models.BooleanField(blank=True)
    channelOne = models.IntegerField(blank=True)
    channelTwo = models.IntegerField(blank=True)
    quenchMethod = models.CharField(max_length=50, blank=True)
    agitReq = models.BooleanField(blank=True)
    tempBeforeQuench = models.PositiveSmallIntegerField(blank=True)
    tempAfterQuench = models.PositiveSmallIntegerField(blank=True)
    WQuenchDelay = models.PositiveSmallIntegerField(blank=True)  ## W = Titanium

    partsCleaned = models.BooleanField(blank=True)
    goodCond = models.BooleanField(blank=True)
    PWAMCL = models.BooleanField(blank=True)
    PWABatchControl = models.BooleanField(blank=True)
    genBy = models.CharField(max_length=50, blank=True)
    genDate = models.DateField(blank=True)
    reviewBy = models.CharField(max_length=50, blank=True)
    reviewDate = models.DateField(blank=True)

    ##spec prefixes all appear to be from Solution Treat Specs table as well, but duplicated on Solution Treat Orders
    specNumber = models.CharField(max_length=50, blank=True)
    specRevision = models.CharField(max_length=50, blank=True)
    specMaterial = models.CharField(max_length=50, blank=True)
    specMaterialSpec = models.CharField(max_length=50, blank=True)
    specMaterialSpecRevision = models.CharField(max_length=50, blank=True)
    specVF1 = models.BooleanField(blank=True)
    specVF2 = models.BooleanField(blank=True)
    specTMQ1 = models.BooleanField(blank=True)
    specTMQ2 = models.BooleanField(blank=True)
    specTMQ3 = models.BooleanField(blank=True)
    specCleaning = models.BooleanField(blank=True)
    specTempSetPointLow = models.PositiveSmallIntegerField(blank=True)
    specTempSetPointHigh = models.PositiveSmallIntegerField(blank=True)
    specUniformityTol = models.PositiveSmallIntegerField(blank=True)
    specSoakTime = models.PositiveSmallIntegerField(blank=True)
    specSoakMinusTimeTol = models.PositiveSmallIntegerField(blank=True)
    specSoakPosTimeTol = models.PositiveSmallIntegerField(blank=True)
    specVFVacPressure = models.PositiveSmallIntegerField(blank=True)
    specTMQHeatLow = models.PositiveSmallIntegerField(blank=True)
    specTMQHeatHigh = models.PositiveSmallIntegerField(blank=True)
    specLoadTC = models.CharField(max_length=50, blank=True)
    specQuenchGFC = models.BooleanField(blank=True)
    specQuenchOil = models.BooleanField(blank=True)
    specQuenchWater = models.BooleanField(blank=True)
    specQuenchAir = models.BooleanField(blank=True)
    specTempBeforeQuenchLow = models.IntegerField(blank=True)
    specTempBeforeQuenchHigh = models.IntegerField(blank=True)
    specTempAfterQuenchMax = models.PositiveSmallIntegerField(blank=True)
    specTitaniumQuenchDelayMax = models.PositiveSmallIntegerField(blank=True)
    specPartsCleanedAfterQuench = models.CharField(max_length=50, blank=True)  ##cannot use Boolean
    specMasterReviewed = models.CharField(max_length=50, blank=True)
    specMasterApproved = models.CharField(max_length=50, blank=True)
    specFormRevision = models.PositiveSmallIntegerField(blank=True)
    specFormRevDate = models.DateField(blank=True)



    def save(self,*args, **kwargs):
        print("save method------------------------")
        if self.workOrder:
            print("------------------------------------------------------------Entering save method")
            conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=C:\Users\stefflc\Desktop\HeatTreat - Moreno Project.accdb;'
            )
            cnxn = pyodbc.connect(conn_str)
            crsr = cnxn.cursor()
            for table_info in crsr.tables(tableType='TABLE'):
                print(table_info.table_name)

            return

        cnxn.close()
        super(AcidClean, self).save(*args, **kwargs)




    def __str__(self):
        return self.workOrder

    def testOutput():
        print("We're in the models.py file")


        return
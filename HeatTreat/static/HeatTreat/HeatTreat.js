//Add CSRF protection 2/25/19

//3-13-19 Lots of updates to onload functions - 
// Localize on load to a specific function by class. This shoudl remove catch(e) requirements.

//Add  stuff for ManageTTPI

//3/27/19
//Fixed soak end /add duration when adding exactly 60 minutes (added <= instead of <)
//Added abillity for date in/ date out to accept and convert 03/26/19 to 2019-03-26 for example
//updateFurnace will now set data.channelOne and channelTwo per list from DAniel Moreno

//3/28/19
//Remove uniformity tolerance from sendemail function, it is not a variable.

//3/28/19, another update
// Add filterOperator for manage TTPI page

//0401/19
// Add additional sendemail checks per DAniel Moreno request

//04_03_19
// Add function(catch(e)) to posttreats function to catch errors thrown by the Django model
// Also updated django model to check for duplicates and reject save if AddTTPI is used when there is already ane existing TTPI
//I.E. CreateTTPI goes to django save which checks for duplicates. If dupes, save method raises NameError which postTreats catchs and displays in alert
       
//04_24_19 - added considerable error checking to sendEmail function  

//08/07/19 - add new null logic to VFVacSpec such that a value can now be erased.
//Specifically if you entered 50 microns then erased and typed in 50CFH for heating environment you would get an error because 50 microns was not null.     

//09/09/19 - add logic for approving specs

//09/19/19 - add approval logic to require that postItNote data is null or blank

//09/25/19 - Add support for work orders like "TEST-BOLT/110" which have no customer PO; internal only

//09/27/19 - Add support for blank stock orders
// Blank stock part numbers all start with "BLK"
// Blank stock customers should all start with "For blank" - could be "For blank stock" "For blank order"...

//10/23/19 - Update Thermocouples - Switch VF# to TMQ# - TMQ#s required 2x thermocouples not VF1/2 funaces

//11/18/19 - on addSoakDur - add logic to check soakTimePref variable. This is preferred time set by management.
// If it is present, use preferred time to calculate soak end time rather than the soaktime from the spec.

 $(document).ready(function(){
 

    
    $(function(){
        //console.log("stuff 2");
      if( $("div").hasClass("OnLoadEditTTPI") ){
          //console.log("stuff3");
     
        try{
            document.getElementById("filterWOID").value = localStorage.getItem("passDataWO");
            angular.element(document.getElementById("filterWOID")).triggerHandler('change');
        }
        catch(e){
            console.log(e);
        }
      }

      if( $("div").hasClass("OnLoadOperatorTTPI") ){
          //console.log("stuff3");
     
        try{
            document.getElementById("filterWOID").value = localStorage.getItem("passDataWO");
            angular.element(document.getElementById("filterWOID")).triggerHandler('change');
            
            
            document.getElementById("filterLoadID").value = localStorage.getItem("passDataLoadNum");
            angular.element(document.getElementById("filterLoadID")).triggerHandler('change');            
        }
        catch(e){
            console.log(e);
        }
      }      
      
      
      
      
      if($("div").hasClass("OnLoadSolutionTreatSpec") ){
          try{
            document.getElementById("specInput").value = localStorage.getItem("passSpecNumber");
    
            document.getElementById("specRevInput").value = localStorage.getItem("passSpecRev")
    
            document.getElementById("specMatInput").value = localStorage.getItem("passSpecMat")
    
            document.getElementById("specMaterialSpecInput").value = localStorage.getItem("passSpecMatSpec")
    
            document.getElementById("specMaterialSpecRevInput").value = localStorage.getItem("passSpecMatSpecRev")
            
            document.getElementById("specFormRevInput").value = localStorage.getItem("passSpecFormRev")
    
    
            angular.element(document.getElementById("specInput")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            angular.element(document.getElementById("specRevInput")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            angular.element(document.getElementById("specMatInput")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            angular.element(document.getElementById("specMaterialSpecInput")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            angular.element(document.getElementById("specMaterialSpecRevInput")).triggerHandler('change'); //Calls ng-change, which then calls update() function
            angular.element(document.getElementById("specFormRevInput")).triggerHandler('change'); //Calls ng-change, which then calls update() function

        }
        catch(e){
            console.log(e);
        }
      
      
      }
      if($("div").hasClass("OnLoadCertPrinter") ){
        try{
            //CertPrinter page
            document.getElementById("filterPrintWorkorder").value = localStorage.getItem("passPrintWorkOrder");
            angular.element(document.getElementById("filterPrintWorkorder")).triggerHandler('change');
         }
        catch(e){
            console.log(e);
        }
      }
      
    });


});
 

function getTodayDate(){
     var n =  new Date();
var y = n.getFullYear();
var m = n.getMonth() + 1;
var d = n.getDate() ;
    
m = '00' + m;
m = m.slice(-2);

d = '00'+d
d = d.slice(-2)
var todayDate = (y + "-" + m + "-" + d);

return todayDate;
 }
 
          




(function(){
    'use strict';

    angular.module('HT.HeatTreat',[] )
        .controller('HeatTreatController',
            [ '$scope' , '$http', HeatTreatController]).run(['$http', run]);
            // the .run(['$http', run]) is needed for CSRF protection for forbidden 403 error, see end of JS

    function HeatTreatController($scope, $http) {


        $scope.HTdata =[];
        var q
        $http.get('/HeatTreat/treats/').then(function(response){
            $scope.HTdata = response.data;
            $scope.workorder = response.data.workOrder;
        });
        
        $scope.specdata = [];
        $http.get('/HeatTreat/solutiontreatspecs/').then(function(response){
            $scope.specdata = response.data;
        });

        //$scope.filterWO = "18-1624/1.0"
        //$scope.filterSpecNumber = "PWA";
        //Default filter so all WO don't show automatically

        $scope.Operatordata = [];
        $http.get('/HeatTreat/operators/').then(function(response){
            $scope.Operatordata = response.data;
        }); 
        
        $scope.furnacedata = [];
        
        $http.get('/HeatTreat/furnaces/').then(function(response){
            $scope.furnacedata = response.data;
        });
        
        $scope.materialdata = [];
        $http.get('/HeatTreat/materials/').then(function(response){
            $scope.materialdata = response.data;
        }); 
        
        $scope.polardata = [];
        $http.get('/HeatTreat/polarchoice/').then(function(response){
            $scope.polardata = response.data;
        });
        
        $scope.certdata = [];
        $http.get('/HeatTreat/printcert/').then(function(response){
            $scope.certdata = response.data;
        
        
        });
        
        $scope.needcertdata = [];
        $http.get('/HeatTreat/nocert/').then(function(response){
            $scope.needcertdata = response.data;
        
        });
        
        $scope.pendingjobdata = [];
        $http.get('/HeatTreat/pendingjobs/').then(function(response){
            $scope.pendingjobdata = response.data;
        
        });    
        
        $scope.unrevieweddata = [];
        
        $http.get('/HeatTreat/unreviewedTTPI/').then(function(response){
            $scope.unrevieweddata = response.data;
        
        });
        
        
        $scope.editTTPIdata = [];
        $http.get('/HeatTreat/editTTPIdata/').then(function(response){
            $scope.editTTPIdata = response.data;
        
        });           
        
            
    $scope.putTreatSpecs = function(spec){
        if(spec.specLocked){
            alert("This Specification is locked.");
        
        }
        else{
            var url = '/HeatTreat/solutiontreatspecs/' + spec.id + '/';
            return (
                $http.put(
            			url,
            			spec
            	)
            )
        } 
    }
    
    //This is for use with $scope.increaseSpecFormRev function
    //The original putTreatSpecs has "specLocked" trigger which will cause copy to fail.
    $scope.copyPutTreatSpecs = function(spec){

        
        var url = '/HeatTreat/solutiontreatspecs/' + spec.id + '/';
        
        //Make sure to lift the specLocked so the new form revision can be edited
        spec.specLocked = false;
        
        return (
            $http.put(
        			url,
        			spec
        	)
        )
        
    }    
        
    $scope.addSoakDur = function(data, spec){
            //console.log("entering addsoak");
            //console.log(data.soakTimeStart);
            console.log("data.soaktimepref: ", data.soakTimePref);

            var time = data.soakTimeStart;
            var soakDuration;
            if(data.overrideSoakTime){
                soakDuration = data.overrideSoakTime;
            }
            else if (data.soakTimePref){
                soakDuration = data.soakTimePref;
            }
            else{
                soakDuration = spec.specSoakTime;
            }
            console.log("soakduration: ", soakDuration)
            //var soakDuration = spec.specSoakTime;
            
            console.log(data.soakTime);
            console.log(typeof time);
            var splitcolon = time.split(":");
            
            if(splitcolon[2] == null){
                splitcolon[2] = "00";
            }
            
           // console.log(splitcolon)
            splitcolon[0] = parseInt(splitcolon[0]);
            splitcolon[1] = parseInt(splitcolon[1]);
            splitcolon[2] = parseInt(splitcolon[2]);
            
            splitcolon[1] = splitcolon[1] + soakDuration
            //console.log(splitcolon)
            while(splitcolon[1] >= 60){
                splitcolon[0] = splitcolon[0] + 1;
                if(splitcolon[0] >23){
                splitcolon[0] = splitcolon[0] - 24}
                
                splitcolon[1] = splitcolon[1] - 60;
                
                
            //console.log(splitcolon);
            }; 
            
            var h = splitcolon[0];
            var m = splitcolon[1];
            var s = splitcolon[2];
            
            var hh = '00'+h
            var mm = '00'+m
            var ss = '00'+s
            
            hh = hh.slice(-2)
            mm = mm.slice(-2)
            ss = ss.slice(-2)
            
            data.soakTimeEnd =  (hh +":" + mm + ":" + ss);
            $scope.putTreats(data);

        };
        
        //Send e-mail should employ user error checking
        $scope.sendEmail = function(data, spec){
            console.log("data.quenchMethod: ", data.quenchMethod);
            var canEmail = false;
            
            
            
            if(data.partNumber == 'PN ERROR'|| !data.partNumber){
                alert("Part number error. Contact management.");    
            }
            else if(data.customer == "CUSTOMER ERROR" || !data.customer || data.customer.indexOf("|") != -1){
                alert("CUSTOMER ERROR. Contact management.");    
            }
            else if(data.PO == "PO ERROR" || !data.PO || data.PO.indexOf("|") != -1 ){
                alert("PO Error. Contact management.");
            }
            else if (data.heatNumber == "HEAT ERROR" || !data.heatNumber){
                alert("Heat # error. Contact management.");
            }
            else if (data.WOop == 999 || data.WOop == '999' || !data.WOop ){
                alert("data.WOop error. Contact management.");
            }
            else if (data.coupons && !data.couponInit){
                alert("Coupons required, but initials missing");
            }
            else if(!data.numPans){
                alert("Error with number of pans");
            }
            else if(!data.quantityLot){
                alert("Error with quantity of lot.");
            }
            else if(!data.weightLot){
                alert("Error with weight of lot.");
            }
            else if(!data.dateIn || data.dateIn == '1900-01-01' || data.dateIn == '1900-01-00'){
                alert("Error with date in.");
            }  
            else if(!data.furnaceNo){
                alert("Error with furnace number selection.");
            }            
            else if(!data.operatorIn){
                alert("Error with operator in selection.");
            } 
            else if(!data.timeIn){
                alert("Error with time in selection.");
            }   
            else if(!data.soakTimeStart){
                alert("Error with soak time start.");
            }
            else if(!data.soakTimeEnd){
                alert("Error with soak time end.");
            }
                         
            else if(!data.dateOut || data.dateIn == '1900-01-01' || data.dateIn == '1900-01-00'){
                alert("Error with date out.");
            }
            else if(!data.timeOut){
                alert("Error with time out.");
            }              
            else if(!data.operatorOut){
                alert("Error with operator out.");
            }
            else if (!data.tempSetPoint){
                alert("Error with temperature set point.");
            }
            else if (!data.channelOne){
                alert("Channel 1 thermocouple is missing. Please re-select Furnace No box to fix the issue." );
                
                }
            else if (!data.channelTwo && (data.furnaceNo == 'TMQ1' || data.furnaceNo == 'TMQ2' || data.furnaceNo == 'TMQ3')){
                alert("Vaccum Furnaces required 2 load thermocouple channels to be entered.")

            }
            else if (!data.goodCond){
                alert("Parts must be in good condition. Please select box at bottom of form.");
            
            }
            //Check soak time +/- tolerances from 
            else if(data.soakTimePlusTol > spec.specSoakPosTimeTol && !data.overrideSoakTimePlusTol){
                alert("Soak Time + Tolerance exceeds specification allowance");
            }
            else if (data.soakTimePlusTol > data.overrideSoakTimePlusTol && data.overrideSoakTimePlusTol){
                alert("Soak Time + Tolerance exceeds specification (override) tolerance");
            }
            else if (data.soakTimeMinusTol > spec.specSoakMinusTimeTol){
                alert("Soak Time - Tolerance is under specification alloance");
            }
 
  

    
              
            else if(!data.quenchMethod || data.quenchMethod == " " ){
                alert("Please select a quench method");
            }
            else if( (data.quenchMethod == 'Oil' || data.quenchMethod == 'OIL' || data.quenchMethod == 'Water') && !data.tempBeforeQuench){
                alert("Temp Before quench required for Oil or Water quench method.");
            
            }
            else if( (data.quenchMethod == 'Oil' || data.quenchMethod == 'OIL' || data.quenchMethod == 'Water') && !data.tempAfterQuench){
                alert("Temp after quench required for Oil or Water quench method.");
            
            }            
            else if( (data.quenchMethod == 'Oil' || data.quenchMethod == 'OIL') && (data.partsCleaned != 'Yes' && data.partsCleaned != 'YES') ){
                alert("If quench method is oil, parts must be alkaline cleaned.");
            
            }
            else if( (data.quenchMethod == 'Oil' || data.quenchMethod == 'OIL' || data.quenchMethod == 'Water' || data.quenchMethod == 'WATER' ) && 
                    !data.agitReq){
                    alert("If quench method is Oil or Water then agitation is required.");
                    
                    }
            else if( (data.furnaceNo == 'TMQ1' || data.furnaceNo == 'TMQ2' || data.furnaceNo == 'TMQ3') && !data.TMQTenPurge){
                alert("If furnace selected is TMQ1, TMQ2, or TMQ3 then 10 Minute Purge is required.");
            
            }
            else if( (data.furnaceNo == 'TMQ1' || data.furnaceNo == 'TMQ2' || data.furnaceNo == 'TMQ3') && !data.TMQHeatEnv){
                alert("If furnace selected is TMQ1, TMQ2, or TMQ3 then TMQ Heating Environment CFH is required.");

            }

            else if ( ( data.furnaceNo == 'VF1' || data.furnaceNo == 'VF2') && !data.VFVacPressure ){ //UpdateVFVacPressure checks if the pressure is correct, this just verifies if vac pressure is truthy
                alert("If furnace selected is VF1 or VF2, then VF Vacuum Pressure is required.");
            
            }
            else if (!data.partsCleaned ){
                alert("Please select Yes/No for Parts alkaline cleaned after Quench");
            }
            
            
            else{
                data.operatorDone = true;
                $scope.putTreats(data);
                
            }
            
       
 
           
            if(data.operatorDone){
                //var workorder = data.workOrder;
                //var operIn = data.operatorIn;
                
               // var emailSubject = "Work Order: " +workorder +" complete.";
               // var emailBody = "Work Order: " +workorder +"\n"+" Operator In: " + operIn;
                
                //window.open('mailto:stefflc@msaerospace.com?subject='+emailSubject+'&body='+emailBody);
               // window.location.href='mailto:morenod@msaerospace.com?subject='+emailSubject+'&body='+emailBody;
                alert("Information is correct. Information will be logged for management. Thanks.");
            }        

        
        }
    
        $scope.convertToDate = function(string){
            console.log(string);
        }

        	
    	$scope.update = function (data) {
        	if(data.dateIn ){ //Check to see if it's not null
        	
        	if(data.dateIn.includes("/")){
            	console.log("string includes / ");
            	
            	var dateArray = data.dateIn.split("/");
            	console.log(dateArray);
            	var month = dateArray[0];
            	var day = dateArray[1];
            	var year = dateArray[2];
            	if(month.length ==1){
            	month = "0" + month;
            	}
            	if(year.length == 2){
            	year = "20"+year;
            	
            	}
            	console.log("mdy: ", month, day, year);
            	data.dateIn = year+"-"+month+"-"+day;
            	
        	
        	}
        	}
        	if(data.dateOut){
	       if(data.dateOut.includes("/")){
            	console.log("string includes / ");
            	
            	var dateArray = data.dateOut.split("/");
            	console.log(dateArray);
            	var month = dateArray[0];
            	var day = dateArray[1];
            	var year = dateArray[2];
            	if(month.length ==1){
            	month = "0" + month;
            	}
            	if(year.length == 2){
            	year = "20"+year;
            	
            	}
            	console.log("mdy: ", month, day, year);
            	data.dateOut = year+"-"+month+"-"+day;
            	
        	
        	}
        	}
        	
    	
    	
    	
        	$scope.putTreats(data);
    	
    	};
    	
    	$scope.updateSpec = function (spec) {
        	console.log("bbbbbb: " + spec.specCleaning);
        	console.log(spec);
        	
        	if(spec.VFPHTSetPointLow == ""){
            	spec.VFPHTSetPointLow = null;
        	
        	}
        	if(spec.VFPHTSetPointHigh == ""){
            	spec.VFPHTSetPointHigh = null;
        	
        	}        	
        	if(spec.VFSoak == ""){
            	spec.VFSoak = null;
        	
        	}        	
        	if(spec.VFMinusTimeTol == ""){
            	spec.VFMinusTimeTol = null;
        	
        	}
        	if(spec.VFPlusTimeTol == ""){
            	spec.VFPlusTimeTol = null;
        	
        	}
        if(spec.specTMQHeatLow == ""){
            spec.specTMQHeatLow = null;
            }
        if(spec.specTMQHeatHigh == ""){
            spec.specTMQHeatHigh = null;
            }  
        	if(spec.specTempBeforeQuenchLow == ""){
            spec.specTempBeforeQuenchLow = null;
            }
        if(spec.specTempBeforeQuenchHigh == ""){
            spec.specTempBeforeQuenchHigh = null;
            } 
            if(spec.specTempAfterQuenchMax == ""){
            spec.specTempAfterQuenchMax = null;
            }
        if(spec.specTMQ1 || spec.specTMQ2 || spec.specTMQ3){
            spec.specLoadTC = "Yes (X2 for TMQ'S)";
        
        }
        if(!spec.specTMQ1 && !spec.specTMQ2 && !spec.specTMQ3){
            spec.specLoadTC = "Yes";
        } 
    	
        	        	
            
               $scope.putTreatSpecs(spec)
               .then(function(response){
            		console.log("Spec updated");
        		
        		})
        		.catch(function(e){
        		console.log("error: ", e);
        		alert("Data entered is invalid.");
        		})	
    	};  
	
    	
    	
    	$scope.updateOperatorList = function(operatorData){
       var url = '/HeatTreat/operators/' + operatorData.id + '/';

        	console.log(operatorData.operatorName);
        	if(operatorData.operatorName == ""){
            	console.log("true");
            	
            	$http.delete(
            	url,
            	operatorData
            	);
    
        	}
        	else{
            	$http.put(
            	url,
            	operatorData
            	);
        	}
        location.reload();   //Refresh the html page 	

    	};
    	
    	$scope.updateDataWithSpec = function(data, spec){
        	console.log("data: ", data);
        	//console.log("spec: ", spec);
        	console.log("data.specnumber: ", data.specNumber);
        	//console.log("spec.specNumber: ", spec.specNumber);
        	
        	$scope.putTreats(data);
    	
    	
    	}
    	
    		$scope.updateSoakStart = function(data){
        	//var time = new datetime.now();
        	var time = data.soakTimeStart;
        	
        	//var time = new Date(data.dateIn+"T"+data.soakTimeStart+"Z" )
        	console.log(time);
        	var splitcolon = time.split(":");
            
            if(splitcolon[2] == null){
                splitcolon[2] = "00";
            }
            
            console.log(splitcolon)
	         var h = splitcolon[0];
            var m = splitcolon[1];
            var s = splitcolon[2];
            
            var hh = '00'+h;
            var mm = '00'+m;
            var ss = '00'+s;
            
            hh = hh.slice(-2);
            mm = mm.slice(-2);
            ss = ss.slice(-2);
            
            data.soakTimeStart =  (hh +":" + mm + ":" + ss);
            	console.log(data.soakTimeStart)
            	
            	//do POST
            	$scope.putTreats(data);
            	
     
    	}

    $scope.updateTMQHeatEnv = function(data, spec){
    
        if(data.TMQHeatEnv < spec.specTMQHeatLow){
            alert(data.TMQHeatEnv +"<"+ spec.specTMQHeatLow);
        
        }
        else if (data.TMQHeatEnv > spec.specTMQHeatHigh){
            alert(data.TMQHeatEnv +">" + spec.specTMQHeatHigh);
        
        }
        else{
            $scope.putTreats(data);
        
        }
        
    
    };

    	
    	$scope.updateTimeIn = function(data){

            //This variable does not appear to be necessary to anything else in the model
            if(data.dateIn == "" || data.dateIn == null){
                alert("Please enter Date In");
            }
            else{
                data.dateTimeIn = new Date(data.dateIn+"T"+data.timeIn+"Z");

            }
        	
        	if(data.timeIn =="" || data.timeIn == null){
            	alert("Time in is blank");
            	
        	
        	}
        	else{
            	
    	       var time = data.timeIn;
            	console.log(time);
            	
	           var splitcolon = time.split(":");
                if(splitcolon[1] == null){
                    alert("Please ensure time is in format HH:MM ");

                }         	
                else{
                    if(splitcolon[2] == null){
                        splitcolon[2] = "00";
                    }
                
                console.log(splitcolon)
                //Change for date crossover
                if(data.dateIn != data.dateOut){
                    if(data.dateIn > data.dateOut){
                        alert("Date in before date out!");
                    }
                    else{
                    
                    }
                }
    	         var h = splitcolon[0];
                var m = splitcolon[1];
                var s = splitcolon[2];
                
                var hh = '00'+h;
                var mm = '00'+m;
                var ss = '00'+s;
                
                hh = hh.slice(-2);
                mm = mm.slice(-2);
                ss = ss.slice(-2);
                
                data.timeIn =  (hh +":" + mm + ":" + ss);
                	console.log(data.timeIn)
                	
                	$scope.putTreats(data);
                }
                
        	}
    	

    	};
    	$scope.updateTimeOut2 = function(data, spec){
    	
        	//In case there is an error from previous time - reset to 0.
        	//The model will re-calculate soakTime
        	if(data.soakTime <0){
            	data.soakTime = 0;
        	}
        		       var time = data.timeOut;
        	console.log(time);
        	var splitcolon = time.split(":");
            
            if(splitcolon[2] == null){
                splitcolon[2] = "00";
            }
            if(splitcolon[1] == null){
                splitcolon[1] = '00';
            }
            
            console.log(splitcolon)
	         var h = splitcolon[0];
            var m = splitcolon[1];
            var s = splitcolon[2];
            
            var hh = '00'+h;
            var mm = '00'+m;
            var ss = '00'+s;
            
            hh = hh.slice(-2);
            mm = mm.slice(-2);
            ss = ss.slice(-2);
            
            data.timeOut =  (hh +":" + mm + ":" + ss);
            	console.log(data.timeOut)
            	
            	
	         $scope.putTreatsThenCatch(data)
                .then(function(response){
                    data.soakTime = response.data.soakTime;
                    console.log("data.soakTime: ", data.soakTime);  
                    data.soakTimeMinusTol = response.data.soakTimeMinusTol;
                    console.log("data.soakTimeMinusTol: ", data.soakTimeMinusTol)
                    
                    data.soakTimePlusTol = response.data.soakTimePlusTol; 
                    console.log("data.soakTimePlusTol: ", data.soakTimePlusTol)
                    var specPosTime;
                    ///If 6-4 titanium or similar like RPS12.01, use override time as spec and spec+tolerancer and by thickness and not static
                    if(response.data.overrideSoakTimePlusTol){
                        specPosTime = response.data.overrideSoakTimePlusTol;
                        console.log("A specPosTime: ", specPosTime);
                    }              
                    else{
                        specPosTime = spec.specSoakPosTimeTol
                        console.log("B specPosTime: ", specPosTime);
                    }
                    
                    var overSoakTime;
                    if(response.data.overrideSoakTime){
                        overSoakTime = response.data.overrideSoakTime;
                        }
                    else{
                        overSoakTime = spec.specSoakTime;
                        }
                    
                    if (data.soakTime < (overSoakTime - spec.specSoakMinusTimeTol) ){
                        alert("You are -"+data.soakTimeMinusTol+" vs soak time. Spec allows -"+spec.specSoakMinusTimeTol);
                    }
                    else if (data.soakTime > (overSoakTime + specPosTime)){
                        console.log(data.soakTime, ">",overSoakTime," + ", specPosTime);
                        alert("You are +"+data.soakTimePlusTol+" vs soak time. Spec allows +"+specPosTime) ;     
                    }
                    else{
                        console.log("just right");  
                    }

                })
                .catch(function(e){
                    console.log("e: ", e);
                    if(e){
                        //var ErrorStuff = e.data.substr(0, e.data.indexOf('REQUEST'));
                        var edata = e.data;
                        //var ErrorStuff2 = edata.substr(10);
                        var ErrorStuff3 = e.data.substring(0, e.data.indexOf('Request'));
                        //console.log("ErrorSTuff: ", ErrorStuff2);
                        console.log("ErrorStuff: ", ErrorStuff3);
                        alert("Error: " + ErrorStuff3);                    
                    
                    
                    console.log("error: ", e.data);
                    }
                    else{
                        alert("updatetimeout2 failed.");

                    }
                })	
                

            	

    	angular.element(document.getElementById("soaktime1")).triggerHandler('change'); //Calls ng-change, which then calls update() function
    	}

    	
//    	$scope.updateTimeOut = function(data, spec){
//	       var time = data.timeOut;
//        	console.log(time);
//        	var splitcolon = time.split(":");
//            
//            if(splitcolon[2] == null){
//                splitcolon[2] = "00";
//            }
//            
//            console.log(splitcolon)
//	         var h = splitcolon[0];
//            var m = splitcolon[1];
//            var s = splitcolon[2];
//            
//            var hh = '00'+h;
//            var mm = '00'+m;
////            var ss = '00'+s;
////            
//            hh = hh.slice(-2);
//            mm = mm.slice(-2);
//            ss = ss.slice(-2);
//            
//            data.timeOut =  (hh +":" + mm + ":" + ss);
//            	console.log(data.timeOut)
//            	
//            var timeOutSeconds = hh*3600 + mm * 60 + ss*1;
//            	console.log(timeOutSeconds);
//            	
//            	
//            	time = data.soakTimeStart;
//            	console.log("time2: ", time)
//            	splitcolon = time.split(":");
//            	console.log("splitcolon2: ", splitcolon)
//            
//            if(splitcolon[2] == null){
//                splitcolon[2] = "00";
//            }
//            
//            console.log(splitcolon)
//	         var h = splitcolon[0];
//            var m = splitcolon[1];
//            var s = splitcolon[2];
//            
//            var hh = '00'+h;
//            var mm = '00'+m;
//            var ss = '00'+s;
//            
//            hh = hh.slice(-2);
//            mm = mm.slice(-2);
//            ss = ss.slice(-2);
//            
//            var soakTimeStartSeconds = hh*3600 + mm*60 + ss*1;
//            console.log(soakTimeStartSeconds);
//            var isNegative = false;
//            
//            var soakTimeSeconds = timeOutSeconds - soakTimeStartSeconds;
//            console.log(soakTimeSeconds);
//            
//            data.soakTime = (soakTimeSeconds)/ 60;
//            
//            console.log("soak"+spec.specSoakTime);
//            console.log("plus"+spec.specSoakPosTimeTol);
//            
//            if (data.soakTime < (spec.specSoakTime - spec.specSoakMinusTimeTol) ){
//                //console.log("too low");
//                data.soakTimeMinusTol = (spec.specSoakTime - data.soakTime);
//                data.soakTimePlusTol = 0;
//                alert("You are -"+data.soakTimeMinusTol+" vs soak time. Spec allows -"+spec.specSoakMinusTimeTol);
//                
//            }
//            
//            
//            else if (data.soakTime > (spec.specSoakTime + spec.specSoakPosTimeTol)){
//                //console.log("too high");  
//                data.soakTimePlusTol =( data.soakTime - spec.specSoakTime   );
//                data.soakTimeMinusTol = 0; 
//                alert("You are +"+data.soakTimePlusTol+" vs soak time. Spec allows +"+spec.specSoakPosTimeTol) ;     
//            
//            }
//            else{
//                console.log("just right");
//                if(data.soakTime > spec.specSoakTime){
//                    data.soakTimePlusTol = data.soakTime - spec.specSoakTime;
//                    data.soakTimeMinusTol = 0;
//                }
//                else if (data.soakTime < spec.specSoakTime){
//                    data.soakTimeMinusTol = spec.specSoakTime - data.soakTime;
//                    data.soakTimePlusTol = 0;
//                }
//                
//                
//            }
//            
//            
//            	
//            	//If it's negative, change to positive for the purposes of calculations
//            	if (soakTimeSeconds <= 0) {
////                	isNegative = true;
//                	soakTimeSeconds = soakTimeSeconds * -1;
//            	}
//            	
//            	var hour = 0;
//            	var minute = 0;
//            	var second = 0;
//            	while (Math.abs(soakTimeSeconds) >= 3600){
//
//            	
//            	
//                	console.log("hello");
//                	console.log(soakTimeSeconds);
//                	soakTimeSeconds -= 3600;
//                	hour = hour + 1;
//                	}
//            while (Math.abs(soakTimeSeconds) >= 60 && Math.abs(soakTimeSeconds) <3600){
//                soakTimeSeconds -= 60;
//                minute = minute +1;
//                }
//            //while (Math.abs(soakTimeSeconds) >0 && Math.abs(soakTimeSeconds) <60){ /////////////////////////////////////////broken here///// infinite loop?
//            second = Math.abs(soakTimeSeconds);
//               //}
//               
//             //If it was negative, change back to positive
////             if(isNegative){
//             
//                 hour = hour * -1;
//                 minute = minute *-1;
//                 second = second * -1;
//                 isNegative = false;
//             
//             }
//               
//               
////            console.log(hour+":"+minute+":"+second);
//            	
//            	
//
////       $scope.putTreatsCatch(data).catch(function(e){
//           console.log(e.data);
//            alert(data.timeOut + " is invalid! Make sure time is from 00:00 to 23:59.");
//            
//        })
//    	
//    	}
//    	
//    	$scope.updateTime = function(data){
//        	var theTime = document.getElementById("toast").value;
//        	console.log(theTime);
//        	data.timeIn = theTime;
//             $scope.putTreats(data);
//    	}
    	
    	$scope.increaseLoadFilter = function(){
        	var loadNumber = document.getElementById("filterLoad").value;
        	loadNumber += 1;
        	document.getElementById("filterLoad").value = loadNumber;
    	
    	}
    	
    	//Good example
    	// model has choices, if you do not PUT request one of the choices it thorws error
    	// This wil lcatch error and notify user ///////////////////////////////////////////////////////////////////////////////
    $scope.updateQuenchMethod = (function(data, spec){
    
  
    
        $scope.putTreatsCatch(data)
        .catch(function(){
            alert(data.quenchMethod + " is invalid!");
            
        })
    });
    
    $scope.toggleOilQuench = function(spec){
    
        if(spec.specQuenchOil){
            spec.specPartsCleanedAfterQuench = "Yes if Oil Quenched";
        
        
        }
        if(!spec.specQuenchOil){
            spec.specPartsCleanedAfterQuench = "No";
        }
    
    
    
    }

    
    

    	$scope.updateQuenchBefore = function(data, spec){
    	
        	if(data.tempBeforeQuench == null || data.tempBeforeQuench == ""){
            	//Do nothing, trigger nothing, wait until user enters value
        	
        	}
    	
        	else if(data.tempBeforeQuench < spec.specTempBeforeQuenchLow || data.tempBeforeQuench >spec.specTempBeforeQuenchHigh ){
            	alert(data.tempBeforeQuench + "°F must be between: " +spec.specTempBeforeQuenchLow + " - " +spec.specTempBeforeQuenchHigh + "°F" );
            	document.getElementById("tempBeforeQuenchBox").value = null;
        	
        	}
        	else{
            $scope.putTreatsCatch(data)
            		.catch(function(){
            		alert(data.tempBeforeQuench + "temp before Quench invalid");
            		})        	//put
        	}

    	}
    	
    	$scope.updateTitaniumDelay = function(data, spec){
        	if(data.WQuenchDelay == null || data.WQuenchDelay == ""){
            	//Do nothing, trigger nothing, wait until user enters value
        	
        	}
        	else if (data.WQuenchDelay > data.WQuenchDelaySpec){
            	alert("Titanium quench delay must be <= spec ");
            	document.getElementById("actualtitaniumquenchdelay").value = null;
        	}
        	else{
            $scope.putTreatsCatch(data)
            		.catch(function(){
            		alert(data.WQuenchDelay + "quench delay seconds appears to be invalid.");
            		}) 
          	}    	
    	
    	
    	}
    	
    	
    	  	
    	$scope.loadPage = function(){
        	console.log("load page");
    	
    	}
    	
    	$scope.updateOperatorIn = function(data, fred){
        	//console.log("help " + data.operatorIn);
        	//console.log("freddie " + fredoperatorName);
        	data.operatorIn = fred.operatorName;
        	//console.log("fish "+ data.operatorIn);
	       $scope.putTreats(data);
    	}
    	
    	$scope.updateTempAfterQuench = function(data, spec){
        	
        	
        	if(data.tempAfterQuench == null || data.tempAfterQuench == ""){
        	 // Do Nothing
        	
        	}
        // If the actual value is > the spec maximum after quench value, do not put the request
        	else if (data.tempAfterQuench > spec.specTempAfterQuenchMax){
            	alert(data.tempAfterQuench + "°F cannot exceed: " + spec.specTempAfterQuenchMax +"°F")
        	
            	document.getElementById("tempAfterQuenchBox").value = null;
        	}
        	else{        	
            $scope.putTreats(data);        	
        	}

    	}
    	$scope.updateVFVacPressure = function(data, spec){
	       if(data.VFVacPressure == null || data.VFVacPressure == ""){
        	 // Null is okay, but blank is not okay
        	 if(data.VFVacPressure == ""){
            	 data.VFVacPressure = null;
        	 }
        	 console.log("data: " + data.VFVacPressure);
        	 $scope.putTreats(data);
        	 
        	
        	}
        // If the actual value is > the spec maximum after quench value, do not put the request
        	else if (data.VFVacPressure > spec.specVFVacPressure){
            	alert(data.VFVacPressure + " microns cannot exceed: " + spec.specVFVacPressure +" microns.")
        	
            	document.getElementById("VFVacPressureBox").value = null;
        	}
        	else{        	
                $scope.putTreats(data);        	
        	}
    	}
    	
    	$scope.updateTempSetPoint = function(data, spec){
	       if(data.tempSetPoint == null || data.tempSetPoint == ""){
        	 // Do Nothing
        	
        	}
        // If the actual value is > the spec maximum after quench value, do not put the request
        	else if (data.tempSetPoint > spec.specTempSetPointHigh || data.tempSetPoint < spec.specTempSetPointLow ){
            	alert(data.tempSetPoint + " must be between: " + spec.specTempSetPointLow +" - " + spec.specTempSetPointHigh )
        	
            	document.getElementById("tempSetPointBox").value = null;
        	}
        	else{        	
            $scope.putTreats(data);        	
        	}
    	
    	
    	
    	}
    	
    	
    	
	   $scope.updateOperatorOut = function(data, bill){
        	console.log("help " + data.operatorOut);
        	console.log("freddie " + bill.operatorName);
        	data.operatorOut = bill.operatorName;
        	console.log("fish "+ data.operatorOut);
	       
	       $scope.putTreats(data);	
    	}
    	
    	$scope.updateFurnaceBox = function(data, spec, furnace){
	       
	       var furnaceName = furnace.furnaceName;
        	
        	if (furnaceName == 'VF1' ){
            	if(spec.specVF1){
                data.furnaceNo = 'VF1'
                data.channelOne = 1;
                data.channelTwo = null;
                $scope.putTreats(data);
            }
            else{
                alert("VF1 capability not available");
            }
        	}
        	else if (furnaceName == 'VF2'){
            	if(spec.specVF2){
                data.furnaceNo = 'VF2'
                data.channelOne = 1;
                data.channelTwo = null;
                $scope.putTreats(data);
            }
            else{
                alert("VF2 capability not available");
            }
        	}
         	else if (furnaceName == 'TMQ1'){
            	if(spec.specTMQ1){
                data.furnaceNo = 'TMQ1'
                data.channelOne = 3;
                data.channelTwo = 4;
                $scope.putTreats(data);
            }
            else{
                alert("TMQ1 capability not available");
            }
        	}
        	else if (furnaceName == 'TMQ2'){
            	if(spec.specTMQ2){
                data.furnaceNo = 'TMQ2'
                data.channelOne = 2;
                data.channelTwo = 4;
                $scope.putTreats(data);
            }
            else{
                alert("TMQ2 capability not available");
            }
        	}        	       	
        	else if (furnaceName == 'TMQ3'){
            	if(spec.specTMQ3){
                data.furnaceNo = 'TMQ3'
                data.channelOne = 14;
                data.channelTwo = 16;
                $scope.putTreats(data);
            }
            else{
                alert("TMQ3 capability not available");
            }
        	}        	
        	else{
            	console.log("silly string", data.furnaceName);
            	alert(data.furnaceName, "Furnace must be VF1, VF2, TMQ1, TMQ2, or TMQ3");
        	
        	
        	}

    	}
    $scope.emptyOrNull = function(item){
          return !(item.reviewBy === null || item.reviewBy.trim().length === 0)
    }


    $scope.addOperator = function(opName){
    
        var newOperator = {
            operatorName: opName  
        };
    
        $http.post('/HeatTreat/operators/', newOperator)
        .then(function(response){

        },
        function(){
            alert('Could not create Operator');
        });
        location.reload();   //Reload the web page to refresh data

    };
    
    $scope.addOperatorById = function(opID){
        
        if(opID.length == 4){
            var newOperator = {
                operatorID: opID  
            };    
        }
        else{
        alert("Operator ID must be 4 digits.");
        
        }
    

    
        $http.post('/HeatTreat/operators/', newOperator)
        .then(function(response){

        },
        function(){
            alert('Could not create Operator');
        });
        location.reload();   //Reload the web page to refresh data

    };
    
    
   // $scope.createCert = function(data){
    
     //   if(data.reviewBy == null || data.reviewBy == ""){
       //     alert("Please ensure TTPI is reviewed.");
//        }
//        else{
//            console.log(data.reviewBy);
        
        
//            console.log("Print Cert activated");
//            console.log("WO: ", data.workOrder);
//            var url = '/HeatTreat/printcert/';
 //           var newCert = {
//                workOrder : data.workOrder,
//            };
            
//            $http.post(url, newCert)
//            .then(function(response){
//                $scope.certsaved = response.data.certSaved;
//                alert("Cert Created. Please 'Open Printer'");
            
//            },
//            function(){
//                alert('Could not create Cert.');
//            });
            
//            };
            
//    };
    $scope.createCert = function(data){
    
        if(data.reviewBy == null || data.reviewBy == ""){
            alert("Please ensure TTPI is reviewed.");
        }
        else{
            console.log(data.reviewBy);
        
        
            console.log("Print Cert activated");
            console.log("WO: ", data.workOrder);
            var url = '/HeatTreat/printcert/';
            var newCert = {
                workOrder : data.workOrder,
            };
            
            $http.post(url, newCert)
            .then(function(response){
                $scope.certsaved = response.data.certSaved;
                //alert("Cert Created. Please 'Open Printer'");
                
                $scope.openPrintCert(data.workOrder); // Only open upon success, otherwise show error message(s)
            
            })
            .catch(function(e){
                //console.log("status: ", e.status);
                //console.log("header: ", e.headers);
                //console.log("test2: ", e.data.also);
                //console.log("got an error in initial processing",e);
                //console.log("also:", e.data);
                
                //var ErrorStuff = e.data.substr(0, e.data.indexOf('REQUEST'));
                var edata = e.data;
                //var ErrorStuff2 = edata.substr(10);
                var ErrorStuff3 = e.data.substring(0, e.data.indexOf('Request'));
                //console.log("ErrorSTuff: ", ErrorStuff2);
                console.log("ErrorStuff: ", ErrorStuff3);
                alert("Error: " + ErrorStuff3);
                //alert("Create cert rejected by program.\n" + "Please ensure all " + data.numLoads +" loads are signed off.");
                //throw e;
            
            }),
            function(){
                alert('Could not create Cert.');
            };
            
            };
            
    };    
 $scope.createNewCert = function(data){
    
        if(data.reviewBy == null || data.reviewBy == ""){
            alert("Please ensure TTPI is reviewed.");
        }
        else{
            console.log(data.reviewBy);
        
        
            console.log("Print Cert activated");
            console.log("WO: ", data.workOrder);
            var url = '/HeatTreat/printcert/';
            var newCert = {
                workOrder : data.workOrder,
            };
            
            $http.post(url, newCert)
            .then(function(response){
                $scope.certsaved = response.data.certSaved;
                //alert("Cert Created. Please 'Open Printer'");
                
                $scope.openPrintCert(data.workOrder); // Only open upon success, otherwise show error message(s)
            
            })
            .catch(function(e){
                //console.log("status: ", e.status);
                //console.log("header: ", e.headers);
                //console.log("test2: ", e.data.also);
                //console.log("got an error in initial processing",e);
                //console.log("also:", e.data);
                
                //var ErrorStuff = e.data.substr(0, e.data.indexOf('REQUEST'));
                var edata = e.data;
                //var ErrorStuff2 = edata.substr(10);
                var ErrorStuff3 = e.data.substring(0, e.data.indexOf('Request'));
                //console.log("ErrorSTuff: ", ErrorStuff2);
                console.log("ErrorStuff: ", ErrorStuff3);
                alert("Error: " + ErrorStuff3);
                //alert("Create cert rejected by program.\n" + "Please ensure all " + data.numLoads +" loads are signed off.");
                //throw e;
            
            }),
            function(){
                alert('Could not create Cert.');
            };
            
            };
            
    };        
    $scope.openPageThenEdit = function(spec){
        localStorage.setItem('passSpecNumber', spec.specNumber);
        localStorage.setItem("passSpecRev", spec.specRevision);
        localStorage.setItem("passSpecMat",spec.specMaterial);
        localStorage.setItem("passSpecMatSpec",spec.specMaterialSpec);
        localStorage.setItem("passSpecMatSpecRev", spec.specMaterialSpecRevision);
        localStorage.setItem("passSpecFormRev", spec.specFormRevision)
    //Moves to next page
        //window.location.href = "HeatTreat/SolutionTreats";
        $scope.goToAbsoluteAddress("HeatTreat/SolutionTreats");

    };
    
    $scope.openOperatorTTPIThenEdit = function(workOrder, loadNumber){
        localStorage.setItem("passDataWO", workOrder);
        localStorage.setItem("passDataLoadNum", loadNumber);
    
    
        $scope.goToAbsoluteAddress("HeatTreat/OperatorTTPI");
    }
    
    $scope.openTTPIThenEdit = function(data){
        localStorage.setItem("passDataWO", data.workOrder);
        localStorage.setItem("passDataLoadNum", data.loadNumber);
        
        
    
        $scope.goToAbsoluteAddress("HeatTreat/EditTTPI");
    
    };
    
    
    
    $scope.openSpecificationsPage = function(){
        var relativeAddress = "HeatTreat/AddSpec";
        $scope.goToAbsoluteAddress(relativeAddress);
    }
    
    $scope.openMaterialsPage = function(){
        var relativeAddress = "HeatTreat/MaterialPortal";
               
        $scope.goToAbsoluteAddress(relativeAddress);
    }
        
    $scope.openOperatorsPage = function(){
        
        $scope.goToAbsoluteAddress("HeatTreat/OperatorPortal")
    }
    
    $scope.addMaterial = function(matName){
    
        var newMaterial = {
            materialName: matName  
        };
    
        $http.post('/HeatTreat/materials/', newMaterial)
        .then(function(response){
        },
        function(){
        alert('Could not create Material');
        
        
        });
        location.reload();   //Reload the web page to refresh data

    };
    
    //Add a new solution treat material
    $scope.addSolutionMaterial = function(matName, solution, harden, temper, age, normalize, anneal){
        
        var newMaterial = {
            materialName: matName,
            solutionMaterial: solution,
            hardenMaterial:  harden,
            temperMaterial: temper,
            ageMaterial: age,
            normalMaterial: normalize,
            annealMaterial: anneal
            
        };
    
        $http.post('/HeatTreat/materials/', newMaterial)
        .then(function(response){
        },
        function(){
        alert('Could not create Material');
        
        
        });
        location.reload();   //Reload the web page to refresh data

    };    
    $scope.addSpecification = function(specNum,specRev,specMat,specMatSpec,specMaterialSpecRev){
        console.log(specNum);
        console.log(specRev);
        console.log(specMat);
        console.log(specMatSpec);
        console.log(specMaterialSpecRev);
        

        var todayDate = getTodayDate();
        

        var newSpec = {
           specNumber : specNum,
           specRevision : specRev,
           specMaterial : specMat,
           specMaterialSpec :  specMatSpec,
           specMaterialSpecRevision : specMaterialSpecRev,
           specFormRevDate : todayDate,
        
        };
        
        
        $http.post('/HeatTreat/solutiontreatspecs/', newSpec)
        .then(function(response){
            alert("cert created");
        
        }).catch(function(){
        		alert("Cannot add material specification!");
        		})	
        //location.reload()

    };
    
    //POST request
    $scope.postTreats = function(varToPost){
        var url = '/HeatTreat/treats/';
    
        console.log("posttreats: ", varToPost.loadNumber);
                  
        $http.post(url, varToPost)
        .then(function(response){
                console.log("treats post success");
                alert("Heat Treat / TTPI creation success!");
        
        })
        .catch(function(e){
            
            //console.log(e.data); //Lot error e
            try{
                var edata = e.data;
                //var ErrorStuff2 = edata.substr(10);
                var ErrorStuff3 = e.data.substring(0, e.data.indexOf('Request'));
                //console.log("ErrorSTuff: ", ErrorStuff2);
                console.log("ErrorStuff: ", ErrorStuff3);
                alert("Error: " + ErrorStuff3);   
                }
                catch(err){
                alert("error trying to print error message. Contact Software Engineering.");
                console.log("error is: ", err);
                }
                finally{
                    alert("Cannot create TTPI!");
                }         
        
        })	    
    
    };
    
    $scope.goToAbsoluteAddress = function(relativeAddress){
               
               //var relativeAddress = "/HeatTreat/MaterialPortal";
               
               
               var hostAddress = location.hostname;
               if (hostAddress == "127.0.0.1"){
                   hostAddress = hostAddress+":8000";
                   }
                   
            var absoluteAddress = "http://" +hostAddress +"/"+ relativeAddress;
               window.location.href= absoluteAddress;    
    }
    
    
    //PUT request for orders (treats)
    //This is full request with put, then, catch
    $scope.putTreats = function(data){
        if(data.locked){
            alert("This TTPI is locked. Changes will not be saved.");
        
        }
        else{
               $scope.putTreatsCatch(data)
        		.catch(function(e){
        		console.log("error: ", e.data);
        		alert("Data entered is invalid.");
        		})        
        }
 
    }
    
    
    //Use this as started, then add catch if you want a specific catch statement
    //This is partial request with put, then.
    // You can chain your own custom catch
    $scope.putTreatsCatch = function(data){
       	if(data.locked){
            alert("This TTPI is locked. Changes will not be saved.");
       	
       	}
       	else{
              return (
                    $scope.putTreatsThenCatch(data)
                    .then(function(response){
                        console.log("success");
                    })
            )       	
        }
    }
    
    //The most basic put
    $scope.putTreatsThenCatch = function(data){
        var url = '/HeatTreat/treats/' + data.id + '/';
        //console.log(data);
        if(data.locked){
                alert("This TTPI is locked. Changes will not be saved.");
                return
        }
        else{
            return(
                $http.put(
                    url,
                    data)
            );
        };
    }
    
    
    $scope.createTTPI = function(operator, spec, workOrderNumber, numberOfLoads, ponumber, heat, opnum ){
            $scope.createTTPIButton = true;  // Disable the create new ttpi button temporarily
            //console.log("fred: ", fred);
            //console.log("mat: ", mat);

            // if heat number is blank or null that means it is not optionally filled in
            // trigger it to be 99 which is default expected by python model's save function
            var canProceed = true;
            console.log("op: ", operator);

            if(operator == "" | operator == null | operator == undefined){
                console.log("Operator is missing");
                canProceed = false;

            }
            if(spec == "" | spec == null | spec == undefined){
                console.log("Spec number is missing");
                canProceed = false;
            }
            else{
                console.log("spec: ", spec);

            }



            if(workOrderNumber == "" | workOrderNumber == null | workOrderNumber == undefined){
                console.log("work order is missing");
                canProceed = false;
                }
            //If workorderNumber starst with "TEST" then ponumber = "INTERNAL"
            else if(workOrderNumber.startsWith("TEST") | workOrderNumber.startsWith("Test") | workOrderNumber.startsWith("test") ){
                console.log("starts with TEST");
                ponumber = "INTERNAL";
            }

            if(numberOfLoads == "" | numberOfLoads == null | numberOfLoads == undefined){
                console.log("Number of loads is missing");
                canProceed = false;
            }



            if(ponumber == "INTERNAL"){
                console.log("PO# Can proceed");
                canProceed = true;
            }
            else if(ponumber == "" | ponumber == null | ponumber == undefined){
                console.log("PO # is missing");
                canProceed = false;
                }









            if(canProceed){
                for(var i = 0; i< numberOfLoads; i++){
    
                    var TTPIname = "newTTPI" + i.toString();
    
    
                    if(heat =="" | heat == null | heat == undefined){
                        console.log("heat: " + heat);
                        heat = 99;
                        console.log("heat: "+ heat);

                    }
                    if(opnum == "" | opnum == null | opnum == undefined){
                        opnum = 99;
                    }
    
    
                    TTPIname ={
                        workOrder : workOrderNumber,
                        genBy : operator.operatorName,
                        specNumber : spec.specNumber,
                        specRevision : spec.specRevision,
                        specMaterial : spec.specMaterial,
                        specMaterialSpec : spec.specMaterialSpec,
                        specMaterialSpecRevision : spec.specMaterialSpecRevision,
                        tempSetPoint : spec.specTempSetPointPref, //New 7/25/19
                        genDate : getTodayDate(),
                        partNumber : 99, //This turns into a STRING in Python Django model
                        customer : 99, //should be 1 match from PO#
                        rev : 99, //should be 1 match from work order
                        //PO : 99,
                        PO: ponumber,
                        heatNumber: heat,
                        WOop : opnum,
                        numLoads: numberOfLoads,
                        loadNumber: i+1,
                    }
                    
                    console.log("loadnumber: ", TTPIname.loadNumber);
                    console.log("TTPI name: ", TTPIname);
                    $scope.postTreats(TTPIname);
              
                    
    
                }

            //location.reload(); // If you use this, it will refresh over the errors. Do not use this.


            }
            else{
                alert("Required field is missing!");
            }

    };

    $scope.clearCreateTTPI = function(){
            //Need to erase fields without reloading the page. Reload will reset any errors that are shown to user.
            
            //Generated by id="genByComboBox"
            document.getElementById("genByComboBox").value = undefined; 
            //spec number id="specNum"
            document.getElementById("specNum").value = undefined; 
            //material spec id="specMat"
            document.getElementById("specMat").value = undefined;
            //work order id="workOrder"
            document.getElementById("workOrder").value = null; 
            //numbre of loads id="numLoads"
            document.getElementById("numLoads").value = null; 

            document.getElementById("poNum").value = null;
            document.getElementById("heatNum").value = null;
            document.getElementById("opNum").value = null;

            $scope.createTTPIButton = false;


    }
    

    
    $scope.increaseSpecFormRev = function(spec){
    
        if(spec.mostCurrent){

            if(spec.specMasterReviewed !=null && spec.specMasterApproved != null){
                spec.specFormRevision = 99; //Set to 99 to use as trigger in Django save method
                console.log(spec.specFormRevision);
                $scope.copyPutTreatSpecs(spec); //IF you use regular PutTreatSpecs it will fail due to "locked" restriction
                location.reload();        
            }
            else{
                alert("Spec must be reviewed and approved to increase form revision.");
            
            }
        }
        else{
            alert("You are only able to increase form rev of the most current spec.");
        
        }
    }
    
    //track by data.id + article: https://stackoverflow.com/questions/23264789/angularjs-ng-repeat-to-assign-generate-a-new-unique-id
    //https://docs.angularjs.org/api/ng/directive/ngRepeat
    $scope.setDateInToday = function(data){
        //the id of the element is dateIn-data.id like dateIn-67344 to uniquely identify it
        var todayDate = getTodayDate();

        console.log(data.id);
        var idTarget = "dateIn-"+data.id;
        console.log(idTarget);

        document.getElementById(idTarget).value = todayDate;
        //angular.element(document.getElementById("dateIn")).triggerHandler('change'); //Calls ng-change, which then calls update() function
        angular.element(document.getElementById(idTarget)).triggerHandler('change'); //Calls ng-change, which then calls update() function

    };

    $scope.setDateOutToday = function(data){
        console.log(data.id);

        var todayDate = getTodayDate();
        console.log(todayDate);

        var idTarget = "dateOut-"+data.id;
        console.log(idTarget);
        
        //document.getElementById("dateOut").value = todayDate;
        //angular.element(document.getElementById("dateOut")).triggerHandler('change'); //Calls ng-change, which then calls update() function

        document.getElementById(idTarget).value = todayDate;
        angular.element(document.getElementById(idTarget)).triggerHandler('change'); //Calls ng-change, which then calls update() function
    
    };
    
    $scope.setReviewDateToday = function(data){
        console.log("data.reviewBy: ", data.reviewBy);
        //data.reviewDate = getTodayDate(); //This doesn't work
        console.log(data.reviewDate);

        //document.getElementById("reviewDateInputBox").value = todayDate;
        var elementID = "reviewDateInputBox" + data.id;
        console.log("value", document.getElementById(elementID).value);
        console.log(elementID);
        console.log("typeof: ", typeof(elementID));
        //angular.element(document.getElementById(elementID)).triggerHandler('change'); //Calls ng-change, which then calls update() function
        //angular.element(document.getElementById(elementID)).trigger('change'); //Calls ng-change, which then calls update() function
        
        document.getElementById(elementID).value = getTodayDate(); // Must use this in conjuction with trigger Handler below
        angular.element(document.getElementById(elementID)).triggerHandler('change'); //Calls ng-change, which then calls update() function
        
    
        //$('select[ng-model="data.reviewDate"]').trigger('change');    
    }
    
    $scope.setTimeOutNow = function(data){
        console.log(data.id);
        var n =  new Date();
     
        var h = n.getHours();
        var M = n.getMinutes();
        
        var hh = '00' + h;
        hh = hh.slice(-2);
        
        var MM = '00' + M;
        MM = MM.slice(-2);
        
        var nowTime = (hh+":"+MM);
        console.log(nowTime);

        var idTarget = "timeOut-"+data.id;
        console.log(idTarget)

        //document.getElementById("timeOut").value = nowTime;
        //angular.element(document.getElementById("timeOut")).triggerHandler('change'); //Calls ng-change, which then calls update() function

        document.getElementById(idTarget).value = nowTime;
        angular.element(document.getElementById(idTarget)).triggerHandler('change'); //Calls ng-change, which then calls update() function
    
    };
    
    $scope.updateCert = function(certdata){
        var url = '/HeatTreat/printcert/' +certdata.id +'/';
        certdata.overrideSafeguard = true;
        //console.log("peanut butter");
        //console.log("jelly");
        //$http.put(url, certdata); #######################################################
        $http.patch(url, create);
        //location.reload();
    
    
    }
    

    $scope.updateMaterialList = function(materialData){
        var url = '/HeatTreat/materials/' + materialData.id + '/';
        console.log("snooze");
        	console.log(materialData.materialName);
        	if(materialData.materialName == ""){
            	console.log("true");
            	
            	$http.delete(
                	url,
                	materialData
            	);
        	}
        	else{
            	$http.put(
                	url,
                	materialData
            	);
        	}
        location.reload();   	
    };
    	
	$scope.updateReview = function(data){
        console.log(data.workOrder, data.loadNumber, data.locked, data.reviewBy);
        console.log(data.reviewDate);
        var today = getTodayDate();
        console.log(today);

        var dateParts = data.reviewDate.split('-');
        if(dateParts[0].length != 4){
            alert("Please enter date in format: YYYY-MM-DD, E.G.: 2019-10-03.");
        }
        else{
            var approvedUsers = ['morenod','ganzhav','rodrigueza']
            if(approvedUsers.includes(spec.specMasterReviewed) && approvedUsers.includes(spec.specMasterApproved)){
                if(!data.locked){
    
                    if(data.reviewBy != null && data.reviewDate != null && data.reviewDate != '1900-01-01' && (data.reviewDate <= today) && (data.postItNote == null | data.postItNote == "")){
                        
        
                        $scope.putTreatsThenCatch(data)
                        .then(function(response){
                            $("#topLevelDiv").find("input,button,textarea,select").attr("disabled",true);
                            alert("TTPI is now locked.");
                        
                        })
                        .catch(function(e){
                            console.log("error: ", e);
                            alert("Review failed. Data is not locked.");
                        })	
                        data.locked = true;
                    }
                    else if(data.postItNote != null && data.postItNote != ""){
                        alert("Please clear the sticky note.");
                    }
                    else if (data.reviewDate > today){
                        alert("Date reviewed cannot be in the future.");
                    }
        
                    else{
                        alert("Please ensure reviewed by and reviewed date are not blank.");
                    }
                }
                else{
                    alert("TTPI is already locked.");
                }
                }
            else{
                alert("Spec must be reviewed and approved by approved users.");
            }
        }

    }
    
    $scope.commitSpecApproved = function(spec){
        //console.log(username);
        //console.log(spec);
        var username = document.getElementById("username").value;
        
        if(spec.specMasterReviewed == null){
            alert("Please review specification first before approving.");
        }
        else if(username == spec.specMasterReviewed){
            alert("The approver cannot be the reviewer.");
        
        }
        else{
            console.log("username: ", username);
            console.log(username);
            console.log("spec locked: ", spec.specLocked);
            //console.log("username: " + x);
            if(username == "morenod"){
                spec.specMasterApproved = "D.Moreno";
                if(spec.specMasterReviewed != null && spec.specMasterApproved != null){
                //As long as specmasterpparoved is not null it will lock file //This triggers the correct save method to fire
                $scope.putTreatSpecs(spec);

                }
            }
            else if (username == "ganzhav"){
                spec.specMasterApproved = "V.Ganzha";
                if(spec.specMasterReviewed != null && spec.specMasterApproved != null){
                //As long as specmasterpparoved is not null it will lock file //This triggers the correct save method to fire
                $scope.putTreatSpecs(spec);

                }

            }
            else if (username == "rodrigueza"){
                spec.specMasterApproved = "A.Rodriguez";
                if(spec.specMasterReviewed != null && spec.specMasterApproved != null){
                //As long as specmasterpparoved is not null it will lock file //This triggers the correct save method to fire
                $scope.putTreatSpecs(spec);

                }

            }
            else{
                alert("Please make sure you are signed in. Only the following people can approve specs: morenod, ganzhav, rodrigueza.");

            }
        

            
        
        }
    
    }
    
    $scope.commitSpecReviewed = function(spec){
        //For integers a <0 check is built into the model by using PositiveSmallIntegerField
    
        if(!spec.specVF1 && !spec.specVF2 && !spec.specTMQ1 && !spec.specTMQ2 && !spec.specTMQ3){
            alert("At least one furnace capability must be selected!");
        }
        else if(spec.specTempSetPointLow == null || spec.specTempSetPointHigh == null ){
            alert("Check temperature set point low and high are set.");
        }
        else if(spec.specUniformityTol == null || spec.specUniformityTol == 0 || spec.specUniformityTol == "0"){
            alert("Uniformity tolerance must be a non-zero value.");
        }
        else if(spec.specSoakTime == null || spec.specSoakTime == 0 || spec.specSoakTime =="0"){
            alert("Spec Soak Time must be a non-zero value.");
        }
        else if(spec.specSoakMinusTimeTol == null){
            alert("Please check Soak MINUS time.");
        }
        else if(spec.specSoakPosTimeTol == null){
            alert("Please check Soak PLUS time.");
        }
        else if( (spec.specVF1 || spec.specVF2) && spec.specVFVacPressure == null){
            alert("Please check VF Vacuum Pressure.");
        }
        else if( (spec.specTMQ1 || spec.specTMQ2 || spec.specTMQ3) && (spec.specTMQHeatLow == null || spec.specTMQHeatHigh == null || (spec.specTMQHeatHigh <spec.specTMQHeatLow ))){
            alert("Please verify TMQ CFH is entered, and high > low .");
        
        }
        else if (!spec.specQuenchGFC && !spec.specQuenchOil && !spec.specQuenchWater && !spec.specQuenchAir ){
            alert("Please choose at least one quench method: GFC, Oil, Water, Air.");
        
        }
    
        else{
            var username = document.getElementById("username").value;
            console.log("username: ", username);
            console.log(username);
            
            if(username == "morenod"){
                spec.specMasterReviewed = "D.Moreno";
            }
            else if (username == "ganzhav"){
                spec.specMasterReviewed = "V.Ganzha";
            }
            else if (username == "rodrigueza"){
                spec.specMasterReviewed = "A.Rodriguez";
            }
            else{
                spec.specMasterReviewed = username;

            }
            
            
            $scope.putTreatSpecs(spec);
        }
    
    }
    
    $scope.filterPendingButton = function(){
        console.log("start: ", $scope.filterPending);
        
        if($scope.filterPending === undefined){
            $scope.filterPending = null;
        }
        else if($scope.filterPending == null){
            $scope.filterPending = undefined;

        }

    }
    $scope.filterMostRecentButton = function(){
        console.log("start: ", $scope.filterMostRecent);
        
        if(!$scope.filterMostRecent){
            $scope.filterMostRecent = true;
        }
        else if($scope.filterMostRecent){
            $scope.filterMostRecent = undefined;

        }    
    }
    
    $scope.filterOperator = true; //This will default the filter to only show true, user can toggle this later
    $scope.toggleOperatorDone = function(data){
    
        if(!$scope.filterOperator){
            $scope.filterOperator = true;
        }
        else if ($scope.filterOperator){
            $scope.filterOperator = undefined;
            }
        
    
    
    }
    
    
    
    $scope.updateSpecRevFilter = function(spec){
        localStorage.setItem("passSpecRev", spec.specRevision);
        document.getElementById("specRevInput").value = spec.specRevision;
        location.reload();
    }
    
    $scope.updateSpecMaterialSpecFilter = function(spec){
        localStorage.setItem("passSpecMatSpecRev", spec.specMaterialSpecRevision);
        document.getElementById("specMaterialSpecRevInput").value = spec.specMaterialSpecRevision;
        location.reload();
    
    }
    
    $scope.openPrintCert = function(WO){
        console.log(WO);
        localStorage.setItem("passPrintWorkOrder", WO);
        
        //window.location.href = "HeatTreat/certprinter";
        $scope.goToAbsoluteAddress("HeatTreat/certprinter");
        
    }

    
    
    
    
    
    
};

}());

//This is needed for CSRF protection, see also .run(...) chain at top near .module
function run($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';

}


/**
 * Filters out all duplicate items from an array by checking the specified key
 * @param [key] {string} the name of the attribute of each object to compare for uniqueness
 if the key is empty, the entire object will be compared
 if the key === false then no filtering will be performed
 * @return {array}
 *https://github.com/angular-ui/angular-ui-OLDREPO/blob/master/modules/filters/unique/unique.js
 */
 
//make sure to change module('blah') to module('HT.HeatTreat') if you get more
angular.module('HT.HeatTreat').filter('unique', function () {

  return function (items, filterOn) {

    if (filterOn === false) {
      return items;
    }

    if ((filterOn || angular.isUndefined(filterOn)) && angular.isArray(items)) {
      var hashCheck = {}, newItems = [];

      var extractValueToCompare = function (item) {
        if (angular.isObject(item) && angular.isString(filterOn)) {
          return item[filterOn];
        } else {
          return item;
        }
      };

      angular.forEach(items, function (item) {
        var valueToCheck, isDuplicate = false;

        for (var i = 0; i < newItems.length; i++) {
          if (angular.equals(extractValueToCompare(newItems[i]), extractValueToCompare(item))) {
            isDuplicate = true;
            break;
          }
        }
        if (!isDuplicate) {
          newItems.push(item);
        }

      });
      items = newItems;
    }
    return items;
  };
});
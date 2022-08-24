//function to show and hide elements
function showBuy() {
    document.getElementById("startBuy").style.display = 'block';
    document.getElementById("initialTable").style.display = 'none';
}

var jubilee = document.getElementById("JUBILEE"); 
var madison = document.getElementById("MADISON");
var corporate = document.getElementById("CORPORATE");
var sanlam = document.getElementById("SANLAM");
var pioneer = document.getElementById("PIONEER");
var directline = document.getElementById("DIRECTLINE");
var trident = document.getElementById("TRIDENT");
var britam = document.getElementById("BRITAM");
var uap = document.getElementById("UAP");

if (jubilee != null) {jubilee.addEventListener("click", showBuy)};
if (madison != null) {madison.addEventListener("click", showBuy)};
if (corporate != null) {corporate.addEventListener("click", showBuy)};
if (sanlam != null) {sanlam.addEventListener("click", showBuy)};
if (pioneer != null) {pioneer.addEventListener("click", showBuy)};
if (directline != null) {directline.addEventListener("click", showBuy)};
if (trident != null) {trident.addEventListener("click", showBuy)};
if (britam != null) {britam.addEventListener("click", showBuy)};
if (uap != null) {uap.addEventListener("click", showBuy)};


//function to get the selected insurer name
function postInsurer() {
    
    var radios = document.querySelectorAll('input[type="radio"]:checked');
    var value = radios.length>0? radios[0].value: null;
    var name = radios.length>0? radios[0].name: null;
    var params=name+"="+value;
    var request = new XMLHttpRequest();
    request.open('POST', '/getInsurer', true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.send(params);
    
    //submit the form
    document.getElementById("form1").submit();
}
document.getElementById("submitKYC").addEventListener("click", postInsurer);


//function to show and hide elements
function addChild() {
    document.getElementById("form1").style.display = 'block';
    document.getElementById("startBuy").style.display = 'none';
    document.getElementById("submitKYC").style.display = 'block';
    document.getElementById("kycForm").style.display = 'block';        
}
document.getElementById("startBuy").addEventListener("click", addChild);

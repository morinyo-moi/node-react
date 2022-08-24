//function to get the default date as today

document.getElementById("startDate").valueAsDate = new Date();



//upload logbook to s3 using presigned url
(function() {
  document.getElementById("logbook").onchange = function(){
    var files = document.getElementById("logbook").files;
    var logbook = files[0];
    getSignedLgbk_url(logbook);
  };
})();

function getSignedLgbk_url(file){
    
let reg_num = document.getElementById("regNum").value.replace(/\s+/g, '').toUpperCase();
let lgbk_key = `${reg_num}-LOGBOOK`;
//console.log(lgbk_key);
    
var xhr = new XMLHttpRequest();
xhr.open("GET", "/signLogbook_s3?file_name="+lgbk_key+"&file_type="+file.type);
xhr.onreadystatechange = function(){
  if(xhr.readyState === 4){
    if(xhr.status === 200){
      var response = JSON.parse(xhr.responseText);
      uploadLgbk(file, response);
    }
//     else{
//       //console.log("Could not get signed URL for the logbook.");
//     }
  }
};
xhr.send();
}

function uploadLgbk(file, s3Data){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", s3Data.url);

  var postData = new FormData();
  for(key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){
        console.log("Logbook image uploaded successifully.");
      }
//       else{
//         console.log("Could not upload logbook image.");
//       }
   }
  };
  xhr.send(postData);
}




//upload national id to s3 using presigned url
(function() {
  document.getElementById("natID").onchange = function(){
    var files = document.getElementById("natID").files;
    var natId = files[0];
    getSignedNatID_url(natId);
  };
})();

function getSignedNatID_url(file){
alert("j");
let reg_num = document.getElementById("regNum").value.replace(/\s+/g, '').toUpperCase();
let owner_names = document.getElementById("ownerNames").value.replace(/\s+/g, '').toUpperCase();    
let natid_key = `${reg_num}-${owner_names}`;  
//console.log(natid_key);    
    
var xhr = new XMLHttpRequest();
xhr.open("GET", "/signNatid_s3?file_name="+natid_key+"&file_type="+file.type);
xhr.onreadystatechange = function(){
  if(xhr.readyState === 4){
    if(xhr.status === 200){
      var response = JSON.parse(xhr.responseText);
      uploadNatID(file, response);
    }
  }
};
xhr.send();
}

function uploadNatID(file, s3Data){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", s3Data.url);

  var postData = new FormData();
  for(key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){
        console.log("ID image uploaded successifully.");
      }
//       else{
//         console.log("Could not upload National ID image.");
//       }
   }
  };
  xhr.send(postData);
}

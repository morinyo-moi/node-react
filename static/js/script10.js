//function to get the default date as today

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
       $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });
        $.ajax({

            type: 'GET',

            url: '/signLogbook_s3',

            data: {
                type: file.type,
                lgbk_key:lgbk_key,
            },
            success: function (response) {
                var data=JSON.parse(response)
                uploadLgbk(file, data);
            }

        });

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
        console.log("Logbook image uploaded successfully.");
      }
       else{
         console.log("Could not upload logbook image.");
       }
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
let reg_num = document.getElementById("regNum").value.replace(/\s+/g, '').toUpperCase();
let owner_names = document.getElementById("ownerNames").value.replace(/\s+/g, '').toUpperCase();    
let natid_key = `${reg_num}-${owner_names}`;


        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });
        $.ajax({

            type: 'GET',

            url: '/signNatid_s3',

            data: {
                type: file.type,
                natid_key:natid_key,
            },
            success: function (response) {
                console.log("ppppppppppppppppppppppppp")
                console.log(response)
                var data=JSON.parse(response)
                uploadNatID(file, data);
            }
        });
}

function uploadNatID(file, s3Data){
 console.log("uuu")
 console.log(s3Data.url)
 console.log(s3Data.fields.key)
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
        console.log("ID image uploaded successfully.");
      }
       else{
         console.log("Could not upload National ID image.");
       }
   }
  };
  xhr.send(postData);
}


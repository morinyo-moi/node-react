// preloader
var loader = document.querySelector('.loader');
window.addEventListener("load", function(){
	loader.style.display = "none";
});


//set up the dropdown function
make_select = document.getElementById('Make');
model_select = document.getElementById('Model');

make_select.onchange = function(){

	make = make_select.value;
	fetch('model/' + make).then(function(response){ 
	response.json().then(function(data) {
		optionHTML = '<option value="" selected disabled hidden>Select the Model</option>';
		for (model of data.model_make) {
		optionHTML += '<option value="' + model.id +'">' + model.name + '</option>'
		}
		model_select.innerHTML = optionHTML;
	});
	});
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('/service_worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered');
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}

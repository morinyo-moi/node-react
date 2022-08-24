//function for the make and model dropdowns
make_select = document.getElementById('make');
model_select = document.getElementById('model');
alert("j")

console.log(make_select);

make_select.onchange = function(){
alert("j")
	make = make_select.value;
	fetch('/model/' + make).then(function(response){
	response.json().then(function(data) {
	    console.log(model_select)
		optionHTML = '<option value="" selected disabled hidden>Select the Model</option>';
		for (model of data.model_make) {
		optionHTML += '<option value="' + model.id +'">' + model.name + '</option>'
		}
		model_select.innerHTML = optionHTML;
	});
	});
	}

//register service worker
//if ('serviceWorker' in navigator) {
//	navigator.serviceWorker
//	.register('/service_worker.js')
//	.then(function(registration) {
//		console.log('Service Worker Registered');
//		return registration;
//	})
//	.catch(function(err) {
//		console.error('Unable to register service worker.', err);
//	});
//}
	

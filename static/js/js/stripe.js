var stripe = Stripe('pk_test_51Lg4MyK6rkKpcwrpM9imgTsK4IupHl9BSeuzPgUQRWExpYnqHxr3Xe9juCUXGR10JXsiknlxoUeZGpTTw2lGG1UF00K0cn1Xv4');

const addFunds1Btn = document.getElementById('add-funds-btn')
console.log(777)
if (addFunds1Btn){
	addFunds1Btn.onclick = () => {
		console.log(123)
			getStripe("stipe")
		}
}


function getStripe(plane){
    let xhr = new XMLHttpRequest();
	xhr.open("GET", '/payment/stripe?price=' + '100')
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json")
	xhr.setRequestHeader("Access-Control-Allow-Origin", window.location.host)
	xhr.send()
	xhr.onload = () => {
		if (xhr.status === 200){
			// document.location.href = JSON.parse(xhr.responseText)["invoice_url"]
			window.open(JSON.parse(xhr.responseText)["invoice_url"], '_blank');
			// stripe.redirectToCheckout({
			// sessionId: session_id
			// })
			// .then(function(result) {
			// console.log("STRIPE", result.error.message)
			// let displayError = document.getElementById('error-message');
			// displayError.textContent = result.error.message;});
	}}
}

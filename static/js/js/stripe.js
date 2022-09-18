var stripe = Stripe('pk_test_51Lg4MyK6rkKpcwrpM9imgTsK4IupHl9BSeuzPgUQRWExpYnqHxr3Xe9juCUXGR10JXsiknlxoUeZGpTTw2lGG1UF00K0cn1Xv4');


const addFunds1Btn = document.getElementById('add-funds-btn')
if (addFunds1Btn){
	addFunds1Btn.onclick = () => {
			let totalPrice = document.getElementById("total-invoice").innerText.slice(0, -1)
			let invoiceId = document.getElementById("invoice-id").innerText
			getStripe(totalPrice, invoiceId)
		}
}


function getStripe(price, invoice_id){
    let xhr = new XMLHttpRequest();
	xhr.open("GET", '/payment/stripe?price=' + price + '&' + 'invoice_id=' + invoice_id)
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json")
	xhr.setRequestHeader("Access-Control-Allow-Origin", window.location.host)
	xhr.send()
	xhr.onload = () => {
		if (xhr.status === 200){
			window.open(JSON.parse(xhr.responseText)["invoice_url"], '_blank');
	}}
}

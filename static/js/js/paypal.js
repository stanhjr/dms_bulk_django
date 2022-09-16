
const AddFundsBtn = document.querySelector(".btn-wrap")
if (AddFundsBtn) {
	AddFundsBtn.onclick = () => {
		getPaypalForm()
	}
}


function getPaypalForm() {
	const contentPopup = document.getElementById("popup-invoice-awaiting")
	const srcBtn = document.getElementsByClassName("js-toggle-deposit active")[0].getElementsByTagName("img")[0].src
	const price = document.getElementsByClassName("js-input-numeric add-funds-price")[0].value
	if (srcBtn.indexOf("btn-paypal") > 0){
	let xhr = new XMLHttpRequest();
	xhr.open("GET", '/payment/get_paypal_form?price=' + price)
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json")
	xhr.setRequestHeader("Access-Control-Allow-Origin", window.location.host)
	xhr.send()
	xhr.onload = () => {
		if (xhr.status === 200){
			console.log('pass')
			// contentPopup.innerHTML = JSON.parse(xhr.responseText)["content"]

	}}

}
}










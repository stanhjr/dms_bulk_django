$(document).ready(() => {
    const add_funds_price = JSON.parse(localStorage.add_funds_price).price
    document.querySelector('.btn.js-popup').innerText = `Add Funds: ${add_funds_price}`
    document.querySelector('.js-input-numeric').value = add_funds_price
})
$(document).ready(() => {
    const add_funds_price = JSON.parse(localStorage.add_funds_price).price
    document.querySelector('.btn.js-popup').innerText = `Add Funds: ${add_funds_price}`
    document.querySelectorAll('.add-funds-price').forEach(tag => {
        tag.innerText = add_funds_price
    });
})
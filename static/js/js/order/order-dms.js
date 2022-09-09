const addFundsButtonClick = () => {
    const add_funds_price = document.querySelector('.js-price-amount').innerText
    localStorage.setItem('add_funds_price', JSON.stringify({
        'price': add_funds_price
    }))
}
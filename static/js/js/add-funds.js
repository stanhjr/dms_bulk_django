window.addEventListener('load', () => {
    const add_funds_price = JSON.parse(localStorage.add_funds_price).price

    document.querySelector('.btn.js-popup').innerText = `Add Funds: ${add_funds_price}`
    document.querySelector('.js-input-numeric').value = add_funds_price
    document.querySelectorAll('.add-funds-price').forEach(tag => {
        tag.innerText = add_funds_price
    });

    $('.js-input-numeric.add-funds-price').on('keyup', () => {
        const oldstr = $('.js-input-numeric.add-funds-price').val()
        const str = oldstr.replace('$', '')
        $('.js-input-numeric.add-funds-price').val(str + '$')      
    })

    document.querySelector('.js-input-numeric').addEventListener('input', event => {
        document.querySelector('.btn.js-popup').innerText = `Add Funds: ${event.target.value}`
        localStorage.add_funds_price = JSON.stringify({
            price: `${event.target.value}`
        })
    })

    document.querySelector('.btn.js-popup').addEventListener('click', () => {
        document.querySelector('#id_payment_method').value = document.querySelector('.js-toggle-deposit.active').id
        document.querySelector('#id_cents').value = document.querySelector('.js-input-numeric.add-funds-price').value.slice(0, -1) * 100

        document.querySelector('#create_invoice_calc_form').submit()
    })
})
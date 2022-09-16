$('.js-input-numeric.add-funds-price').on('keyup', () => {
    const oldstr = $('.js-input-numeric.add-funds-price').val()
    const str = oldstr.replace('$', '')

    $('.js-input-numeric.add-funds-price').val(str + '$')
    if (!str) {
        $('.btn.js-popup').text('Add Funds: 0$')
    } else {
        $('.btn.js-popup').text(`Add Funds: ${str}$`)
    }
})

$('.btn.js-popup').click(() => {
    $('#id_payment_method').val($('.js-toggle-deposit.active').attr('id'))
    $('#id_cents').val(
        $('.js-input-numeric.add-funds-price').val().slice(0, -1) * 100
    )
    $('#create_invoice_calc_form').submit()

    const invoice_id = $('.invoice-table > .td')[0].innerText.match('(DM-[0-9]*-)([0-9]*)')
    
    const current_date = new Date()
    const date_string = ('0' + current_date.getDate()).slice(-2) + '.'
                + ('0' + (current_date.getMonth()+1)).slice(-2) + '.'
                + current_date.getFullYear()

    const new_invoice = `
        <div class="tr invoice-table">
            <div class="td invoice-id">${invoice_id[1] + (parseInt(invoice_id[2]) + 1)}</div>
            <div class="td invoice-payment-method">${$('.js-toggle-deposit.active').attr('id')}</div>
            <div class="td invoice-description">Social Media Marketing</div>
            <div class="td invoice-price">${$('.js-input-numeric.add-funds-price').val()}</div>
            <div class="td invoice-status"><span class="c-orange">Awaiting Payment</span></div>
            <div class="td invoice-created-at">${date_string}</div>
            <div class="td"><a class="js-popup" href="#popup-invoice-awaiting">View</a></div>
        </div>
    `
    $('.table > div:nth-child(1)').after(new_invoice)
})
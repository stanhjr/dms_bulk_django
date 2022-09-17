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
})
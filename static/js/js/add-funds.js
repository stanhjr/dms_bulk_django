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

$('.open-invoice-btn').click(event => {
    const current_invoice_table = new Array()
    $(event.target).closest('.invoice-table').children().each((i, element) => current_invoice_table.push($(element).text()))
    
    $('.table-info > .tr:eq(1) > .td:eq(0)').text(current_invoice_table[0])
    $('.table-info > .tr:eq(1) > .td:eq(1)').text(current_invoice_table[1])
    $('.table-info > .tr:eq(1) > .td:eq(2)').text(current_invoice_table[2])
    $('.table-info > .tr:eq(1) > .td:eq(3) > span').text(current_invoice_table[4])

    $('.info-wrap > div:eq(1) > p').text(current_invoice_table[5])

    $('.table-total > .tr').each((i, element) => $(element).find('.td:eq(1)').text(current_invoice_table[3]))

    $('.header-wrap > .right > p').text(`ID (#${current_invoice_table[0]})`)

    if (current_invoice_table[1] === 'Paypal') {
        $('#paypal-button-container').css('display', 'block')
    } else {
        $('#paypal-button-container').css('display', 'none')
    }
})
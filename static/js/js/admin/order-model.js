$(() => {
    if ($('#id_sending').is(':checked') || !$('#id_scraping').is(':checked')) {
        $('.form-row.field-sending_end_at').remove()
    }
})
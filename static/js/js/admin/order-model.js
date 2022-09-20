$(() => {
    if ($('#id_sending').is(':checked') || !$('#id_scraping').is(':checked')) {
        $('.form-row.field-hours_to_sending_end').remove()
    }
})
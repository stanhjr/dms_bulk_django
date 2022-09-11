window.addEventListener('load', () => {
    const social_network = document.querySelector('.tab-content.active > .block-social-calculator.block-white > div > b').innerText
    const add_funds_price = document.querySelector(`.result-wrap.${social_network.toLowerCase()} > div:nth-child(3) > div`).innerText
    console.log(add_funds_price)
    document.querySelector('.js-price-amount').innerText = add_funds_price
})

const saveAddFundsPriceInLocalStorage = () => {
    const social_network = document.querySelector('.tab-content.active > .block-social-calculator.block-white > div > b').innerText
    const add_funds_price = document.querySelector(`.result-wrap.${social_network.toLowerCase()} > div:nth-child(3) > div`).innerText

    localStorage.add_funds_price = JSON.stringify({
        'price': add_funds_price
    })
}

const saveOrderCompaignInfoInLocalStorage = () => {
    localStorage.compaign_info = JSON.stringify({
        targets_or_competitors_submited: document.querySelector('#targets_or_competitors_submited').value,
        use_our_default_filtering: document.querySelector('#use_our_default_filtering').checked,
        not_use_any_filtering: document.querySelector('#not_use_any_filtering').checked,
        message: document.querySelector('#message').value,
        attach_in_message: document.querySelector('#attach_in_message').value,
        additional_info: document.querySelector('#additional_info').value,
        contact_details: document.querySelector('#contact_details').value
    })
}

const submitOrderDataCreateForm = () => {
    const compaign_info = JSON.parse(localStorage.compaign_info)

    document.querySelector('#id_targets_or_competitors_submited').value = compaign_info.targets_or_competitors_submited
    document.querySelector('#id_use_our_default_filtering').value = compaign_info.use_our_default_filtering
    document.querySelector('#id_not_use_any_filtering').value = compaign_info.not_use_any_filtering
    document.querySelector('#id_message').value = compaign_info.message
    document.querySelector('#id_attach_in_message').value = compaign_info.attach_in_message
    document.querySelector('#id_additional_information').value = compaign_info.additional_info
    document.querySelector('#id_contact_details').value = compaign_info.contact_details
    document.querySelector('#id_use_tokens').value = document.querySelector('#use_existing_tokens_checkbox').checked

    console.log(document.querySelector('#id_use_tokens').value)
    // document.querySelector('#order_create_form').submit()
}
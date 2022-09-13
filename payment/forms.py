from paypal.standard.forms import PayPalPaymentsForm


class CustomPayPalPaymentsForm(PayPalPaymentsForm):

    def get_html_submit_element(self):

        return """<div class="btn-wrap"><a class="btn" type="submit href="#">DEPOSIT</a></div>"""
        # return """<button type="submit">Continue on PayPal website</button>"""
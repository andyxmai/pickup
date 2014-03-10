class PreviousURL(object):
    def process_response(request, response):
        if response.status_code == 200:
            request.session['previous_url'] = request.get_full_url()
        return response
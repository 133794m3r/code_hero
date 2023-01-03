from json import loads as json_decode

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from code_hero.lib.totp import TotpAuthorize


# TFA related views.
@login_required(login_url='login')
@require_http_methods("GET")
def tfa_qr_code(request):
	domain = request.get_host()
	if not domain:
		domain = 'example.com'
	username = f"{request.user.username}@{domain}"
	new_totp = TotpAuthorize(request.user.tfa_secret)
	request.session['totp_secret'] = new_totp.secret

	qrcode = new_totp.qrcode(username)
	response = HttpResponse(content_type="image/png")
	qrcode.save(response,"PNG")
	return response


@login_required(login_url='login')
@require_http_methods(("GET","POST"))
def tfa_enable(request):
	if request.method == "GET":
		has_tfa_enabled = request.user.tfa_enabled
		return render(request,"two_factor.html",{"enabled":has_tfa_enabled})
	else:
		if request.is_ajax():
			token = json_decode(request.body).get('token')
		else:
			token = request.POST.get('token')

		new_totp = TotpAuthorize(request.session['totp_secret'])
		if token and new_totp.valid(token):
			request.user.tfa_secret = request.session['totp_secret']
			request.user.tfa_enabled = True
			request.user.save()
			enabled = True
			error = ""
		else:
			enabled = False
			error = "The token you provided didn't work. Refresh the page and try again."
		if request.is_ajax():
			return JsonResponse({"enabled":enabled,"error":error})
		else:
			return render(request,"two_factor.html",{"enabled":enabled,error:error})
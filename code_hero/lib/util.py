def jsonify_queryset(queryset: object) -> dict:
	"""
	jsonify_queryset will take a queryset object from the Django.models result
	and return a list of dicts that are ready to be serialized into JSON for
	the use by the API and consumed by the client.


	:param queryset: The object we're working with. May already be a dict.o
	:return: {dict} A dict that's ready to be serialized as JSON.
	"""

	out = []
	if type(queryset) is dict:
		return queryset
	elif len(queryset) > 1:
		for result in queryset:
			if type(result) is dict:
				out.append(result)
			else:
				out.append(result.to_dict())
	else:
		try:
			if queryset.count() == 1:
				tmp = queryset.first()
				if type(tmp) is dict:
					return tmp
				else:
					return tmp.to_dict()
		except AttributeError:
			return queryset.to_dict()

	return out
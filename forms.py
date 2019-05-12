from django import forms
from .models import Blog

<form method='post' action='' enctype="multipart/form-data">
	{% csrf_token %}
	<table>
		{{ form.as_table }}
	</table>
	<input type="submit">
</form>
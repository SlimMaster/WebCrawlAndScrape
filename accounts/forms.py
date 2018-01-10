from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
	
		
		
		if username and password:
			user_qs = User.objects.filter(username=username)
			if user_qs.count() == 1:
				user = user_qs.first()	
			else:
				raise forms.ValidationError("This user doesn't exit")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")

			if not user.is_active:
				raise forms.ValidationError("User no longer active , please re-log in !")

		return super(UserLoginForm,self).clean(*args, **kwargs)

class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = [
			'email',
			'email2',
			'username',			
			'password'
		]

	# def clean(self, *args,**kwargs):
	# 	email = self.cleaned_data.get("email")
	# 	email2 = self.cleaned_data.get("email2")
	# 	if email2 != email:
	# 		raise forms.ValidationError("Emails must much !")
	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This Email has already been registred")
	# 	return super(UserRegistrationForm,self).clean(*args,**kwargs)
	



	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		if email2 != email:
			raise forms.ValidationError("Emails must much !")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This Email has already been registred")
		return email


	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
 #    	email2 = self.cleaned_data.get('email2')
 #    	# if email != email2:
 #    	# 	raise forms.ValidationError("fzef")





 #    	return email
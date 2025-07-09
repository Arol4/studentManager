from django import forms
class LoginForm(forms.Form):
    roles=[   
    ('etudiant','Étudiant'),
    ('enseignant','Enseignant'),
    ('administrateur','Administrateur'),
    ]
    nom=forms.CharField(label="Nom d'utilisateur")
    password=forms.CharField(widget=forms.PasswordInput(),label="Mot de passe")
    role=forms.ChoiceField(
        choices=roles,
        label="Rôle"
    )

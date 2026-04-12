from django import forms
class LoginForm(forms.Form):
    roles=[   
    ('etudiant','Étudiant'),
    ('enseignant','Enseignant'),
    ('administrateur','Administrateur'),
    ]
    nom=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Entrez votre nom d'utilisateur"}), label="Nom d'utilisateur")
    password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Entrez votre mot de passe"}),label="Mot de passe")
    role=forms.ChoiceField(
        choices=roles,
        label="Rôle"
    )

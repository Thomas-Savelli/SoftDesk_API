# SoftDesk - API Rest


Le projet SoftDesk est une initiative visant à créer un backend robuste et sécurisé pour alimenter des applications frontend sur diverses plateformes. Cette API RESTful permettra de traiter et de gérer efficacement les données, offrant une expérience utilisateur optimale.

## **Pour commencer - le téléchargement**

Télécharger l’intégralité du repository sur : https://github.com/Thomas-Savelli/SoftDesk_API.git

Pour ce faire, veuillez ouvrir votre Terminal de Commande: 

1. Grace à la commande cd , dirigez vous vers le répertoire ou vous voulez installer le repository exemple : ```cd Desktop``` *(pour l'installer sur le Desktop de votre ordinateur)*.

2. Par la suite, entrez dans votre terminal la commande : 
```
git clone https://github.com/Thomas-Savelli/SoftDesk_API.git
```
puis appuyer sur entrée afin de créer votre clone local.

## **2/ Installation des dépendances / packages**

Une fois le repository téléchargé et stocké localement, rendez vous dans le dossier SoftDesk_API. Pour cela utiliser la commande : ```cd SoftDesk_API```
- Créer un environnement virtuel afin de récupérer les dépendances et packages du projet.  
*exemple procedure* : ```python -m venv env```
- Contrôler avec ```ls``` que vous disposez maintenant d’un dossier env. Si ce n’est pas le cas, réitérer cette étape en contrôlant la syntaxe de la ligne de commande. Sinon activer votre nouvel environnement virtuel.
  
    exemple procédure : 
    - (PowerShell): ```.\env\Scripts\activate``` 
    - (Windows): ```.\env\Scripts\activate.bat```
    - (autres): ```source env/bin/activate```

*Si vous rencontrez des difficultés vous pouvez vous référer sur le site :* https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows/18713789#18713789
  
  Pour contrôler la réussite de cette manœuvre, vous devriez avoir un ```(env)``` devant votre ligne de commande. Par exemple :

```(env) PS C:\Users\thoma\Desktop\OpenClassrooms\Parcours DA PYTHON\Projet 10\SoftDesk_API>```
  
  PS : Taper seulement ```deactivate``` pour fermer ce dernier.

Pour finir, télécharger avec pip les packages et dépendances requis pour le bon fonctionnement du code avec le requirements.txt en entrant la commande suivante *(dans votre environnement virtuel !)* 

```pip install -r requirements.txt``` 

Une fois le téléchargement effectué et l'installation terminée, vous êtes prêt à exécuter le code.

## **3/ Activation du Serveur en Local**

Afin de pouvoir utiliser et tester l'API rest de SoftDesk, vous devez lancer un serveur local. Pour ce faire, vous devez :

- activer votre environnement virtuel (env)
- dans votre terminal, vous situez dans le dossier de l'application Softdesk :

```(env) PS C:\Users\thoma\Desktop\OpenClassrooms\Parcours DA PYTHON\Projet 10\SoftDesk_API\Softdesk>```
- Lancer le serveur local avec la commande :
``` python manage.py runserver```

Votre serveur local est maintenant lancé. Vous pouvez utiliser la documentation de l'API Rest Softdesk fournie *(documentationAPI.postman_collection.json)* dans Postman ou tout autres outils que vous préférez.


## Dévellopé avec

* Python3 -  [*https://docs.python.org/fr/3/tutorial/index.html*]
* Django -  [*https://pypi.org/project/Django/*]
* djangorestframework -  [*https://www.django-rest-framework.org/*]
* djangorestframework-simplejwt - [*https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html*]
* IDE - [*https://code.visualstudio.com/*] - Visual Studio Code     
* PowerShell - [*https://learn.microsoft.com/fr-fr/powershell/scripting/overview?view=powershell-7.3*]  
* GitHub - [*https://github.com/*]   

## Versions

**Dernière version stable :** Beta 1.0.0  
**Dernière version :** Beta 1.0.0  

## Auteur  
* **Thomas Savelli** [https://github.com/Thomas-Savelli] - ``Devellopeur Python - Junior - SoftDesk``  
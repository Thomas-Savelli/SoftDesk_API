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

- Assurez-vous que Pipenv est installé. Si ce n'est pas le cas, vous pouvez l'installer avec la commande : ```pip install pipenv```

- Créez un environnement virtuel et installez les dépendances à l'aide de Pipenv. Utilisez la commande : ```pipenv install ```

*Si vous rencontrez des problèmes, référez-vous à la documentation de Pipenv pour plus d'informations :* https://pipenv.pypa.io/en/latest/

- Activez votre environnement virtuel avec la commande : : ```pipenv shell ``` 

 (La commande pour desactiver votre environement virtuel est : ```exit``` )

-Une fois l'environnement virtuel activé, vous pouvez télécharger les packages et dépendances requis pour le projet en exécutant : ```pipenv install --dev``` 

Maintenant, vous êtes prêt à exécuter le code.

## **3/ Activation du Serveur en Local**

Afin de pouvoir utiliser et tester l'API Rest de SoftDesk, lancez le serveur local. Dans le dossier de l'application Softdesk (```SoftDesk_API\Softdesk```), assurez-vous que votre environnement virtuel est toujours actif. Si ce n'est pas le cas, activez-le avec ```pipenv shell```.

- Lancer le serveur local avec la commande :
``` python manage.py runserver```

Votre serveur local est maintenant lancé. Vous pouvez utiliser la documentation de l'API Rest Softdesk fournie *(SoftDesk_API_documentation.json)* dans Postman ou tout autres outils que vous préférez.

## **4/ Importation de la Documentation dans Postman**

Pour utiliser facilement notre API REST avec Postman, vous pouvez importer la documentation directement dans votre application Postman. Suivez les étapes ci-dessous :

1. **Téléchargement de la Documentation**

    Vous pouvez trouver la documentation de l'API SoftDesk à la racine de ce projet sous le nom :  SoftDesk_API_documentation.json

2. **Ouverture de Postman**

    Assurez-vous que vous avez [Postman](https://www.postman.com/downloads/) installé sur votre machine. Ouvrez l'application Postman.

3. **Importation de la Collection**

    - Cliquez sur le bouton "Import" en haut à gauche de l'interface Postman.
    - Choisissez l'option "File" et sélectionnez le fichier JSON que vous avez téléchargé.
    - La collection et les requêtes seront importées dans votre application Postman.

4. **Exploration de l'API**

    - Accédez à la section "Collections" sur la barre latérale gauche pour voir la liste des requêtes.
    - Vous trouverez également la documentation détaillée pour chaque requête avec des exemples et des détails sur les paramètres.

5. **Utilisation de l'API**

    Vous pouvez maintenant utiliser les requêtes importées pour interagir avec l'API. Assurez-vous de remplir les informations d'authentification appropriées (par exemple, le token Bearer) dans les requêtes qui nécessitent une authentification.

N'hésitez pas à explorer et tester l'API avec Postman. Si vous avez des questions, consultez la documentation pour obtenir des informations détaillées sur chaque point de terminaison.

Bonne exploration !


## Dévellopé avec

* Python3 -  [*https://docs.python.org/fr/3/tutorial/index.html*]
* Django -  [*https://pypi.org/project/Django/*]
* djangorestframework -  [*https://www.django-rest-framework.org/*]
* djangorestframework-simplejwt - [*https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html*]
* IDE - [*https://code.visualstudio.com/*] - Visual Studio Code     
* PowerShell - [*https://learn.microsoft.com/fr-fr/powershell/scripting/overview?view=powershell-7.3*]  
* GitHub - [*https://github.com/*]
* Postman - [*https://www.postman.com/*] 

## Versions

**Dernière version stable :** Beta 1.0.0  
**Dernière version :** Beta 1.0.0  

## Auteur  
* **Thomas Savelli** [https://github.com/Thomas-Savelli] - ``Devellopeur Python - Junior - SoftDesk``  
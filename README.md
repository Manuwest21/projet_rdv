
Résumé du projet :

    Ce projet est l'élaboration d'un site web à partir du framework django qui se base sur un projet de site pour un coach en developement personnel.
    Nous allons créé un profil "staff" au coach pour qu'il puisse accéder à toutes les fonctionalités du site en se connectant.
    
Fonctionnement du site pour le client:
    
    Le client peut voir des informations sur le coach et ses prestations en se connectant, et avoir plus d'infos sur celui-ci dans les onglets "à propos de moi" et "méthodes de coaching"
    Il a la possibilité de s'enregistrer puis de se connecter avec ses identifiants pour avoir la possibilité de réserver un rdv avec le coach.
    Le client pourra se déconecter du site, ainsi que renouveler son mot de passe, avec un email qui lui sera envoyé (l'envoi est visible depuis le terminal de commandes de l'ordinateur) 
    Il pourra retrouver tous ses rendez-vous personnels dans l'onglet "mes rendez-vous".
    
Fonctionnement du site pour le coach:

Le coach a la possibilité de voir l'onglet "liste des rendez-vous" qui affichera tous ses rendez-vous programmés, avec la possibilité d'écrire une note à propos d'un client, note qui sera reliée à ce client.
Aussi il peut avoir accés à toutes les notes d'un client particulier en allant dans l'onglet "voir notes utilisateurs", il sélectionnera l'utilisateur pour lequel il souhaite avoir accés aux notes déjà prises.


Fonctionnement des rendez-vous:
    
    Le coach propose des rendez-vous en semaine de 9h à 12h30 et de 13h30 à 17h, ses séances sont de 45minutes et le choix de créneau horaires pour le client est établi de manière à ce qu'il ait au minimum 10minutes entre chaque rendez-vous client.
    Il propose la prise de rendez-vous uniquement durant les 60 prochains jours du jour de  l'enregistrement du rendez-vous.
    
    Lors de la réservation, un message d'erreur s'affichera et le rendez-vous ne sera pas enregistré si:
        -le client tente d'effectuer une prise de rendez-vous en dehors des jours allant du lundi au vendredi.
        -à une même date et à un même créneau horaire, un rendez-vous est déjà réservé.
        -le client veut réserver un rendez vous à une date postérieure aux 60 prochains jours de la date de prise de rendez-vous.
    

Instructions de l'utilisation du site par le coach:
  -le coach va créer un profil "superuser" via la commande dans le terminal : <python manage.py createsuperuser> 
    >>> il va pouvoir définir un identifiant et un mot de passe qui lui seront nécessaires pour se connecter sur le site, et aura dés lors accés à ses fonctionnalités suplémentaires.
    >>> il pourra également accéder à l'interface administrateur(via <site>/admin s'il souhaite par exemple supprimer des utilisateurs ou des notes éditées
    >>> de plus s'il travaille avec un collégue, une fois que celui-ci s'est enregistré, il pourra (via la page admin) lui définir le statut "staff" qui lui permettra à lui aussi d'accéder aux planning de tous les rendez-vous, ajouter des notes aux clients ou les consulter. 

    
    

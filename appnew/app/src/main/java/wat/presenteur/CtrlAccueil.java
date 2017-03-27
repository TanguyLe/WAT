package wat.presenteur;

import wat.metier.Bdd;
import wat.metier.Utilisateurs;

/**
 * Created by Link on 02/03/2017.
 */

public class CtrlAccueil {

    private Bdd bdd = new Bdd();
    public String listerUsers() {
        StringBuilder retour = new StringBuilder();

        for (Utilisateurs user : bdd.getUsers()) {
            retour.append(user.getNom());
            retour.append("\n");
        }
        return retour.toString();
    }
}

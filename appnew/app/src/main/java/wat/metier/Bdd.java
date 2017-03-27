package wat.metier;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Link on 02/03/2017.
 */

public class Bdd {

    public List<Utilisateurs> getUsers() {


        List<Utilisateurs> retour = new ArrayList<>();
        retour.add(new Utilisateurs("Toto"));
        retour.add(new Utilisateurs("Titi"));
        retour.add(new Utilisateurs("Tata"));
        retour.add(new Utilisateurs("Tutu"));
        return retour;
    }
}

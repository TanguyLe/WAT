package wat.ihm;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import wat.wat.R;
import wat.presenteur.CtrlAccueil;

public class Accueil extends AppCompatActivity {
    private CtrlAccueil ctrl = new CtrlAccueil();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_accueil);
        afficherUtilisateurs();

    }

    private void afficherUtilisateurs() {
        TextView lstusers = (TextView)findViewById(R.id.Liste);
        lstusers.setText(ctrl.listerUsers());
    }

    public void swapActivity(View view) {
        System.out.println("Action btn");

        Intent intent = new Intent(this, Conversation.class);
        startActivity(intent);

    }
}

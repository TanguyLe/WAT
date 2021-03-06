package com.studio.tlfam.wat;

import android.app.Activity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.content.Intent;

/**
 * Created by tanguy on 09/01/17.
 */

public class ExerciceActivity extends Activity {
    Button myButton = null, myButton2 = null;
    TextView myText = null;

    private View.OnTouchListener touchListenerButtons = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            myButton.setTextSize(Math.abs(event.getX() - myButton.getWidth() / 2) +
                    Math.abs(event.getY() - myButton.getHeight() / 2));
            return true;
        }
    };

    private View.OnClickListener clickListenerButtons = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            Intent myIntent = new Intent(ExerciceActivity.this, GeolocationActivity.class);
            ExerciceActivity.this.startActivity(myIntent);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent intent = getIntent();
        String username = intent.getStringExtra("username");
        String password = intent.getStringExtra("password");

        setContentView(R.layout.exercice_layout);

        myButton = (Button) findViewById(R.id.button1);
        myButton2 = (Button) findViewById(R.id.button2);
        myButton2.setOnClickListener(clickListenerButtons);
        myButton.setOnTouchListener(touchListenerButtons);

        myText = (TextView) findViewById(R.id.authenticatedLabel);
        myText.setText("Coucou " + username + ", ça va ? Au fait j'ai vu ton password : " + password + ", lol.");
    }
}

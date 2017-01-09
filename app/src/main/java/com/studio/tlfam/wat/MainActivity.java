package com.studio.tlfam.wat;

import android.app.Activity;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v4.widget.TextViewCompat;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;


public class MainActivity extends Activity {
    Button monbouton = null;
    TextView myText = null;


    private View.OnClickListener clickListenerButtons = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(monbouton.getText() == "Yolo")
                monbouton.setText("Lala");
            else
                monbouton.setText("Yolo");
        }
    };

    private View.OnTouchListener touchListenerButtons = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            monbouton.setTextSize(Math.abs(event.getX() - monbouton.getWidth() / 2) +
                                  Math.abs(event.getY() - monbouton.getHeight() / 2));
            return true;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.exercice_layout);

        monbouton = (Button)findViewById(R.id.bouton);
        monbouton.setOnTouchListener(touchListenerButtons);
    }
}

package com.studio.tlfam.wat;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.EditText;

/**
 * Created by tanguy on 09/01/17.
 */

public class AuthenticationActivity extends Activity {

    TextView myTextViewUsername = null, myTextViewPassword = null;
    EditText myEditTextUsername = null, myEditTextPassword = null;
    Button submitButton = null;

    private View.OnClickListener clickListenerButtons = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            Intent myIntent = new Intent(AuthenticationActivity.this, ExerciceActivity.class);
            myIntent.putExtra("username", myEditTextUsername.getText().toString());
            myIntent.putExtra("password", myEditTextPassword.getText().toString());
            AuthenticationActivity.this.startActivity(myIntent);
        }
    };

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.authentication_form);

        myTextViewUsername = (TextView)findViewById(R.id.usernameLabel);
        myTextViewPassword = (TextView)findViewById(R.id.passwordLabel);
        myEditTextUsername = (EditText)findViewById(R.id.usernameField);
        myEditTextPassword = (EditText)findViewById(R.id.passwordField);
        submitButton = (Button)findViewById(R.id.submitButton);

        submitButton.setOnClickListener(clickListenerButtons);

    }
}

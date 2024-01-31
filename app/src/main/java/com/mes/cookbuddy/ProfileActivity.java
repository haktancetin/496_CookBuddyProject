package com.mes.cookbuddy;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class ProfileActivity extends AppCompatActivity {

    EditText e_username,e_firstname,e_lastname,e_age,e_email,e_password;
    Button bt_save;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        e_username=(EditText) findViewById(R.id.e_username);
        e_firstname=(EditText) findViewById(R.id.e_firstname);
        e_lastname=(EditText) findViewById(R.id.e_lastname);
        e_age=(EditText) findViewById(R.id.e_age);
        e_email=(EditText) findViewById(R.id.e_email);
        e_password=(EditText) findViewById(R.id.e_password);
        bt_save=(Button) findViewById(R.id.bt_save);

        Intent logHomeInt=getIntent();
        String log_userName=logHomeInt.getStringExtra("log_et_username");

        DataBase db=new DataBase();
        UserInfoForLogin ui=db.userinfoView(log_userName);
        e_username.setText(ui.getUsername());
        e_firstname.setText(ui.getFirstname());
        e_lastname.setText(ui.getLastname());
        e_age.setText(ui.getAge()+"");
        e_email.setText(ui.getEmail());
        e_password.setText(ui.getPassword());

        bt_save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                UserInfoForLogin uinew=new UserInfoForLogin();
                uinew.setUsername(e_username.getText().toString());
                uinew.setFirstname(e_firstname.getText().toString());
                uinew.setLastname(e_lastname.getText().toString());
                int parseint=Integer.parseInt(e_age.getText().toString());
                uinew.setAge(parseint);
                uinew.setEmail(e_email.getText().toString());
                uinew.setPassword(e_password.getText().toString());
                db.userinfoUpdate(uinew);

            }
        });
    }

}
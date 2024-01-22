package com.mes.cookbuddy;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class SignUpActivity extends AppCompatActivity {

EditText et_username,et_firstname,et_lastname,et_age,et_email,et_password,et_passwordverify;
Button bttn_sign;
TextView txt_notverify;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);

        // security
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8){
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        et_username=(EditText) findViewById(R.id.et_username);
        et_firstname=(EditText) findViewById(R.id.et_firstname);
        et_lastname=(EditText) findViewById(R.id.et_lastname);
        et_age=(EditText) findViewById(R.id.et_age);
        et_email=(EditText) findViewById(R.id.et_email);
        et_password=(EditText) findViewById(R.id.et_password);
        et_passwordverify=(EditText) findViewById(R.id.et_passwordverify);
        txt_notverify=(TextView) findViewById(R.id.txt_notverify);

        bttn_sign=(Button) findViewById(R.id.bttn_sign);


        bttn_sign.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                UserInfoForLogin uifl=new UserInfoForLogin();
                uifl.setUsername(et_username.getText().toString());
                uifl.setFirstname(et_firstname.getText().toString());
                uifl.setLastname(et_lastname.getText().toString());
                if(!et_age.getText().toString().isEmpty()){
                    String value=et_age.getText().toString();
                    int val=Integer.parseInt(value);
                    uifl.setAge(val);
                }
                uifl.setEmail(et_email.getText().toString());
                uifl.setPassword(et_password.getText().toString());
                uifl.setPasswordverify(et_passwordverify.getText().toString());

                int control=0;
                     if(uifl.getUsername().isEmpty()){
                        et_username.setHint("Username can not empty.");
                        et_username.setHintTextColor(Color.RED);
                        control=1;
                     }
                    if(uifl.getFirstname().isEmpty()){
                        et_firstname.setHint("First name can not empty.");
                        et_firstname.setHintTextColor(Color.RED);
                        control=1;
                    }
                    if(uifl.getLastname().isEmpty()){
                        et_lastname.setHint("Last name can not empty.");
                        et_lastname.setHintTextColor(Color.RED);
                        control=1;
                    }
                    if((uifl.getAge()+"").isEmpty()){
                        et_age.setHint("Age can not empty.");
                        et_age.setHintTextColor(Color.RED);
                        control=1;
                    }
                    if(uifl.getEmail().isEmpty()){
                        et_email.setHint("Password can not empty.");
                        et_email.setHintTextColor(Color.RED);
                        control=1;
                     }
                    if(uifl.getPassword().isEmpty()){
                        et_password.setHint("Password can not empty.");
                        et_password.setHintTextColor(Color.RED);
                        control=1;
                    }
                    if(uifl.getPasswordverify().isEmpty()){
                        et_passwordverify.setHint("Password verify can not empty.");
                        et_passwordverify.setHintTextColor(Color.RED);
                        control=1;
                    }
                    txt_notverify.setVisibility(View.INVISIBLE);
                    if(!uifl.getPassword().equals(uifl.getPasswordverify())){
                        txt_notverify.setVisibility(View.VISIBLE);
                        control=1;
                    }
                    if(control!=1){
                        DataBase db=new DataBase();
                        if(db.userUsernameCheck(uifl.getUsername())){
                            db.userinfoInsert(uifl.getUsername(),uifl.getEmail(), uifl.getAge(), uifl.getFirstname(),uifl.getLastname(),uifl.getPassword());
                            Intent SignToHome = new Intent(SignUpActivity.this,HomePageActivity.class);
                            startActivity(SignToHome);
                        }
                        else{
                            et_username.setText("");
                            et_username.setHint("Username is used.");
                            et_username.setHintTextColor(Color.RED);
                            control=1;
                        }

                    }
            }
        });

    }

}